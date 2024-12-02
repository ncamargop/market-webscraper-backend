import time
from bs4 import BeautifulSoup as BS
import requests
import search_index.rappi_index as rappi_index
import pandas as pd


url_base="https://www.rappi.com.co/tiendas/900103835-turbo/"

database_products = {}

headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
})

for _ in rappi_index.sites:
    url = url_base + _

    webpg = requests.get(url, headers=headers)
    time.sleep(6)
    doc = BS(webpg.text, "html.parser")
    prod_container = doc.find_all('div', class_ = "sc-rBLzX gNlmsq")


    for product in prod_container:
        name = product.find("img", alt=True)["alt"]
        price = product.find("span", {"data-qa": "product-price"}).text.strip().replace(' ', '').replace('$', '').replace('.', '').strip()
        quantity = product.find("span", {"data-qa": "product-description"}).text.strip()
        image = product.find_all("img", alt=True)[1]["src"]
        print(image)
        #discount = product.find("span", {"data-qa": "product-discount"})
        #if(discount):
            #discount = discount.text.strip()
        #else:
            #discount = 0

        store = "Rappi"
        database_products[name] = price, quantity, store, image  #, discount



print("Rappi web scraping done..")
df = pd.DataFrame(
    [(name, price, quantity, store, image) for name, (price, quantity, store, image) in database_products.items()],
    columns=['Product Name', 'Price', 'Quantity', 'Store', 'Image']#, 'Discount']
)


output_file = "Data/rappiProducts.csv"
df.to_csv(output_file, index=False)
print(f"Data has been written to {output_file}")

print("Exporting to mySQL..")


