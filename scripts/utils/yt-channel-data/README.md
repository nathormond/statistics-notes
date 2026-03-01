# yt-channel-data

Fetch all videos, livestreams, and shorts for a YouTube channel and export them to CSV.

## Setup

```bash
# Create / update the conda environment
conda env create -f environment.yml
conda activate stats-notes-python

# Add your YouTube Data API v3 key to .env
echo 'YOUTUBE_API_KEY=your-key-here' > .env
```

To get an API key: Google Cloud Console > APIs & Services > Enable **YouTube Data API v3** > Credentials > Create API key.

## Configuration

Edit `config.json` to set the target channel:

```json
{
  "channel_name": "trigggerpod",
  "channel_id": "UC7oPkqeHTwuOZ5CZ-R9f-6w"
}
```

- `channel_name` — slug used in the output filename
- `channel_id` — the YouTube channel ID (find it in the channel URL or via YouTube's advanced settings)

## Usage

```bash
# Test API access with a single video
python channel-data.py --test

# Fetch all uploads
python channel-data.py

# Filter by type
python channel-data.py --type video
python channel-data.py --type video livestream
python channel-data.py --type short
```

## Output

CSV files are written to `data/<YYYY-MM-DD>/<channel-name>.csv` (relative to the project root) with columns:

| Column | Description |
|---|---|
| `published_date` | Publication date (YYYY-MM-DD) |
| `type` | `video`, `short`, or `livestream` |
| `title` | Video title |
| `url` | Link to the video |
