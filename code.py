import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def scrape_crypto_prices():
    url = "https://coincodex.com/"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

    soup = BeautifulSoup(response.text, "html.parser")

    # Selecting the main coin table rows
    rows = soup.select("table tbody tr")

    crypto_list = []

    for row in rows[:10]:  # Top 10 coins
        try:
            name = row.select_one("td.cc-ticker a").text.strip()
            price = row.select_one("td.cc-price").text.strip()
            change_24h = row.select_one("td.cc-change-24h").text.strip()
            market_cap = row.select_one("td.cc-marketcap").text.strip()

            crypto_list.append({
                "Coin Name": name,
                "Price": price,
                "24h Change": change_24h,
                "Market Cap": market_cap,
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

        except:
            continue

    return crypto_list


def save_to_csv(data):
    df = pd.DataFrame(data)
    df.to_csv("crypto_prices_webscraped.csv", index=False)
    print("✔ Data saved to crypto_prices_webscraped.csv")


if __name__ == "__main__":
    print("Scraping cryptocurrency prices...\n")

    data = scrape_crypto_prices()

    for d in data:
        print(d)

    save_to_csv(data)

    print("\n🟩 Web Scraping Completed Successfully!")
