from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
DATA_PATH = "data/shl_assessments.json"
VEC_PATH = "data/vectors.index"

assessments = []
vectors = []


def load_existing_data():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def load_data_and_update_index():
    global assessments, vectors
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(CATALOG_URL)

    os.makedirs("data", exist_ok=True)

    assessments = load_existing_data()
    vectors = []

    scraped_names = {a['name'] for a in assessments}
    page_count = 0

    while True:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        rows = soup.find_all("tr", attrs={"data-course-id": True})

        new_items = 0
        old_first_name = soup.find("td", class_="custom__table-heading__title").text.strip()

        for row in rows:
            try:
                link_tag = row.find("td", class_="custom__table-heading__title").find("a")
                name = link_tag.text.strip()
                if name in scraped_names:
                    continue

                relative_url = link_tag["href"]
                full_url = BASE_URL + relative_url

                driver.get(full_url)
                time.sleep(2)
                detail_soup = BeautifulSoup(driver.page_source, "html.parser")

                description_elem = detail_soup.find("div", class_="text__content")
                description = description_elem.get_text(separator=" ").strip() if description_elem else name

                duration = "Unknown"
                for p in detail_soup.find_all("p"):
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
                scraped_names.add(name)

                print(f"✅ {name}")
                driver.back()
                time.sleep(1)

                new_items += 1
                if new_items % 5 == 0:
                    with open(DATA_PATH, "w", encoding="utf-8") as f:
                        json.dump(assessments, f, indent=2, ensure_ascii=False)
                    print("📏 Saved progress after 5 items")

            except Exception as e:
                print(f"❌ Error on item: {e}")
                driver.back()

        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "pagination__arrow"))
            )

            driver.execute_script("""
                const el = document.querySelector('.locale-switcher');
                if (el) el.style.display = 'none';
            """)
            driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", next_button)

            WebDriverWait(driver, 10).until(
                lambda d: old_first_name != BeautifulSoup(d.page_source, 'html.parser')
                .find("td", class_="custom__table-heading__title").text.strip()
            )
            page_count += 1
            time.sleep(2)

        except Exception as e:
            print(f"❌ Pagination stopped: {e}")
            break

    driver.quit()

    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(assessments, f, indent=2, ensure_ascii=False)

    if vectors:
        X = np.array(vectors).astype("float32")
        index = faiss.IndexFlatL2(X.shape[1])
        index.add(X)
        faiss.write_index(index, VEC_PATH)

    print(f"✅ Finished scraping {len(assessments)} assessments!")
