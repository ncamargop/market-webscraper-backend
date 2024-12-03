# Colombian Supermarket Price Tracker Backend

This is the backend project for the colombian supermarket price tracker app. It handles the logic for webscraping products from multiple stores in Colombia, processing the data and storing it in a MySQL database, as well as, providing endpoints for fetching the data with the frontend with you can find [here](https://github.com/ncamargop/market-webscraper-frontend.git).



## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Preview](#preview)


## Features

- **Web scraping**: Inside the webscrapping folder, you can optionally run the webscraping.py file to retrieve in real-time data from more than 7500 products available online.
- **API Endpoints**: Provides endpoints for fetching product prices, supermarkets, and price variations over time.
- **Price Change Index**: Calculates the unweighted index for tracking overall price changes across supermarkets.
- **Database Integration**: Stores price data in a MySQL database and supports easy updates and queries.


## Pre-requisites

1. Must have installed MySQL and have a localhost server running. The database schema, configurations, database, tables and testing data is stored [here](https://github.com/ncamargop/market-webscraper-backend/tree/master/Webscrapping/mySQL_db), which you can import into your MySQL (needed for [frontend](https://github.com/ncamargop/market-webscraper-frontend.git) testing and visualization).

2. If needed or desired, you can run the webscraping.py file located [here](https://github.com/ncamargop/market-webscraper-backend/blob/master/Webscrapping/webscraping.py) to retrieve in real-time products information from Rappi, Exito, Carulla, and D1, which is automatically stored into your localhost MySQL server.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ncamargop/market-webscraper-backend.git

2. In the project directory, install dependencies by running:
   ```bash
   pip install -r requirements.txt

3. Run the backend server with:
   ```bash
   python manage.py runserver

4. Visit http://localhost:8000/products to test endpoints.





## Preview

This is the frontend visualization preview, must install and run the frontend server.

![price-tracker1](https://github.com/user-attachments/assets/36a639f9-f256-4713-a3db-0d3bf57485f8)

![price-tracker2](https://github.com/user-attachments/assets/6ce74450-c32b-4ca5-8cc8-6127cad06ea9)

![price-tracker3](https://github.com/user-attachments/assets/4e22c9dd-22ea-4af8-901c-dcc6f8c94929)
