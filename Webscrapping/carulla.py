import re
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as BS
import search_index.carulla_index as carulla_index

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument('--disable-web-security')
options.add_argument('--headless') 
options.add_argument('--disable-gpu')  
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=options)

url_base = "https://www.carulla.com/"
database_products = {}

for category in carulla_index.index:
    page = 1
    while page < 5:
        url = url_base + category + "?page=" + str(page)
        driver.get(url)
        time.sleep(6)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.vtex-search-result-3-x-galleryItem'))
            )
        except Exception as e:
            print(f"Error loading page..")
            break  

        html = driver.page_source
        webpg = BS(html, 'html.parser')
        products = webpg.select('div.vtex-search-result-3-x-galleryItem')

        if not products: 
            break

        for product in products:
            prod = product.select_one('img.vtex-product-summary-2-x-imageNormal')
            price_container = product.select_one('div.exito-vtex-components-4-x-PricePDP span.exito-vtex-components-4-x-currencyContainer')

            if price_container and prod:
                name = prod.get('alt', "No name found")
                price = price_container.text.strip().replace(' ', '').replace('$', '').replace('.', '').strip()
                quantity = re.split(r'(\d+\w*)', name)
                image = prod.get('src', "No image found")  
            else:
                name = "No name found"
                price = 0
                quantity = "Not found"
                image = "No image found" 

            if len(quantity) > 1:
                quantity = quantity[1].strip()
            else:
                quantity = "No quantity found"

            store = "Carulla"
            database_products[name] = price, quantity, store, image 

        page += 1

driver.quit()

print("Carulla web scraping finished..")
df = pd.DataFrame(
    [(name, price, quantity, store, image) for name, (price, quantity, store, image) in database_products.items()],
    columns=['Product Name', 'Price', 'Quantity', 'Store', 'Image']  
)

output_file = "Data/carullaProducts.csv"
df.to_csv(output_file, index=False)
print(f"Data has been written to {output_file}")
