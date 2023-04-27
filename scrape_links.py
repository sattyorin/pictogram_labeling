import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By

# import chromedriver_binary  # NOQA

SLEEP_TIME = 3
URL_ICON = "https://......"

collection_icon_df = pd.read_csv("collection_icon.csv")

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
        if href and href.startswith(URL_ICON):
            icon_links.append(href)

icons_df = pd.DataFrame(icon_links, columns=["url"])
icons_df.to_csv("icons.csv", index=False)

driver.quit()
