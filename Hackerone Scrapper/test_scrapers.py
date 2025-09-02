#!/usr/bin/env python3
import unittest
import os
import sys
import logging
from cve_scraper import CVEScraper
from cwe_scraper import CWEScraper
from disclosed_reports_scraper import DisclosedReportsScraper
from undisclosed_reports_scraper import UndisclosedReportsScraper

# Disable logging for tests
logging.disable(logging.CRITICAL)

class TestScrapers(unittest.TestCase):
    """Test cases for HackerOne scrapers"""
    
    def setUp(self):
        """Set up test environment"""
        # Create test output directory
        os.makedirs("test_output", exist_ok=True)
        
    def tearDown(self):
        """Clean up after tests"""
        # Remove test files
        for file in ["test_output/cve_test.txt", "test_output/cwe_test.txt", 
                    "test_output/disclosed_test.txt", "test_output/undisclosed_test.txt"]:
            if os.path.exists(file):
                os.remove(file)
    
    def test_cve_scraper_initialization(self):
        """Test CVE scraper initialization"""
        scraper = CVEScraper()
        self.assertEqual(scraper.output_file, "output/cve_links.txt")
        self.assertEqual(scraper.category_name, "CVE")
        self.assertEqual(scraper.base_url, "https://hackerone.com/hacktivity/cve_discovery")
    
    def test_cwe_scraper_initialization(self):
        """Test CWE scraper initialization"""
        scraper = CWEScraper()
        self.assertEqual(scraper.output_file, "output/cwe_links.txt")
        self.assertEqual(scraper.category_name, "CWE")
        self.assertEqual(scraper.base_url, "https://hackerone.com/hacktivity/cwe_discovery")
    
    def test_disclosed_reports_scraper_initialization(self):
        """Test disclosed reports scraper initialization"""
        scraper = DisclosedReportsScraper()
        self.assertEqual(scraper.output_file, "output/disclosed_links.txt")
        self.assertEqual(scraper.category_name, "Disclosed Reports")
        self.assertEqual(scraper.base_url, "https://hackerone.com/hacktivity/overview")
    
    def test_undisclosed_reports_scraper_initialization(self):
        """Test undisclosed reports scraper initialization"""
        scraper = UndisclosedReportsScraper()
        self.assertEqual(scraper.output_file, "output/undisclosed_links.txt")
        self.assertEqual(scraper.category_name, "Undisclosed Reports")
        self.assertEqual(scraper.base_url, "https://hackerone.com/hacktivity/overview")
    
    def test_save_and_load_links(self):
        """Test saving and loading links"""
        # Create a test scraper
        class TestScraper(CVEScraper):
            def __init__(self):
                super().__init__()
                self.output_file = "test_output/cve_test.txt"
        
        # Create an instance
        scraper = TestScraper()
        
        # Add some test links
        test_links = [
            "https://hackerone.com/hacktivity/cve_discovery?id=CVE-2021-1234",
            "https://hackerone.com/hacktivity/cve_discovery?id=CVE-2022-5678"
        ]
        scraper.links = test_links
        
        # Save links
        scraper.save_links()
        
        # Create a new instance and load links
        new_scraper = TestScraper()
        new_scraper.load_existing_links()
        
        # Check if links were loaded correctly
        self.assertEqual(new_scraper.links, test_links)

if __name__ == "__main__":
    unittest.main()