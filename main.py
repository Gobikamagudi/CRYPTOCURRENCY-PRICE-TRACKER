from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
from datetime import datetime


#  Function to save website screenshot
def save_website_image(driver):
    image_name = f"livecoinwatch_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    driver.save_screenshot(image_name)
    print(f"✔ Website image saved as {image_name}")


def scrape_crypto_selenium():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    url = "https://www.livecoinwatch.com/"
    driver.get(url)

    time.sleep(5)
    save_website_image(driver)

    crypto_data = []
    rows = driver.find_elements(By.XPATH, "//table/tbody/tr")

    for row in rows[:10]:  # Top 10 coins
        try:
            name = row.find_element(By.XPATH, ".//td[2]//a").text
            price = row.find_element(By.XPATH, ".//td[3]").text
            change_24h = row.find_element(By.XPATH, ".//td[5]").text
            market_cap = row.find_element(By.XPATH, ".//td[8]").text

            crypto_data.append({
                "Coin Name": name,
                "Price": price,
                "24h Change": change_24h,
                "Market Cap": market_cap,
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        except:
            continue

    driver.quit()
    return crypto_data


def save_to_csv(data):
    df = pd.DataFrame(data)
    df.to_csv("crypto_prices_selenium.csv", index=False)
    print("✔ Data saved to crypto_prices_selenium.csv")


if __name__ == "__main__":
    print("🔍 Scraping Crypto Prices Using Selenium...\n")

    data = scrape_crypto_selenium()

    for d in data:
        print(d)

    save_to_csv(data)

    print("\n Selenium Web Scraping Completed Successfully!")
