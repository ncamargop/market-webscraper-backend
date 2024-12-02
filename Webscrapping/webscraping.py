import re
import subprocess
import mysql.connector
import csv

scripts = ["carulla.py", "d1.py", "exito.py", "rappi.py"]

for script in scripts:
    subprocess.run(["python", script])

print("All sites web scraping done..")
print("Running data to mySQL..")


bd = mysql.connector.connect(
    user='root',
    password='root',
    host='localhost',
    database='webscraper')

cursor = bd.cursor()


files = ["Data/exitoProducts.csv", "Data/rappiProducts.csv", "Data/carullaProducts.csv", "Data/d1Products.csv"]
for file in files:    
    with open(file, 'r', encoding="UTF-8") as csv_data:
        csv_reader = csv.reader(csv_data)
        next(csv_data)
        for row in csv_reader:
            productName = row[0]
            price = row[1]
            quantity = row[2]
            store = row[3]
            image = row[4]
            cursor.execute(
                    "INSERT INTO products (productName, price, quantity, store, image) VALUES (%s, %s, %s, %s, %s)",
                    (productName, price, quantity, store, image) 
                )
            
            
cursor.execute("DROP TABLE average_products")



cursor.execute("""
                CREATE TABLE average_products AS
                SELECT SUBSTRING_INDEX(productName, ' ', 1) AS product_name, 
                    store,
                    AVG(price) AS average_price, 
                    uploaded_at
                FROM 
                    products
                GROUP BY 
                    product_name, store, uploaded_at"""
    )



bd.commit()
cursor.close()
bd.close()
print("SQL loading done..")


# Get index for graph
subprocess.run(["python", "index500.py"])
print("All done here!")

