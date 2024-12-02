from bs4 import BeautifulSoup as BS
import re
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from search_index import d1_index


options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument('--disable-web-security')
options.add_argument('--disable-dev-shm-usage')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--enable-javascript")
driver = webdriver.Chrome(options=options)

url_base = "https://domicilios.tiendasd1.com/ca/"
database_products = {}





for _ in d1_index.index:
    url = url_base + _
    driver.get(url)
    time.sleep(6)
    html = driver.page_source
    webpg = BS(html, 'html.parser')

    products = webpg.findAll("div", {"class": "card-product-vertical"})
    for prod in products:
        children = prod.findAll("p" , recursive=True)
        image = prod.find("img").get("src") if prod.find("img") else "No image found"
        print(image)
        name = children[1].text
        price = children[0].text.strip().replace(' ', '').replace('$', '').replace('.', '').strip()
        quantity = children[2].text
        store = "D1"
        database_products[name] = price, quantity, store, image

driver.quit()

print("D1 web scraping finished..")
df = pd.DataFrame(
    [(name, price, quantity, store, image) for name, (price, quantity, store, image) in database_products.items()],
    columns=['Product Name', 'Price', 'Quantity', 'Store', 'Image']
)

output_file = "Data/d1Products.csv"
df.to_csv(output_file, index=False)
print(f"Data has been written to {output_file}")


