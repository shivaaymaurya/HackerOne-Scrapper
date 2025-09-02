import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import json
import re
from tqdm import tqdm
import logging
import sys
from webdriver_manager.chrome import ChromeDriverManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scraper.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

class BaseHackerOneScraper:
    """Base class for HackerOne scrapers"""
    
    def __init__(self, output_file, category_name):
        """Initialize the scraper with output file and category name"""
        self.output_file = output_file
        self.category_name = category_name
        self.links = []
        self.total_links = 0
        self.current_link = ""
        self.logger = logging.getLogger(f"{category_name}Scraper")
        
        # Create session with headers
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        })
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Initialize Chrome options for Selenium
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--window-size=1920,1080")
        self.chrome_options.add_argument("--disable-notifications")
        self.chrome_options.add_argument("--disable-extensions")
        self.chrome_options.add_argument("--disable-infobars")
        
        # User agent
        self.chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
    def setup_driver(self):
        """Set up and return a Chrome webdriver"""
        try:
            # Try to use webdriver-manager to get the ChromeDriver
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=self.chrome_options)
        except Exception as e:
            self.logger.warning(f"Failed to use webdriver-manager: {e}")
            # Fallback to default Chrome webdriver
            driver = webdriver.Chrome(options=self.chrome_options)
            
        driver.set_page_load_timeout(30)
        return driver
        
    def save_links(self):
        """Save the collected links to the output file"""
        try:
            with open(self.output_file, 'w') as f:
                for link in self.links:
                    f.write(f"{link}\n")
            self.logger.info(f"Saved {len(self.links)} {self.category_name} links to {self.output_file}")
        except Exception as e:
            self.logger.error(f"Error saving links to {self.output_file}: {e}")
        
    def load_existing_links(self):
        """Load existing links from the output file if it exists"""
        if os.path.exists(self.output_file):
            try:
                with open(self.output_file, 'r') as f:
                    self.links = [line.strip() for line in f.readlines()]
                self.logger.info(f"Loaded {len(self.links)} existing {self.category_name} links from {self.output_file}")
            except Exception as e:
                self.logger.error(f"Error loading links from {self.output_file}: {e}")
                self.links = []
            
    def update_progress(self, current, total, link=""):
        """Update and display the progress"""
        self.current_link = link
        self.logger.debug(f"Progress: {current}/{total} {self.category_name} links scraped | Current: {link}")
        
    def scrape(self):
        """Main scrape method to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement the scrape method")
        
    def run(self):
        """Run the scraper"""
        self.logger.info(f"Starting {self.category_name} scraper...")
        self.load_existing_links()
        
        start_time = time.time()
        try:
            self.scrape()
            self.save_links()
            
            elapsed_time = time.time() - start_time
            self.logger.info(f"Completed {self.category_name} scraping in {elapsed_time:.2f} seconds")
            self.logger.info(f"Total {self.category_name} links: {len(self.links)}")
            
        except KeyboardInterrupt:
            self.logger.warning("Scraping interrupted by user")
            self.save_links()  # Save what we have so far
        except Exception as e:
            self.logger.error(f"Error during scraping: {e}")
            self.save_links()  # Save what we have so far