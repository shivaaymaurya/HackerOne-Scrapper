# HackerOne Link Scraper Todo

## Research Phase
- [x] Research HackerOne website structure
- [x] Analyze CVE page structure and pagination
- [x] Analyze CWE page structure and pagination
- [x] Analyze disclosed reports structure and pagination
- [x] Analyze undisclosed reports structure and pagination
- [x] Determine best scraping approach for each category

## Development Phase
- [x] Create base scraper structure
- [x] Implement CVE link scraper
  - [x] Extract CVE IDs from the table
  - [x] Generate URLs in the format: https://hackerone.com/hacktivity/cve_discovery?id=CVE-XXXX-XXXXX
  - [x] Handle pagination to get all CVEs
  - [x] Save to cve_links.txt with progress tracking
- [x] Implement CWE link scraper
  - [x] Extract CWE IDs from the table
  - [x] Generate URLs in the format: https://hackerone.com/hacktivity/cwe_discovery?id=cwe-XX
  - [x] Handle pagination to get all CWEs
  - [x] Save to cwe_links.txt with progress tracking
- [x] Implement disclosed reports scraper
  - [x] Extract report IDs from the page
  - [x] Generate URLs in the format: https://hackerone.com/reports/XXXXXXX
  - [x] Handle pagination to get all disclosed reports
  - [x] Save to disclosed_links.txt with progress tracking
- [x] Implement undisclosed reports scraper
  - [x] Extract report information from the page
  - [x] Generate URLs in the format: https://hackerone.com/hacktivity/overview?queryString=disclosed%3Afalse&sortField=latest_disclosable_activity_at&sortDirection=DESC&pageIndex=X
  - [x] Handle pagination to get all undisclosed reports
  - [x] Save to undisclosed_links.txt with progress tracking
- [x] Implement progress tracking functionality
  - [x] Show current progress (X/Y links scraped)
  - [x] Display currently processing link
  - [x] Show estimated time remaining

## Testing Phase
- [x] Test CVE scraper
- [x] Test CWE scraper
- [x] Test disclosed reports scraper
- [x] Test undisclosed reports scraper
- [x] Verify output files

## Finalization
- [x] Create main script to run all scrapers
- [x] Add documentation
- [x] Final testing