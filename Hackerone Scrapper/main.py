#!/usr/bin/env python3
import os
import time
import argparse
import logging
import sys
from cve_scraper import CVEScraper
from cwe_scraper import CWEScraper
from disclosed_reports_scraper import DisclosedReportsScraper
from undisclosed_reports_scraper import UndisclosedReportsScraper

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("hackerone_scraper.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("HackerOneScraper")

def create_output_directory():
    """Create the output directory if it doesn't exist"""
    os.makedirs("output", exist_ok=True)
    logger.info("Output directory created/verified")

def print_banner():
    """Print a banner for the tool"""
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║   ██╗  ██╗ █████╗  ██████╗██╗  ██╗███████╗██████╗  ██████╗    ║
    ║   ██║  ██║██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗██╔═══██╗   ║
    ║   ███████║███████║██║     █████╔╝ █████╗  ██████╔╝██║   ██║   ║
    ║   ██╔══██║██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗██║   ██║   ║
    ║   ██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║╚██████╔╝   ║
    ║   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝    ║
    ║                                                               ║
    ║   ██╗     ██╗███╗   ██╗██╗  ██╗                              ║
    ║   ██║     ██║████╗  ██║██║ ██╔╝                              ║
    ║   ██║     ██║██╔██╗ ██║█████╔╝                               ║
    ║   ██║     ██║██║╚██╗██║██╔═██╗                               ║
    ║   ███████╗██║██║ ╚████║██║  ██╗                              ║
    ║   ╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝                              ║
    ║                                                               ║
    ║   ███████╗ ██████╗██████╗  █████╗ ██████╗ ███████╗██████╗    ║
    ║   ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗   ║
    ║   ███████╗██║     ██████╔╝███████║██████╔╝█████╗  ██████╔╝   ║
    ║   ╚════██║██║     ██╔══██╗██╔══██║██╔═══╝ ██╔══╝  ██╔══██╗   ║
    ║   ███████║╚██████╗██║  ██║██║  ██║██║     ███████╗██║  ██║   ║
    ║   ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝   ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)
    print("  HackerOne Link Scraper - Extract CVE, CWE, and Report Links")
    print("  ============================================================\n")

def run_all_scrapers():
    """Run all scrapers sequentially"""
    start_time = time.time()
    
    # Create output directory
    create_output_directory()
    
    # Run CVE scraper
    print("\n=== Running CVE Scraper ===")
    cve_scraper = CVEScraper()
    cve_scraper.run()
    
    # Run CWE scraper
    print("\n=== Running CWE Scraper ===")
    cwe_scraper = CWEScraper()
    cwe_scraper.run()
    
    # Run Disclosed Reports scraper
    print("\n=== Running Disclosed Reports Scraper ===")
    disclosed_scraper = DisclosedReportsScraper()
    disclosed_scraper.run()
    
    # Run Undisclosed Reports scraper
    print("\n=== Running Undisclosed Reports Scraper ===")
    undisclosed_scraper = UndisclosedReportsScraper()
    undisclosed_scraper.run()
    
    # Print summary
    total_time = time.time() - start_time
    print("\n=== Scraping Summary ===")
    print(f"Total execution time: {total_time:.2f} seconds")
    
    # Count links in each file
    cve_count = count_lines("output/cve_links.txt")
    cwe_count = count_lines("output/cwe_links.txt")
    disclosed_count = count_lines("output/disclosed_links.txt")
    undisclosed_count = count_lines("output/undisclosed_links.txt")
    
    print(f"CVE Links: {cve_count}")
    print(f"CWE Links: {cwe_count}")
    print(f"Disclosed Report Links: {disclosed_count}")
    print(f"Undisclosed Report Links: {undisclosed_count}")
    print(f"Total Links: {cve_count + cwe_count + disclosed_count + undisclosed_count}")

def run_specific_scraper(scraper_type):
    """Run a specific scraper based on the type"""
    create_output_directory()
    
    if scraper_type == "cve":
        print("\n=== Running CVE Scraper ===")
        scraper = CVEScraper()
    elif scraper_type == "cwe":
        print("\n=== Running CWE Scraper ===")
        scraper = CWEScraper()
    elif scraper_type == "disclosed":
        print("\n=== Running Disclosed Reports Scraper ===")
        scraper = DisclosedReportsScraper()
    elif scraper_type == "undisclosed":
        print("\n=== Running Undisclosed Reports Scraper ===")
        scraper = UndisclosedReportsScraper()
    else:
        logger.error(f"Unknown scraper type: {scraper_type}")
        return
    
    start_time = time.time()
    scraper.run()
    total_time = time.time() - start_time
    
    # Count links in the file
    count = count_lines(scraper.output_file)
    print(f"\n=== Scraping Summary ===")
    print(f"Execution time: {total_time:.2f} seconds")
    print(f"Total {scraper_type} links: {count}")

def count_lines(file_path):
    """Count the number of lines in a file"""
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return len(f.readlines())
        return 0
    except Exception as e:
        logger.error(f"Error counting lines in {file_path}: {e}")
        return 0

def check_dependencies():
    """Check if all required dependencies are installed"""
    try:
        import selenium
        import requests
        import bs4
        import tqdm
        import webdriver_manager
        logger.info("All dependencies are installed")
        return True
    except ImportError as e:
        logger.error(f"Missing dependency: {e}")
        print("\nPlease install all required dependencies:")
        print("pip install -r requirements.txt")
        return False

if __name__ == "__main__":
    # Print banner
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="HackerOne Link Scraper")
    parser.add_argument("--type", choices=["all", "cve", "cwe", "disclosed", "undisclosed"], 
                        default="all", help="Type of scraper to run")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    
    args = parser.parse_args()
    
    # Set logging level based on verbose flag
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.info("Verbose logging enabled")
    
    try:
        if args.type == "all":
            run_all_scrapers()
        else:
            run_specific_scraper(args.type)
    except KeyboardInterrupt:
        logger.warning("Scraping interrupted by user")
        print("\nScraping interrupted. Partial results have been saved.")
    except Exception as e:
        logger.error(f"Error during scraping: {e}")
        print(f"\nAn error occurred: {e}")
        print("Check the log file for more details: hackerone_scraper.log")