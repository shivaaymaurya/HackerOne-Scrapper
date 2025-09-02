import time
import re
from scraper_base import BaseHackerOneScraper
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from tqdm import tqdm

class UndisclosedReportsScraper(BaseHackerOneScraper):
    """Scraper for HackerOne undisclosed reports links"""
    
    def __init__(self):
        """Initialize the undisclosed reports scraper"""
        super().__init__("output/undisclosed_links.txt", "Undisclosed Reports")
        self.base_url = "https://hackerone.com/hacktivity/overview"
        self.query_params = "?queryString=disclosed%3Afalse&sortField=latest_disclosable_activity_at&sortDirection=DESC&pageIndex="
        
    def scrape(self):
        """Scrape undisclosed reports links from HackerOne"""
        driver = self.setup_driver()
        try:
            # Start with page 0
            page_index = 0
            has_more_pages = True
            all_page_urls = []
            
            with tqdm(desc="Scraping undisclosed report pages", unit="page") as pbar:
                # Process each page until no more pages are available
                while has_more_pages:
                    # Navigate to the current page
                    current_url = f"{self.base_url}{self.query_params}{page_index}"
                    driver.get(current_url)
                    time.sleep(3)  # Wait for page to load
                    
                    # Check if the page has content
                    has_content = self.check_page_has_content(driver)
                    
                    if has_content:
                        all_page_urls.append(current_url)
                        pbar.set_postfix({"Pages found": len(all_page_urls)})
                        pbar.update(1)
                        page_index += 1
                        
                        # Check if there's a next page
                        has_more_pages = self.check_next_page(driver)
                        
                        # Add a small delay to avoid overloading the server
                        time.sleep(1)
                        
                        # Add a limit to avoid infinite loops
                        if page_index >= 1000:  # Arbitrary limit
                            has_more_pages = False
                            print("Reached maximum page limit")
                    else:
                        has_more_pages = False
                        print(f"No more content found on page {page_index}")
            
            # Save all page URLs
            total_pages = len(all_page_urls)
            print(f"Found a total of {total_pages} pages of undisclosed reports")
            
            with tqdm(total=total_pages, desc="Generating undisclosed report page links", unit="link") as pbar:
                for i, url in enumerate(all_page_urls):
                    self.links.append(url)
                    pbar.update(1)
                    pbar.set_postfix({"Current page": i + 1})
                
        except Exception as e:
            print(f"Error during undisclosed reports scraping: {e}")
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
    
    def check_page_has_content(self, driver):
        """Check if the page has report content"""
        max_retries = 3
        retries = 0
        
        while retries < max_retries:
            try:
                # Wait for the page to load
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                
                # Look for program links or report elements
                program_links = driver.find_elements(By.CSS_SELECTOR, "a[href^='https://hackerone.com/']")
                
                # Filter out navigation links
                content_links = [link for link in program_links if not any(x in link.get_attribute("href") for x in [
                    "/hacktivity/", "/opportunities/", "/directory/", "/leaderboard", "/users/sign_in"
                ])]
                
                # Check for error messages
                error_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Error')]")
                if error_elements and len(error_elements) > 0:
                    print("Error message found on page, retrying...")
                    driver.refresh()
                    retries += 1
                    time.sleep(3)
                    continue
                
                return len(content_links) > 0
                
            except (TimeoutException, StaleElementReferenceException) as e:
                retries += 1
                print(f"Retry {retries}/{max_retries} due to: {e}")
                time.sleep(2)
            except Exception as e:
                print(f"Error checking page content: {e}")
                break
                
        return False

if __name__ == "__main__":
    scraper = UndisclosedReportsScraper()
    scraper.run()