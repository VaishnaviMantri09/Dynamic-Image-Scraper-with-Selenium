import os
import re
import time
import requests
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def smart_scroll_to_load_images(driver, max_attempts=100, pause_time=1.5):
    last_img_count = 0
    attempts_without_new_images = 0
    max_no_new_image_attempts = 5

    for attempt in range(max_attempts):
        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(pause_time)

        images = driver.find_elements(By.TAG_NAME, "img")
        current_count = len(images)
        print(f"Scroll attempt {attempt+1}: {current_count} images found.")

        if current_count > last_img_count:
            last_img_count = current_count
            attempts_without_new_images = 0
        else:
            attempts_without_new_images += 1
            if attempts_without_new_images >= max_no_new_image_attempts:
                print("No new images detected after multiple scrolls. Stopping.")
                break


def extract_all_image_urls(driver, base_url, seen):
    ordered_urls = []
    images = driver.find_elements(By.TAG_NAME, "img")

    for img in images:
        for attr in ["src", "data-src"]:
            src = img.get_attribute(attr)
            if src and src not in seen:
                seen.add(src)
                ordered_urls.append(urljoin(base_url, src))

        srcset = img.get_attribute("srcset")
        if srcset:
            candidates = [s.strip().split()[0] for s in srcset.split(',') if s.strip()]
            if candidates:
                high_res = urljoin(base_url, candidates[-1])
                if high_res not in seen:
                    seen.add(high_res)
                    ordered_urls.append(high_res)

    return ordered_urls

def extract_background_images(driver, base_url, seen):
    urls = []
    elements = driver.find_elements(By.XPATH, '//*[@style]')
    for el in elements:
        style = el.get_attribute("style")
        matches = re.findall(r'url\(["\']?(.*?)["\']?\)', style)
        for match in matches:
            full_url = urljoin(base_url, match)
            if full_url not in seen:
                seen.add(full_url)
                urls.append(full_url)
    return urls

def download_images_dynamic(url, folder="downloaded_images"):
    if not os.path.exists(folder):
        os.makedirs(folder)

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)

    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "img")))

    smart_scroll_to_load_images(driver, max_attempts=100, pause_time=1.5)
    
    time.sleep(8)
    seen = set()
    img_urls = extract_all_image_urls(driver, url, seen)
    bg_urls = extract_background_images(driver, url, seen)
    all_image_urls = img_urls + bg_urls
    print(f"Found {len(all_image_urls)} total images.")

    
    for idx, img_url in enumerate(all_image_urls):
        try:
            response = requests.get(img_url, timeout=10)
            if response.status_code == 200:
                ext = os.path.splitext(img_url.split("?")[0])[1]
                if not ext or not ext.startswith("."):
                    ext = ".jpg"
                img_name = f"image_{idx+1:03}{ext}"
                with open(os.path.join(folder, img_name), "wb") as f:
                    f.write(response.content)
                print(f"Downloaded {img_name}")
            else:
                print(f"Skipped {img_url} (Status code: {response.status_code})")
        except Exception as e:
            print(f"Failed to download {img_url}: {e}")
            
    driver.quit()

download_images_dynamic("https://new.express.adobe.com/webpage/7R9jXPxVaE1e6")
