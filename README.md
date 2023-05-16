# pictogram_labeling

# setup
```
google-chrome --version
```

```
python -m pip install chromedriver-binary==<google-chrome version>
python -m pip install selenium
```

# create dataset

```
cp data/collection_icon_example.csv data/collection_icon.csv
```
modify collection_icon.csv

```
python3 scrape_links.py --url https://...
```

```
python3 scrape_keywords.py --prefix https://... --suffix .png
python3 download_image.py --prefix https://... --suffix .png
```
