import argparse
import os
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

OUTPUT_CSV_FILE_PATH = "data/icons.csv"
COLLECTION_ICON_FILE_PATH = "data/collection_icons.csv"
SLEEP_TIME = 1
TIME_OUT = 10
XPATH = "//button[contains(text(), 'Load Next 200 Icons')]"

parser = argparse.ArgumentParser()
parser.add_argument(
    "--url",
    type=str,
    required=True,
    help="URL of the website to scrape",
)
args = parser.parse_args()

# create file path
execution_dir_path = os.path.dirname(os.path.abspath(__file__))
output_csv_file_path = os.path.join(execution_dir_path, OUTPUT_CSV_FILE_PATH)

# read collection_icon.csv
collection_icon_df = pd.read_csv(
    os.path.join(execution_dir_path, COLLECTION_ICON_FILE_PATH)
)

options = ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
# options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=options)

icon_links = []
for _, row in collection_icon_df.iterrows():
    url = row["url"]
    driver.get(url)
    for num_page in range(row["num_pages"]):
        print(f"access page {num_page + 1} of {url}")

        if num_page >= row["num_pages"]:
            break

        wait = WebDriverWait(driver, 10)
        button = wait.until(
            expected_conditions.element_to_be_clickable((By.XPATH, XPATH))
        )

        driver.execute_script("arguments[0].click();", button)
        driver.implicitly_wait(TIME_OUT)

        time.sleep(SLEEP_TIME)

    print("parsing html")
    for link in driver.find_elements(By.TAG_NAME, "a"):
        href = link.get_attribute("href")
        if href and href.startswith(args.url):
            icon_links.append(href)

# set DataFrame
print("exporting DataFrame to csv")
icons_df = pd.DataFrame(icon_links, columns=["url"])
icons_df.to_csv(output_csv_file_path, index=False)

driver.quit()
