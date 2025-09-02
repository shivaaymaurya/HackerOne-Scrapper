import time
import re
from scraper_base import BaseHackerOneScraper
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from tqdm import tqdm

class DisclosedReportsScraper(BaseHackerOneScraper):
    """Scraper for HackerOne disclosed reports links"""
    
    def __init__(self):
        """Initialize the disclosed reports scraper"""
        super().__init__("output/disclosed_links.txt", "Disclosed Reports")
        self.base_url = "https://hackerone.com/hacktivity/overview"
        self.query_params = "?queryString=disclosed%3Atrue&sortField=latest_disclosable_activity_at&sortDirection=DESC&pageIndex="
        
    def scrape(self):
        """Scrape disclosed reports links from HackerOne"""
        driver = self.setup_driver()
        try:
            # Start with page 0
            page_index = 0
            has_more_pages = True
            all_report_ids = []
            
            with tqdm(desc="Scraping disclosed report pages", unit="page") as pbar:
                # Process each page until no more pages are available
                while has_more_pages:
                    # Navigate to the current page
                    current_url = f"{self.base_url}{self.query_params}{page_index}"
                    driver.get(current_url)
                    time.sleep(3)  # Wait for page to load
                    
                    # Extract report IDs from the current page
                    report_ids = self.extract_report_ids(driver)
                    
                    if report_ids:
                        all_report_ids.extend(report_ids)
                        pbar.set_postfix({"Reports found": len(all_report_ids)})
                        pbar.update(1)
                        page_index += 1
                        
                        # Check if there's a next page
                        has_more_pages = self.check_next_page(driver)
                        
                        # Add a small delay to avoid overloading the server
                        time.sleep(1)
                    else:
                        has_more_pages = False
                        print(f"No more reports found on page {page_index}")
            
            # Generate links for all report IDs
            total_reports = len(all_report_ids)
            print(f"Found a total of {total_reports} disclosed reports")
            
            with tqdm(total=total_reports, desc="Generating disclosed report links", unit="link") as pbar:
                for i, report_id in enumerate(all_report_ids):
                    link = f"https://hackerone.com/reports/{report_id}"
                    self.links.append(link)
                    pbar.update(1)
                    pbar.set_postfix({"Current": report_id})
                
        except Exception as e:
            print(f"Error during disclosed reports scraping: {e}")
        finally:
            driver.quit()
    
    def check_next_page(self, driver):
        """Check if there's a next page button and if it's enabled"""
        try:
            # Find the next page button
            next_button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "pagination-next-page"))
            )
            
            # Check if the button is enabled
            return next_button.is_enabled() and "disabled" not in next_button.get_attribute("class")
        except (TimeoutException, NoSuchElementException):
            return False
        except Exception as e:
            print(f"Error checking next page: {e}")
            return False
    
    def extract_report_ids(self, driver):
        """Extract report IDs from the current page"""
        report_ids = []
        max_retries = 3
        retries = 0
        
        while retries < max_retries:
            try:
                # Wait for the report links to load
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "a[href^='/reports/']"))
                )
                
                # Find all report links on the page
                report_links = driver.find_elements(By.CSS_SELECTOR, "a[href^='/reports/']")
                
                for link in report_links:
                    try:
                        href = link.get_attribute("href")
                        # Extract the report ID from the href
                        match = re.search(r'/reports/(\d+)', href)
                        if match:
                            report_id = match.group(1)
                            report_ids.append(report_id)
                    except Exception:
                        continue
                
                # Remove duplicates
                report_ids = list(set(report_ids))
                
                # If we got here without exceptions, break the retry loop
                break
                
            except (TimeoutException, StaleElementReferenceException) as e:
                retries += 1
                print(f"Retry {retries}/{max_retries} due to: {e}")
                time.sleep(2)
            except Exception as e:
                print(f"Error extracting report IDs: {e}")
                break
                
        return report_ids

if __name__ == "__main__":
    scraper = DisclosedReportsScraper()
    scraper.run()