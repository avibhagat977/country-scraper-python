import requests
from bs4 import BeautifulSoup
import csv
from pathlib import Path

from database import create_table, insert_data

url = "http://www.scrapethissite.com/pages/simple/"
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
CSV_FILE = DATA_DIR / "countries.csv"


def scrape_countries():
    response = requests.get(url)
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

    return data

def save_to_csv(data):
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Country", "Capital", "Population", "Area"])
        writer.writerows(data)

if __name__ == "__main__":
    countries = scrape_countries()

    save_to_csv(countries)

    # Data integration
    create_table()
    insert_data(countries)

    print(f"Saved {len(countries)} countries to CSV and SQLite DB")