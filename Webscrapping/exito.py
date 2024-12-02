import re
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as BS
import search_index.exito_index as exito_index

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument('--disable-web-security')
options.add_argument('--headless') 
options.add_argument('--disable-gpu')  
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=options)

url_base = "https://www.exito.com/"
database_products = {}

for category in exito_index.index:
    page = 1
    while page < 5:
        url = url_base + category + "?page=" + str(page)
        driver.get(url)
        time.sleep(6)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.productCard_productInfo__yn2lK'))
            )
        except Exception as e:
            print(f"Error loading page..")
            break  

        html = driver.page_source
        webpg = BS(html, 'html.parser')
        products = webpg.select('div.productCard_contentInfo__CBBA7')

        if not products:  
            break

        for product in products:
            img_tag = product.select('div.styles_productCardImage__RBIdi img')
            image = img_tag[1]['src'] if len(img_tag) > 1 else "No image found"
            print(image)

            name = product.select_one('p.styles_name__qQJiK').text.strip()
            price = product.select_one('p.ProductPrice_container__price__XmMWA').text.strip().replace(' ', '').replace('$', '').replace('.', '').strip()
            quantity = 1  
            store = "Exito"

            database_products[name] = price, quantity, store, image

        page += 1

driver.quit()

print("Exito web scraping finished..")
df = pd.DataFrame(
    [(name, price, quantity, store, image) for name, (price, quantity, store, image) in database_products.items()],
    columns=['Product Name', 'Price', 'Quantity', 'Store', 'Image']  
)

output_file = "Data/exitoProducts.csv"
df.to_csv(output_file, index=False)
print(f"Data has been written to {output_file}")
