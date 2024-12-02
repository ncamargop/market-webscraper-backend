import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt


connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='webscraper'
)


query = """
WITH base_prices AS (
    SELECT
        id,
        price AS base_price,
        productName
    FROM products
    WHERE uploaded_at = (SELECT MIN(uploaded_at) FROM products)
),
price_ratios AS (
    SELECT
        pp.uploaded_at,
        pp.id,
        pp.productName,
        pp.price,
        bp.base_price,
        pp.price / bp.base_price AS price_ratio
    FROM products pp
    JOIN base_prices bp
        ON pp.productName = bp.productName
)
SELECT
    uploaded_at,
    productName,
    AVG(price_ratio) * 100 AS unweighted_index
FROM price_ratios
GROUP BY uploaded_at, productName
ORDER BY uploaded_at;
"""


df = pd.read_sql(query, connection)

# Clean the productName column 
df['productName'] = df['productName'].fillna('').astype(str).str.strip()

# Group the data by 'uploaded_at' to calculate the overall index for each day
daily_index = df.groupby('uploaded_at')['unweighted_index'].mean().reset_index()
daily_index['uploaded_at'] = pd.to_datetime(daily_index['uploaded_at'])




# Drop table and create the one for the index
cursor = connection.cursor()
drop_table_query = "DROP TABLE IF EXISTS index_prices;"
cursor.execute(drop_table_query)


create_table_query = """
CREATE TABLE index_prices (
    date DATE NOT NULL,
    unweighted_index FLOAT NOT NULL,
    PRIMARY KEY (date)
);
"""
cursor.execute(create_table_query)


insert_query = """
    INSERT INTO index_prices (date, unweighted_index)
    VALUES (%s, %s)
    ON DUPLICATE KEY UPDATE unweighted_index = VALUES(unweighted_index);
"""

for index, row in daily_index.iterrows():
    cursor.execute(insert_query, (row['uploaded_at'].date(), row['unweighted_index']))


connection.commit()

cursor.close()
connection.close()

print("Data uploaded successfully to the index_prices table..")


