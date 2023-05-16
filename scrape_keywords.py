import argparse
import json
import os
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

SLEEP_TIME = 1
USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/Chrome/84.0.4147.135 Safari/537.36"  # NOQA

ICON_FILE_PATH = "data/icons.csv"
OUTPUT_CSV_FILE_PATH = "data/keywords.csv"

parser = argparse.ArgumentParser()
parser.add_argument(
    "--prefix",
    type=str,
    required=True,
    help="prefix for the image link",
)
parser.add_argument(
    "--suffix",
    type=str,
    default=".png",
    help="suffix for the image link",
)
args = parser.parse_args()

# create file path
execution_dir_path = os.path.dirname(os.path.abspath(__file__))
output_csv_file_path = os.path.join(execution_dir_path, OUTPUT_CSV_FILE_PATH)

# read icons.csv
icons_df = pd.read_csv(os.path.join(execution_dir_path, ICON_FILE_PATH))

headers = {"User-Agent": USER_AGENT}
indexed_keywords = []

for url in icons_df["url"]:
    print(f"scraping {url}")
    time.sleep(SLEEP_TIME)
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Error:", response.status_code)
        break

    soup = BeautifulSoup(response.text, "html.parser")

    script_tag = soup.find("script", {"type": "application/ld+json"})
    data = json.loads(script_tag.string)

    index = data["contentUrl"][len(args.prefix) : -len(args.suffix)]
    indexed_keywords.append((index, data["keywords"]))

# create DataFrame and save csv
keywords_df = pd.DataFrame.from_dict(
    dict((index, d) for index, d in indexed_keywords), orient="index"
)
keywords_df.columns = [f"keywords{column}" for column in keywords_df.columns]
keywords_df.to_csv(output_csv_file_path)
