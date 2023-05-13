import argparse
import os

import pandas as pd

"""
Increase the number of pages for this link.
"""

FILE_PATH = "data/collection_icon.csv"

parser = argparse.ArgumentParser()
parser.add_argument(
    "--url",
    type=str,
    required=True,
)
parser.add_argument(
    "--pages",
    type=int,
    default=1,
    help="number of pages for this link",
)
args = parser.parse_args()

# create file path
execution_dir_path = os.path.dirname(os.path.abspath(__file__))
csv_file_path = os.path.join(execution_dir_path, FILE_PATH)
csv_dir_path = os.path.join(execution_dir_path, os.path.dirname(FILE_PATH))

if not os.path.exists(csv_dir_path):
    os.mkdir(csv_dir_path)

# write urls to csv
urls = [f"{args.url}?p={i + 1}" for i in range(args.pages)]
url_df = pd.DataFrame(urls, columns=["url"])
url_df.to_csv(csv_file_path, index=False)
