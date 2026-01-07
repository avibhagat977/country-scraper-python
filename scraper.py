import requests
from bs4 import BeautifulSoup

url = "http://www.scrapethissite.com/pages/simple/"


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

        data.append([name, capital, population, area])

    return data

if __name__ == "__main__":
    countries = scrape_countries()
    print(f"Scraped {len(countries)} countries")