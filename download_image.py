import os
import time

import pandas as pd
import requests

KEYWORDS_CSV_PATH = "data/keywords.csv"
PREFIX = "https://..."
SUFFIX = ".png"
IMAGES_DIRECTORY = "images"
SLEEP_TIME = 1


def download_image(url: str, save_file_path: str) -> None:
    print(f"downloading {url}")
    response = requests.get(url)

    if response.status_code == 200:
        with open(save_file_path, "wb") as f:
            f.write(response.content)
    else:
        print(f"Unable to download image: {response.status_code}")


if __name__ == "__main__":
    keywords = pd.read_csv(KEYWORDS_CSV_PATH, index_col=0)
    for index in keywords.index:
        url = f"{PREFIX}{index}{SUFFIX}"
        save_filename = f"{index}{SUFFIX}"
        download_image(url, os.path.join(IMAGES_DIRECTORY, save_filename))
        time.sleep(SLEEP_TIME)
