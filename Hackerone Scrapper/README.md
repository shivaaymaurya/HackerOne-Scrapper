# HackerOne Link Scraper

A comprehensive tool to scrape HackerOne links for CVEs, CWEs, disclosed reports, and undisclosed reports.

## Features

- Scrapes CVE links from HackerOne
- Scrapes CWE links from HackerOne
- Scrapes disclosed report links from HackerOne
- Scrapes undisclosed report links from HackerOne
- Shows live progress during scraping
- Saves all links to separate text files

## Requirements

- Python 3.7+
- Chrome browser (for Selenium WebDriver)

## Installation

1. Clone this repository:
```
git clone https://github.com/yourusername/hackerone-link-scraper.git
cd hackerone-link-scraper
```

2. Install the required packages:
```
pip install -r requirements.txt
```

3. Install ChromeDriver:
   - For Linux: `apt-get install chromium-chromedriver`
   - For macOS: `brew install --cask chromedriver`
   - For Windows: Download from https://chromedriver.chromium.org/downloads

## Usage

### Run all scrapers

To run all scrapers (CVE, CWE, disclosed, undisclosed):

```
python main.py
```

### Run a specific scraper

To run only a specific scraper:

```
python main.py --type cve          # Run only the CVE scraper
python main.py --type cwe          # Run only the CWE scraper
python main.py --type disclosed    # Run only the disclosed reports scraper
python main.py --type undisclosed  # Run only the undisclosed reports scraper
```

## Output

The scraped links are saved to the following files in the `output` directory:

- `cve_links.txt`: Contains all CVE links
- `cwe_links.txt`: Contains all CWE links
- `disclosed_links.txt`: Contains all disclosed report links
- `undisclosed_links.txt`: Contains all undisclosed report links

## Progress Tracking

The tool displays live progress during scraping, showing:
- Current progress (X/Y links scraped)
- Currently processing link
- Total links found after completion

## Notes

- The tool uses Selenium WebDriver to interact with the HackerOne website
- Rate limiting is implemented to avoid overloading the HackerOne servers
- The tool can be stopped and resumed, as it will load existing links from the output files