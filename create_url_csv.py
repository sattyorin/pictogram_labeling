import pandas as pd

page_num = 1
url = "https://....."

urls = [f"{url}?p={i + 1}" for i in range(page_num)]
url_df = pd.DataFrame(urls, columns=["url"])
url_df.to_csv("collection_icon.csv", index=False)
