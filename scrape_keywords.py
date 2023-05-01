import json
import os
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

INPUT_FILE_PATH = "icons.csv"
OUTPUT_DIR_PATH = "keywords.csv"
DATA_DIRECTORY = "data"

PREFIX = "https://......"
SUFFIX = ".png"

SLEEP_TIME = 1
USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/Chrome/84.0.4147.135 Safari/537.36"  # NOQA

icons_df = pd.read_csv(os.path.join(DATA_DIRECTORY, INPUT_FILE_PATH))
headers = {"User-Agent": USER_AGENT}
indexed_keywords = []

for url in icons_df["url"]:
    time.sleep(SLEEP_TIME)
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Error:", response.status_code)
        exit()

    soup = BeautifulSoup(response.text, "html.parser")

    script_tag = soup.find("script", {"type": "application/ld+json"})
    data = json.loads(script_tag.string)

    index = data["contentUrl"][len(PREFIX) : -len(SUFFIX)]
    indexed_keywords.append((index, data["keywords"]))

    keywords_df = pd.DataFrame.from_dict(
        dict((index, d) for index, d in indexed_keywords), orient="index"
    )

keywords_df.to_csv(os.path.join(DATA_DIRECTORY, OUTPUT_DIR_PATH))
