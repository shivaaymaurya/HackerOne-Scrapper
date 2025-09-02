import time
import re
from scraper_base import BaseHackerOneScraper
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from tqdm import tqdm

class CWEScraper(BaseHackerOneScraper):
    """Scraper for HackerOne CWE links"""
    
    def __init__(self):
        """Initialize the CWE scraper"""
        super().__init__("output/cwe_links.txt", "CWE")
        self.base_url = "https://hackerone.com/hacktivity/cwe_discovery"
        
    def scrape(self):
        """Scrape CWE links from HackerOne"""
        driver = self.setup_driver()
        try:
            # Navigate to the CWE discovery page
            driver.get(self.base_url)
            time.sleep(3)  # Wait for page to load
            
            # Extract all CWE IDs
            all_cwe_ids = []
            page = 0
            has_next_page = True
            
            with tqdm(desc="Scraping CWE pages", unit="page") as pbar:
                while has_next_page:
                    # Extract CWE IDs from the current page
                    cwe_ids = self.extract_cwe_ids(driver)
                    all_cwe_ids.extend(cwe_ids)
                    
                    pbar.set_postfix({"CWEs found": len(all_cwe_ids)})
                    pbar.update(1)
                    
                    # Check if there's a next page
                    has_next_page = self.go_to_next_page(driver)
                    page += 1
                    
                    # Add a small delay to avoid overloading the server
                    time.sleep(1)
            
            # Generate links for all CWE IDs
            total_cwes = len(all_cwe_ids)
            print(f"Found a total of {total_cwes} CWEs")
            
            with tqdm(total=total_cwes, desc="Generating CWE links", unit="link") as pbar:
                for i, cwe_id in enumerate(all_cwe_ids):
                    # Convert CWE-79 to cwe-79 (lowercase) for the URL
                    cwe_id_lower = cwe_id.lower()
                    link = f"https://hackerone.com/hacktivity/cwe_discovery?id={cwe_id_lower}"
                    self.links.append(link)
                    pbar.update(1)
                    pbar.set_postfix({"Current": cwe_id})
                
        except Exception as e:
            print(f"Error during CWE scraping: {e}")
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
    
    def extract_cwe_ids(self, driver):
        """Extract CWE IDs from the current page"""
        cwe_ids = []
        max_retries = 3
        retries = 0
        
        while retries < max_retries:
            try:
                # Wait for the table to load
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "table"))
                )
                
                # Find all rows in the CWE table
                rows = driver.find_elements(By.CSS_SELECTOR, "tr")
                
                for row in rows:
                    try:
                        # Extract the CWE ID from the row
                        cells = row.find_elements(By.CSS_SELECTOR, "td")
                        if cells:
                            cwe_text = cells[0].text.strip()
                            # Use regex to extract CWE ID
                            match = re.search(r'(CWE-\d+)', cwe_text)
                            if match:
                                cwe_id = match.group(1)
                                cwe_ids.append(cwe_id)
                    except (NoSuchElementException, StaleElementReferenceException):
                        continue
                
                # If we got here without exceptions, break the retry loop
                break
                
            except (TimeoutException, StaleElementReferenceException) as e:
                retries += 1
                print(f"Retry {retries}/{max_retries} due to: {e}")
                time.sleep(2)
            except Exception as e:
                print(f"Error extracting CWE IDs: {e}")
                break
                
        return cwe_ids

if __name__ == "__main__":
    scraper = CWEScraper()
    scraper.run()