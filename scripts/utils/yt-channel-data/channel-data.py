"""
Fetch all videos (uploads, livestreams, shorts) for a YouTube channel
and write them to a CSV under data/<invocation-date>/<channel-name>.csv
"""

import argparse
import csv
import json
import os
import sys
from datetime import date, datetime

from dotenv import load_dotenv
from googleapiclient.discovery import build

# ── Config ────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

load_dotenv(os.path.join(SCRIPT_DIR, ".env"))

CONFIG_PATH = os.path.join(SCRIPT_DIR, "config.json")

with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

CHANNEL_NAME = config["channel_name"]
CHANNEL_ID = config["channel_id"]
API_KEY = os.environ.get("YOUTUBE_API_KEY")
# ──────────────────────────────────────────────────────────────────────

DATA_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "..", "..", "data"))

SHORTS_MAX_DURATION_SECONDS = 60


def build_client():
    if not API_KEY:
        sys.exit("Error: set the YOUTUBE_API_KEY environment variable.")
    return build("youtube", "v3", developerKey=API_KEY)


def get_uploads_playlist_id(youtube, channel_id):
    resp = youtube.channels().list(
        id=channel_id,
        part="contentDetails",
    ).execute()
    items = resp.get("items", [])
    if not items:
        sys.exit(f"Error: no channel found for id {channel_id}")
    return items[0]["contentDetails"]["relatedPlaylists"]["uploads"]


def fetch_all_video_ids(youtube, playlist_id):
    """Return list of (video_id, title, published_at) from the uploads playlist."""
    results = []
    next_page = None

    while True:
        resp = youtube.playlistItems().list(
            playlistId=playlist_id,
            part="snippet",
            maxResults=50,
            pageToken=next_page,
        ).execute()

        for item in resp["items"]:
            snippet = item["snippet"]
            results.append({
                "video_id": snippet["resourceId"]["videoId"],
                "title": snippet["title"],
                "description": snippet.get("description", ""),
                "published_at": snippet["publishedAt"],
            })

        next_page = resp.get("nextPageToken")
        if not next_page:
            break

    return results


def iso8601_duration_to_seconds(duration):
    """Convert ISO 8601 duration (PT#H#M#S) to total seconds."""
    import re

    match = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", duration)
    if not match:
        return 0
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = int(match.group(3) or 0)
    return hours * 3600 + minutes * 60 + seconds


def classify_videos(youtube, video_entries):
    """Batch-fetch video details and classify each as video, livestream, or short."""
    ids = [v["video_id"] for v in video_entries]

    details = {}
    # videos().list accepts max 50 ids at a time
    for i in range(0, len(ids), 50):
        batch = ids[i : i + 50]
        resp = youtube.videos().list(
            id=",".join(batch),
            part="contentDetails,liveStreamingDetails,statistics,snippet,topicDetails",
        ).execute()
        for item in resp["items"]:
            details[item["id"]] = item

    classified = []
    for entry in video_entries:
        vid = entry["video_id"]
        detail = details.get(vid)
        if not detail:
            continue

        duration_iso = detail["contentDetails"].get("duration", "PT0S")
        duration_s = iso8601_duration_to_seconds(duration_iso)
        is_live = "liveStreamingDetails" in detail

        if is_live:
            video_type = "livestream"
        elif duration_s <= SHORTS_MAX_DURATION_SECONDS:
            video_type = "short"
        else:
            video_type = "video"

        published = datetime.fromisoformat(
            entry["published_at"].replace("Z", "+00:00")
        )

        stats = detail.get("statistics", {})
        detail_snippet = detail.get("snippet", {})
        topics = detail.get("topicDetails", {})

        # Pipe-delimit lists so they don't break CSV columns
        tags = detail_snippet.get("tags", [])
        topic_cats = topics.get("topicCategories", [])

        # Collapse newlines/tabs to single spaces for clean CSV output
        title = " ".join(entry["title"].split())
        description = " ".join(entry.get("description", "").split())

        classified.append({
            "published_date": published.strftime("%Y-%m-%d"),
            "type": video_type,
            "title": title,
            "description": description,
            "url": f"https://www.youtube.com/watch?v={vid}",
            "view_count": stats.get("viewCount", ""),
            "like_count": stats.get("likeCount", ""),
            "comment_count": stats.get("commentCount", ""),
            "category_id": detail_snippet.get("categoryId", ""),
            "tags": "|".join(tags),
            "topic_categories": "|".join(topic_cats),
        })

    return classified


def write_csv(rows, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "published_date", "type", "title", "description", "url",
            "view_count", "like_count", "comment_count",
            "category_id", "tags", "topic_categories",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {output_path}")


def test(youtube):
    """Fetch one video and print the result to verify API access."""
    print(f"[test] Fetching uploads playlist for channel {CHANNEL_ID} …")
    playlist_id = get_uploads_playlist_id(youtube, CHANNEL_ID)

    resp = youtube.playlistItems().list(
        playlistId=playlist_id,
        part="snippet",
        maxResults=1,
    ).execute()

    if not resp["items"]:
        sys.exit("No videos found on this channel.")

    snippet = resp["items"][0]["snippet"]
    entry = {
        "video_id": snippet["resourceId"]["videoId"],
        "title": snippet["title"],
        "description": snippet.get("description", ""),
        "published_at": snippet["publishedAt"],
    }

    rows = classify_videos(youtube, [entry])
    print("[test] Single video result:")
    for k, v in rows[0].items():
        print(f"  {k}: {v}")


ALL_TYPES = {"video", "short", "livestream"}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Fetch YouTube channel video metadata to CSV."
    )
    parser.add_argument(
        "--test", action="store_true",
        help="Fetch a single video and print the result (no file written).",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Fetch a single video and write it to CSV to verify output.",
    )
    parser.add_argument(
        "--type", nargs="+", choices=sorted(ALL_TYPES), default=None,
        help="Only include these types (e.g. --type video livestream).",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    youtube = build_client()

    if args.test:
        test(youtube)
        return

    type_filter = set(args.type) if args.type else ALL_TYPES

    print(f"Fetching uploads playlist for channel {CHANNEL_ID} …")
    playlist_id = get_uploads_playlist_id(youtube, CHANNEL_ID)

    if args.dry_run:
        resp = youtube.playlistItems().list(
            playlistId=playlist_id,
            part="snippet",
            maxResults=1,
        ).execute()
        snippet = resp["items"][0]["snippet"]
        entries = [{
            "video_id": snippet["resourceId"]["videoId"],
            "title": snippet["title"],
            "description": snippet.get("description", ""),
            "published_at": snippet["publishedAt"],
        }]
        print("[dry-run] Fetched 1 video to test file output.")
    else:
        print("Fetching all video IDs …")
        entries = fetch_all_video_ids(youtube, playlist_id)
        print(f"Found {len(entries)} uploads.")

    print("Classifying videos (batched detail lookups) …")
    rows = classify_videos(youtube, entries)

    rows = [r for r in rows if r["type"] in type_filter]

    # sort chronologically
    rows.sort(key=lambda r: r["published_date"])

    print(f"Keeping {len(rows)} rows (types: {', '.join(sorted(type_filter))}).")

    today = date.today().isoformat()
    out_dir = os.path.join(DATA_DIR, today)
    out_file = os.path.join(out_dir, f"{CHANNEL_NAME}.csv")

    write_csv(rows, out_file)


if __name__ == "__main__":
    main()
