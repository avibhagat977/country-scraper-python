import requests
from bs4 import BeautifulSoup
import csv
from pathlib import Path
from database import create_table, insert_data
import logging

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

url = "http://www.scrapethissite.com/pages/simple/"
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
CSV_FILE = DATA_DIR / "countries.csv"

logging.basicConfig(
    filename=LOG_DIR / "scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def scrape_countries():
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        logging.info("Website accessed successfully")
        
        soup = BeautifulSoup(response.text, "html.parser")
        countries = soup.select(".country")
        data = []

        for country in countries:
            name = country.select_one(".country-name").text.strip()
            capital = country.select_one(".country-capital").text.strip()
            population = country.select_one(".country-population").text.strip().replace(",", "")
            area = country.select_one(".country-area").text.strip().replace(",", "")

            # Convert types for DB
            population = int(population)
            area = float(area)

            data.append([name, capital, population, area])
    
        logging.info(f"Scraped {len(data)} countries")
        return data

    except Exception as e:
        logging.error(f"Scraping failed: {e}")
        return []

def save_to_csv(data):
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Country", "Capital", "Population", "Area"])
        writer.writerows(data)

if __name__ == "__main__":
    countries = scrape_countries()

    if countries:
        save_to_csv(countries)

        # Data integration
        create_table()
        insert_data(countries)

        print(f"Saved {len(countries)} countries to CSV and SQLite DB")
    else:
        print("No data scraped. Check logs")