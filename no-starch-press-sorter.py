import requests
from bs4 import BeautifulSoup, NavigableString
from urllib.parse import urljoin

# TO-DO: automate topic retrieval from root website
BASE_URL = "https://nostarch.com"
CATALOG_RESOURCE = "/catalog"
TOPIC = "/programming"
URL = BASE_URL + CATALOG_RESOURCE + TOPIC

def main():
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    scraped_products = soup.find_all("div", {"class": "product-info-wrapper"})

    # empty lists, to be populated programmatically
    product_titles = []
    product_subtitles = []
    product_links = []
    product_authors = []
    product_published_dates = []
    
    for product in scraped_products:
        product_titles.append(product.find_next("div", {"class": "product-title"}).a.text)
        product_subtitles.append(product.find_next("div", {"class": "product-subtitle"}).text)
        product_links.append(urljoin(BASE_URL, product.find_next("div", {"class": "product-title"}).a['href']))
        product_authors.append(product.find_next("div", {"class": "product-author"}).text)

        # work-around for getting the unwrapped date for a given product
        for child in product:
            if child.name != 'span' and child.name != 'div':
                if child.text.strip() != "":
                    product_published_dates.append(child.text.strip())

    products = zip(product_titles,
                   product_subtitles,
                   product_links,
                   product_published_dates,
                   product_authors)

if __name__ == "__main__":
    main()
