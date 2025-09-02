import time
import re
from scraper_base import BaseHackerOneScraper
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from tqdm import tqdm

class CVEScraper(BaseHackerOneScraper):
    """Scraper for HackerOne CVE links"""
    
    def __init__(self):
        """Initialize the CVE scraper"""
        super().__init__("output/cve_links.txt", "CVE")
        self.base_url = "https://hackerone.com/hacktivity/cve_discovery"
        
    def scrape(self):
        """Scrape CVE links from HackerOne"""
        driver = self.setup_driver()
        try:
            # Navigate to the CVE discovery page
            driver.get(self.base_url)
            time.sleep(3)  # Wait for page to load
            
            # Extract all CVE IDs
            all_cve_ids = []
            page = 0
            has_next_page = True
            
            with tqdm(desc="Scraping CVE pages", unit="page") as pbar:
                while has_next_page:
                    # Extract CVE IDs from the current page
                    cve_ids = self.extract_cve_ids(driver)
                    all_cve_ids.extend(cve_ids)
                    
                    pbar.set_postfix({"CVEs found": len(all_cve_ids)})
                    pbar.update(1)
                    
                    # Check if there's a next page
                    has_next_page = self.go_to_next_page(driver)
                    page += 1
                    
                    # Add a small delay to avoid overloading the server
                    time.sleep(1)
            
            # Generate links for all CVE IDs
            total_cves = len(all_cve_ids)
            print(f"Found a total of {total_cves} CVEs")
            
            with tqdm(total=total_cves, desc="Generating CVE links", unit="link") as pbar:
                for i, cve_id in enumerate(all_cve_ids):
                    link = f"https://hackerone.com/hacktivity/cve_discovery?id={cve_id}"
                    self.links.append(link)
                    pbar.update(1)
                    pbar.set_postfix({"Current": cve_id})
                
        except Exception as e:
            print(f"Error during CVE scraping: {e}")
        finally:
            driver.quit()
    
    def go_to_next_page(self, driver):
        """Click the next page button if available"""
        try:
            # Find the next page button
            next_button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "pagination-next-page"))
            )
            
            # Check if the button is enabled
            if next_button.is_enabled() and "disabled" not in next_button.get_attribute("class"):
                next_button.click()
                time.sleep(2)  # Wait for page to load
                return True
            else:
                return False
        except (TimeoutException, NoSuchElementException):
            return False
        except Exception as e:
            print(f"Error navigating to next page: {e}")
            return False
    
    def extract_cve_ids(self, driver):
        """Extract CVE IDs from the current page"""
        cve_ids = []
        max_retries = 3
        retries = 0
        
        while retries < max_retries:
            try:
                # Wait for the table to load
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "table"))
                )
                
                # Find all rows in the CVE table
                rows = driver.find_elements(By.CSS_SELECTOR, "tr")
                
                for row in rows:
                    try:
                        # Extract the CVE ID from the row
                        cells = row.find_elements(By.CSS_SELECTOR, "td")
                        if len(cells) >= 2:
                            cve_text = cells[1].text.strip()
                            # Use regex to extract CVE ID
                            match = re.search(r'(CVE-\d{4}-\d+)', cve_text)
                            if match:
                                cve_id = match.group(1)
                                cve_ids.append(cve_id)
                    except (NoSuchElementException, StaleElementReferenceException):
                        continue
                
                # If we got here without exceptions, break the retry loop
                break
                
            except (TimeoutException, StaleElementReferenceException) as e:
                retries += 1
                print(f"Retry {retries}/{max_retries} due to: {e}")
                time.sleep(2)
            except Exception as e:
                print(f"Error extracting CVE IDs: {e}")
                break
                
        return cve_ids

if __name__ == "__main__":
    scraper = CVEScraper()
    scraper.run()