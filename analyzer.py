import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from pathlib import Path

DB_FILE = Path("data/countries.db")

def analyze_data():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql("SELECT * FROM countries", conn)
    conn.close()

    print("\nTop 10 Most Populated Countries:")
    print(df.sort_values("population", ascending=False).head(10)[["country", "population"]])

    print("\nAverage Population:", int(df["population"].mean()))
    print("Average Area:", round(df["area"].mean(), 2))

    plot_population(df)
    plot_area(df)


def plot_population(df):
    top = df.sort_values("population", ascending=False).head(10)

    plt.figure(figsize=(10,6))
    plt.bar(top["country"], top["population"], color="skyblue")
    plt.xticks(rotation=45, ha="right")
    plt.title("Top 10 Most Populated Countries")
    plt.tight_layout()
    plt.savefig("data/top_population.png")
    plt.close()


def plot_area(df):
    top = df.sort_values("area", ascending=False).head(10)

    plt.figure(figsize=(10,6))
    plt.bar(top["country"], top["area"], color="salmon")
    plt.xticks(rotation=45, ha="right")
    plt.title("Top 10 Largest Countries by Area")
    plt.tight_layout()
    plt.savefig("data/top_area.png")
    plt.close()


if __name__=="__main__":
    analyze_data()