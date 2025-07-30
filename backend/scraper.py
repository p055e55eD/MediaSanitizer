"""
Selenium-based Scraper for MediaSanitizer.
Supports scraping Armenian/English news from CivilNet, Hetq, and generic sites.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

class NewsScraper:
    def __init__(self):
        # Custom rules for supported news sites (add more as needed)
        self.site_rules = {
            "civilnet.am": {
                "title_xpath": "//h1",
                "content_xpath": "//div[contains(@class, 'article-content') or contains(@class, 'content')]"
            },
            "hetq.am": {
                "title_xpath": "//h1",
                "content_xpath": "//div[contains(@class, 'article-content') or contains(@class, 'content')]"
            }
        }
        # Path to your chromedriver.exe (adjust as needed)
        self.chromedriver_path = "./chromedriver.exe"

    def _get_driver(self):
        from selenium.webdriver.chrome.service import Service
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1280,800")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-blink-features=AutomationControlled')
        service = Service(self.chromedriver_path)
        return webdriver.Chrome(service=service, options=options)

    def scrape(self, url):
        domain = self._get_domain(url)
        try:
            driver = self._get_driver()
            driver.get(url)
            time.sleep(2)  # Wait for page to load JS (tune if needed)
        except Exception as e:
            print(f"[Scraper] Failed to load page with Selenium: {e}")
            return None

        result = {
            "domain": domain,
            "title": "",
            "content": ""
        }

        try:
            if domain in self.site_rules:
                # Site-specific logic
                rule = self.site_rules[domain]
                try:
                    # Title
                    title_el = driver.find_element(By.XPATH, rule["title_xpath"])
                    result["title"] = title_el.text.strip()
                except Exception:
                    result["title"] = ""
                try:
                    # Content
                    content_el = driver.find_element(By.XPATH, rule["content_xpath"])
                    paragraphs = content_el.find_elements(By.TAG_NAME, "p")
                    content = "\n".join([p.text for p in paragraphs if p.text.strip()])
                    if not content:
                        content = content_el.text.strip()
                    result["content"] = content
                except Exception:
                    result["content"] = ""
            else:
                # Generic scraping: get all visible <p> tags
                ps = driver.find_elements(By.TAG_NAME, "p")
                content = "\n".join([p.text for p in ps if p.text.strip()])
                result["title"] = driver.title or ""
                result["content"] = content
        except Exception as e:
            print(f"[Scraper] Error while scraping: {e}")
        finally:
            driver.quit()

        if not result["content"]:
            print(f"[Scraper] No content scraped for {url}")
            return None

        return result

    def _get_domain(self, url):
        # Extracts domain like civilnet.am
        try:
            return url.split("//")[1].split("/")[0].replace("www.", "")
        except Exception:
            return "unknown"

# --- Standalone test ---
if __name__ == "__main__":
    test_url = "https://www.civilnet.am/en/news/949827/armenias-ruling-party-proposes-exemption-fee-for-avoiding-military-service/"
    scraper = NewsScraper()
    res = scraper.scrape(test_url)
    print("SCRAPED RESULT:", res)
