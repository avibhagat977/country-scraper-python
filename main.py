from scraper import scrape_countries, save_to_csv
from database import create_table, insert_data
from analyzer import analyze_data
from pathlib import Path

Path("logs").mkdir(exist_ok=True)

def main():
    print("Scraping country data...")
    data = scrape_countries()
    if not data:
        print("No data scraped. Check logs.")
        return
    
    save_to_csv(data)
    create_table()
    insert_data(data)

    print("Analyzing data...")
    analyze_data()
    print("Done")

if __name__=="__main__":
    main()