# Scraping Quotes

Recorre el sitio <http://quotes.toscrape.com> y genera la lista de citas

# Execution

```
pipenv shell

pipenv install

```

#### Generates a json file with title, tags, and quotes:


```
cd quotes_scraper

scrapy crawl quotes

```

#### Generates a json file with title, top 3 of tags, and quotes:


```
cd quotes_scraper

scrapy crawl quotes -a top=3  

```

#### Genetates in csv format:


```
cd quotes_scraper

scrapy crawl quotes -o quotes.csv

```
