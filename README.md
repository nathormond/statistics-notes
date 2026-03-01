# Statistics Notes

A repository for notes and investigations into statistical concepts, accompanied by hands-on R code examples and visualisations.

## Overview

This project serves as a personal repository for notes and investigations into various statistical concepts. It leverages [Quarto](https://quarto.org/) to create an interactive website where each topic is explored through hands-on R code examples and visualizations. The goal is to provide a clear and reproducible way to understand statistical principles as I investigate them.

## Features

- **Interactive Demonstrations**: Run R code directly in the browser
- **Reproducible Package Management**: Uses `renv` for project-specific R package management, ensuring consistent environments.
- **Visual Learning**: Rich plots and visualizations for each concept
- **Mathematical Foundation**: Formal mathematical notation and explanations
- **Responsive Design**: Works on desktop and mobile devices

## Current Topics

- **Central Limit Theorem**: Understanding how sampling distributions approach normality
- **Chatbot Effects on Postpartum Mental Health**: An analysis and discussion of a paper on chatbot therapy.
- *More topics coming soon...*

## Project Structure

```
stats-concepts/
├── _quarto.yml                    # Quarto configuration
├── index.qmd                      # Homepage
├── about.qmd                      # About page
├── styles.css                     # Custom CSS styling
├── README.md                      # This file
│
├── src/                           # Source Quarto documents
│   ├── teaching-stats/            # Educational content
│   │   └── core-concepts/         # Core statistical concepts
│   │       ├── central-limit-theorem.qmd
│   │       ├── degrees-of-freedom.qmd
│   │       └── template.qmd
│   └── blog/                      # Blog-style articles and reviews
│       ├── paper-reviews/         # Paper review articles
│       │   ├── index.qmd
│       │   └── chatbot-mental-health/
│       │       └── chatbot-postpartum-mental-health.qmd
│       └── essays/                # Opinion pieces and essays
│
├── data/                          # Data files (for external datasets, if needed)
├── resources/                     # Resources and generated content
│   └── images/                    # Generated plots and images
│       ├── clt-demo/
│       └── plots/
├── scripts/                       # Helper scripts
│   ├── generate_nav.R           # Auto-generate navigation from directory structure
│   └── serve.sh                  # Render and serve the site locally
│
├── renv/                          # R environment management
├── renv.lock                      # R package lock file
└── stats-concepts.Rproj           # RStudio project file
```

## Prerequisites

Before you begin, ensure you have the following installed:

### Required Software

1. **R** (version 4.0 or higher)
   - Download from [r-project.org](https://www.r-project.org/)
   - Or install via package manager:
     ```bash
     # macOS (using Homebrew)
     brew install r
     
     # Ubuntu/Debian
     sudo apt-get install r-base
     ```

2. **Quarto** (version 1.0 or higher)
   - Download from [quarto.org](https://quarto.org/docs/get-started/)
   - Or install via package manager:
     ```bash
     # macOS (using Homebrew)
     brew install quarto
     
     # Ubuntu/Debian
     wget https://github.com/quarto-dev/quarto-cli/releases/download/v1.4.549/quarto-1.4.549-linux-amd64.deb
     sudo dpkg -i quarto-1.4.549-linux-amd64.deb
     ```

3. **RStudio** (optional but recommended)
   - Download from [posit.co](https://posit.co/download/rstudio-desktop/)

### Verify Installation

Check that both R and Quarto are properly installed:

```bash
# Check R version
R --version

# Check Quarto version
quarto --version
```

## Setup Instructions

### 1. Clone or Download the Repository

```bash
# If using git
git clone git@github.com:nathormond/statistics-notes.git
cd stats-concepts

# Or download and extract the ZIP file
```

### 2. Install R Dependencies

This project uses `renv` to ensure a reproducible R environment. All required packages are listed in the `renv.lock` file.

To get started, follow these steps in your R console:

1.  **Restore the Environment:**
    This command installs the exact versions of all R packages used in the project.
    ```r
    renv::restore()
    ```

2.  **Developing and Adding Packages:**
    If you need to add a new package for your analysis, use:
    ```r
    renv::install("new-package-name")
    ```

3.  **Save Your Changes:**
    After installing or updating packages, save your changes to the lockfile. This is crucial for reproducibility.
    ```r
    renv::snapshot()
    ```
    Commit the updated `renv.lock` file to your Git repository.

### 3. Python Environment (for utility scripts)

Some helper scripts under `scripts/utils/` are written in Python. A conda environment is provided **scoped to those scripts** (kept separate from the Quarto/R setup to avoid conflicts).

```bash
# Create the environment (one-time)
conda env create -f scripts/utils/yt-channel-data/environment.yml

# Activate it
conda activate stats-notes-python
```

The environment only needs to be active when running Python utility scripts — it is not required for Quarto rendering or R workflows.

### 4. Verify Setup

Test that everything is working:

```bash
# Render the website
quarto render
```

If successful, you should see output indicating that the files were rendered to the `_site/` directory.

## How to Serve the Website (For Developers)

This section outlines how to build and serve the website locally for development and testing.

### Local Development Server (Recommended)

For active development, use Quarto's built-in preview server. This provides live reloading as you make changes.

```bash
# Start a local development server
quarto preview

# Or with a specific port
quarto preview --port 4242
```

This command will:
- Start a local web server (typically at `http://localhost:4848`).
- Automatically reload the browser when you save changes to `.qmd` files.
- Display a live preview of your edits.

### Building Static Files

To generate the static HTML files for deployment or local serving without live reloading:

```bash
# Build the entire website
quarto render
```

The generated static files will be located in the `_site/` directory. You can then serve these files using any web server (e.g., Python's `http.server`, Node.js `http-server`, or a simple static file server).

### Serving Built Files

#### Quick Serve Script (Recommended)

Use the convenience script to render and serve in one command:

```bash
# Render and serve on default port 8080
./scripts/serve.sh

# Or specify a custom port
./scripts/serve.sh 3000
```

This script will:
- Render the Quarto site
- Automatically detect and use an available web server (Python, Node.js, etc.)
- Start a local server and display the URL
- Handle cleanup gracefully when you stop it (Ctrl+C)

#### Manual Serving

If you prefer to build and serve manually:

**Using Python's Built-in Server:**

```bash
# First, build the site
quarto render

# Then, navigate to the output directory and serve
cd _site
python3 -m http.server 8080
# Access in your browser at http://localhost:8080
```

**Using Node.js http-server:**

```bash
# Build the site
quarto render

# Navigate to the output directory and serve
cd _site
npx --yes http-server -p 8080
# Access in your browser at http://localhost:8080
```

## Development Workflow

### Adding New Concepts

1. **Copy the template**:
   ```bash
   cp src/teaching-stats/core-concepts/template.qmd src/teaching-stats/core-concepts/your-concept-name.qmd
   ```

2. **Edit the new file**:
   - Update the YAML header with your concept name
   - Replace placeholder content with your demonstration
   - Add your R code in the code blocks

3. **Update navigation automatically**:
   Run the navigation generator script to automatically update `_quarto.yml`:
   ```r
   source("scripts/generate_nav.R")
   ```
   Or from the command line:
   ```bash
   Rscript scripts/generate_nav.R
   ```
   
   This script scans your `src/` directory, reads YAML headers from `.qmd` files to get titles, and automatically updates the navigation structure in `_quarto.yml`. No more manual editing of navigation links!

4. **Test your changes**:
   ```bash
   quarto preview
   ```

### Code Block Best Practices

- Use `#| echo: true` to show code
- Use `#| warning: false` to suppress warnings
- Use `#| message: false` to suppress messages
- Set `set.seed()` for reproducible results

### Example Code Block

```r
#| echo: true
#| warning: false
#| message: false

# Your demonstration code here
```

## Local Testing and CI Simulation

### Unified test runner

Use the unified script to test builds locally or simulate CI with `act`.

Manual build test (recommended):

```bash
./scripts/test.sh
```

This will:
- Restore `renv` packages
- Generate navigation
- Render the site with Quarto
- Verify `_site/index.html`

CI test using `act` (syntax/flow validation):

```bash
# Basic
./scripts/test.sh --ci

# Apple Silicon (force amd64 containers)
./scripts/test.sh --ci --amd64

# Explicit token (otherwise uses gh auth token if available)
./scripts/test.sh --ci --token YOUR_GITHUB_TOKEN
```

Notes:
- `act` can’t fully replicate GitHub Actions; Quarto setup may fail due to missing `gh` CLI in containers. Use the manual build test for reliable local validation.

## Deployment

### GitHub Pages

1. Push your code to a GitHub repository
2. Enable GitHub Pages in repository settings
3. Set source to "GitHub Actions"
4. Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: r-lib/actions/setup-r@v2
      with:
        r-version: '4.2'
    - uses: r-lib/actions/setup-renv@v2
    - name: Install Quarto
      uses: quarto-dev/quarto-actions/install@v2
    - name: Render
      run: quarto render
    - name: Deploy
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./_site
```

### Netlify

1. Connect your repository to Netlify
2. Set build command: `quarto render`
3. Set publish directory: `_site`

### Vercel

1. Connect your repository to Vercel
2. Set build command: `quarto render`
3. Set output directory: `_site`

## Troubleshooting

### Common Issues

**"Package not found" errors:**
- Ensure you have run `source("setup_project_packages.R")` or `renv::restore()` to install all project dependencies.
- Check that you have internet access for package downloads.
- Verify that the package is listed in `renv.lock`. If not, you may need to install it and run `renv::snapshot()`.

**Rendering fails:**
- Verify R and Quarto are properly installed
- Check that all required packages are available
- Look for syntax errors in your R code

**Images not displaying:**
- Ensure image files are in the correct directory
- Check file paths are relative to the project root

**Navigation not working:**
- Verify `_quarto.yml` syntax is correct
- Check that file paths in navigation match actual file locations

### Getting Help

- Check the [Quarto documentation](https://quarto.org/docs/)
- Review R error messages for specific issues
- Ensure all prerequisites are properly installed

## Contributing

Contributions are welcome! If you'd like to add new concepts, improve existing ones, or fix issues, please follow these steps:

1.  **Fork the repository**: Start by forking this repository to your GitHub account.
2.  **Clone your fork**: Clone your forked repository to your local machine.
    ```bash
    git clone https://github.com/YOUR_USERNAME/stats-notes.git
    cd stats-notes
    ```
3.  **Create a new branch**: Create a new branch for your feature or bug fix.
    ```bash
    git checkout -b feature/your-feature-name
    ```
4.  **Make your changes**: Implement your changes, add new `.qmd` files for concepts, or update existing ones.
5.  **Test locally**: Ensure your changes work as expected by building and previewing the site locally.
    ```bash
    quarto preview
    ```
6.  **Commit your changes**: Commit your changes with a clear and concise commit message.
7.  **Push to your fork**: Push your new branch to your forked repository on GitHub.
8.  **Open a Pull Request**: Create a pull request from your fork to the `main` branch of this repository. Describe your changes in detail.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## References

References for all papers and discussions are provided inline within the respective Quarto documents.

## Acknowledgments

- Built with [Quarto](https://quarto.org/)
- Powered by [R](https://www.r-project.org/)
- Visualizations created with [ggplot2](https://ggplot2.tidyverse.org/) 