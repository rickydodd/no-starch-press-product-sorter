import requests
from bs4 import BeautifulSoup, NavigableString
from urllib.parse import urljoin

# TO-DO: automate topic retrieval from root website
BASE_URL = "https://nostarch.com"
CATALOG_RESOURCE = "/catalog"
TOPIC = "/programming"
URL = BASE_URL + CATALOG_RESOURCE + TOPIC

MONTHS = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6, "July": 7,
          "August": 8, "September": 9, "October": 10, "November": 11, "December": 12}

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
                    # date takes the form Month Year (example: January 2000), so split on the whitespace
                    # and then append to the product_published_dates list as a tuple of the form (Month, Year)
                    product_published_date = child.text.strip().split()
                    product_published_dates.append((product_published_date[0], product_published_date[1]))

    products = zip(product_titles,
                   product_subtitles,
                   product_links,
                   product_published_dates,
                   product_authors)

    products = sorted(products, key=lambda x: (x[3][1], reversor(MONTHS[x[3][0]])), reverse=True)

class reversor:
    def __init__(self, obj):
        self.obj = obj

    def __eq__(self, other):
        return other.obj == self.obj

    def __lt__(self, other):
        return other.obj < self.obj

if __name__ == "__main__":
    main()
