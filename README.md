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
cp data/collection_icons_example.csv data/collection_icons.csv
```
modify collection_icons.csv

```
python3 scrape_links.py --url https://...
```

```
python3 scrape_keywords.py --prefix https://... --suffix .png
python3 download_images.py --prefix https://... --suffix .png
```
