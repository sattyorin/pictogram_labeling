import argparse
import os
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By

SAVE_CSV_FILE_PATH = "data/icons.csv"
COLLECTION_ICON_FILE_PATH = "data/collection_icon.csv"
SLEEP_TIME = 3

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
csv_file_path = os.path.join(execution_dir_path, SAVE_CSV_FILE_PATH)
save_csv_dir_path = os.path.join(
    execution_dir_path, os.path.dirname(SAVE_CSV_FILE_PATH)
)

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
for url in collection_icon_df["url"]:
    driver.get(url)
    time.sleep(SLEEP_TIME)
    print("sleep")

    for link in driver.find_elements(By.TAG_NAME, "a"):
        href = link.get_attribute("href")
        if href and href.startswith(args.url):
            icon_links.append(href)

icons_df = pd.DataFrame(icon_links, columns=["url"])
icons_df.to_csv(csv_file_path, index=False)

driver.quit()
