from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from app.models.embedder import get_embedding
import json
import time
import numpy as np
import faiss
import os

BASE_URL = "https://www.shl.com"
CATALOG_URL = "https://www.shl.com/solutions/products/product-catalog/"

def scrape_catalog():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get(CATALOG_URL)

    assessments = []
    vectors = []

    while True:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        rows = soup.find_all("tr", attrs={"data-course-id": True})

        for row in rows:
            try:
                link_tag = row.find("td", class_="custom__table-heading__title").find("a")
                name = link_tag.text.strip()
                relative_url = link_tag["href"]
                full_url = BASE_URL + relative_url

                # Go to detail page
                driver.get(full_url)
                time.sleep(2)
                detail_soup = BeautifulSoup(driver.page_source, "html.parser")

                # Extract description
                description_elem = detail_soup.find("div", class_="text__content")
                description = description_elem.get_text(separator=" ").strip() if description_elem else name

                # Extract duration
                duration = "Unknown"
                length_labels = detail_soup.find_all("p")
                for p in length_labels:
                    if "completion time" in p.text.lower():
                        duration = p.text.strip().split('=')[-1].strip()
                        break

                full_text = detail_soup.get_text(separator=" ").lower()
                remote_support = "yes" if "remote" in full_text or "online" in full_text else "no"
                adaptive = "yes" if "adaptive" in full_text or "irt" in full_text else "no"

                item = {
                    "name": name,
                    "url": full_url,
                    "type": "Assessment",
                    "description": description,
                    "duration": duration,
                    "remote_support": remote_support.capitalize(),
                    "adaptive": adaptive.capitalize()
                }

                assessments.append(item)
                vectors.append(get_embedding(description))

                print(f"✅ {name}")
                driver.back()

            except Exception as e:
                print(f"❌ Error on item: {e}")
                driver.back()

        # Pagination: click "Next" until it's not available
        try:
            next_button = driver.find_element(By.LINK_TEXT, "Next")
            if "disabled" in next_button.get_attribute("class") or not next_button.is_enabled():
                break
            next_button.click()
            time.sleep(4)
        except NoSuchElementException:
            break

    driver.quit()

    os.makedirs("data", exist_ok=True)
    with open("data/shl_assessments.json", "w", encoding="utf-8") as f:
        json.dump(assessments, f, indent=2, ensure_ascii=False)

    if vectors:
        X = np.array(vectors).astype("float32")
        index = faiss.IndexFlatL2(X.shape[1])
        index.add(X)
        faiss.write_index(index, "data/vectors.index")

    print(f"✅ Scraped and saved {len(assessments)} assessments!")

if __name__ == "__main__":
    scrape_catalog()
