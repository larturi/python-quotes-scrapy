# Scraping Quotes
Recorre el sitio http://quotes.toscrape.com y genera la lista de citas

# Execution:
```
pipenv shell

pipenv install

cd quotes_scraper

scrapy crawl quotes -o quotes.json
scrapy crawl quotes -o quotes.csv

```
