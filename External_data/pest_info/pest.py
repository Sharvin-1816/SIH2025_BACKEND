from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import requests

BASE_URL = "https://www.nbair.res.in"
MAIN_PAGE = f"{BASE_URL}/pest-alert"

# ----------------------------
# Step 1: Launch Playwright and get page content
# ----------------------------
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(MAIN_PAGE)
    page.wait_for_timeout(5000)  # wait 5 seconds to load content

    html_content = page.content()
    browser.close()

# ----------------------------
# Step 2: Extract all pest alert links
# ----------------------------
soup = BeautifulSoup(html_content, "html.parser")

links = []
for div in soup.find_all("div", class_="views-field views-field-title"):
    span_tag = div.find("span", class_="field-content")
    if span_tag:
        a_tag = span_tag.find("a")
        if a_tag and a_tag.get("href"):
            full_url = urljoin(BASE_URL, a_tag["href"])
            links.append(full_url)

print(f"Extracted {len(links)} links from main page.")

# ----------------------------
# Step 3: Function to scrape header and image from each URL
# ----------------------------
def scrape_pest_info(urls):
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for url in urls:
            page.goto(url)
            page.wait_for_timeout(3000)  # wait 3 seconds
            soup = BeautifulSoup(page.content(), "html.parser")

            # Extract header
            header_span = soup.select_one("h1.page-header span")
            title = header_span.text.strip() if header_span else None

            # Extract image src
            img_tag = soup.select_one(
                "div.field.field--name-field-pest-picture div.field--item img"
            )
            img_src = urljoin(BASE_URL, img_tag["src"]) if img_tag and img_tag.get("src") else None

            results.append({
                "url": url,
                "title": title,
                "image_src": img_src
            })

        browser.close()

    return results

data = scrape_pest_info(links)

# ----------------------------
# Step 4: Function to download images
# ----------------------------
def download_images(data, folder="pest_images"):
    if not os.path.exists(folder):
        os.makedirs(folder)

    for item in data:
        img_url = item.get("image_src")
        title = item.get("title", "unknown").replace("/", "").replace("\\", "")

        if img_url:
            try:
                response = requests.get(img_url, stream=True)
                if response.status_code == 200:
                    file_ext = os.path.splitext(img_url)[1] or ".jpg"
                    file_path = os.path.join(folder, f"{title}{file_ext}")

                    with open(file_path, "wb") as f:
                        for chunk in response.iter_content(1024):
                            f.write(chunk)

                    print(f"Downloaded: {file_path}")
                else:
                    print(f"Failed to download {img_url}, status: {response.status_code}")
            except Exception as e:
                print(f"Error downloading {img_url}: {e}")
        else:
            print(f"No image URL for {title}")

# ----------------------------
# Step 5: Download images
# ----------------------------
download_images(data, folder="pest_alert_images")

# ----------------------------
# Step 6: Print results
# ----------------------------
for item in data:
    print(item)