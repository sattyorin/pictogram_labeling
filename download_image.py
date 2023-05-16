import argparse
import os
import time

import pandas as pd
import requests

KEYWORDS_CSV_PATH = "data/keywords.csv"
IMAGE_DIRECTORY = "images"
SLEEP_TIME = 1

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
images_dir_path = os.path.join(execution_dir_path, IMAGE_DIRECTORY)
if not os.path.exists(images_dir_path):
    print(f"make directory: {images_dir_path}")
    os.mkdir(images_dir_path)

keywords = pd.read_csv(
    os.path.join(execution_dir_path, KEYWORDS_CSV_PATH), index_col=0
)
for index in keywords.index:
    url = f"{args.prefix}{index}{args.suffix}"
    save_filename = f"{index}{args.suffix}"
    print(f"downloading {url} and saving {save_filename}")
    response = requests.get(url)
    if response.status_code == 200:
        with open(os.path.join(images_dir_path, save_filename), "wb") as f:
            f.write(response.content)
    else:
        print(f"Unable to download image: {response.status_code}")
    time.sleep(SLEEP_TIME)
