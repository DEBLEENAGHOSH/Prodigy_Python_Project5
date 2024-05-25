import requests
from bs4 import BeautifulSoup
import csv

# URL of the website to scrape
URL = "http://books.toscrape.com/"


# Function to extract product information from a single page
def extract_product_info(soup):
    product_list = []
    articles = soup.find_all('article', class_='product_pod')

    for article in articles:
        name = article.h3.a['title']
        price = article.find('p', class_='price_color').text.strip()
        rating = article.p['class'][1]

        product_list.append({
            'name': name,
            'price': price,
            'rating': rating
        })

    return product_list


# Function to scrape all pages
def scrape_books_to_scrape():
    all_products = []
    page = 1

    while True:
        print(f"Scraping page {page}...")
        response = requests.get(URL + f"catalogue/page-{page}.html")

        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.content, 'html.parser')
        products = extract_product_info(soup)
        all_products.extend(products)

        page += 1

    return all_products


# Function to save the data to a CSV file
def save_to_csv(products, filename):
    keys = products[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(products)


# Main execution
if __name__ == "__main__":
    products = scrape_books_to_scrape()
    save_to_csv(products, 'books_to_scrape_products.csv')
    print("Scraping complete. Data saved to 'books_to_scrape_products.csv'.")

