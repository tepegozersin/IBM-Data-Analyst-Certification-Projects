from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import time
import pandas as pd
import matplotlib.pyplot as plt

# Selenium başlat
driver = webdriver.Chrome()
driver.get("https://books.toscrape.com/")
time.sleep(1)

titles = []
prices = []
availabilities = []

while True:
    books = driver.find_elements(By.CLASS_NAME, "product_pod")

    for book in books:
        title = book.find_element(By.TAG_NAME, "h3").text
        price = book.find_element(By.CLASS_NAME, "price_color").text
        availability = book.find_element(By.CLASS_NAME, "availability").text.strip()

        titles.append(title)
        prices.append(float(price.replace("£", "")))
        availabilities.append(availability)

    # Sonraki sayfa varsa git, yoksa kır
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, "li.next > a")
        next_button.click()
        time.sleep(1)
    except:
        break

driver.quit()

# CSV'ye yaz
with open("C:/Users/tepeg/Desktop/Scraping_Analysis/books_paginated.csv", mode="w", encoding="utf-8-sig", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Price", "Availability"])
    for i in range(len(titles)):
        writer.writerow([titles[i], prices[i], availabilities[i]])

# Analiz ve grafik
df = pd.read_csv("C:/Users/tepeg/Desktop/Scraping_Analysis/books_paginated.csv")
df_sorted = df.sort_values("Price", ascending=False).head(10)

plt.figure(figsize=(12, 6))
plt.bar(df_sorted["Title"], df_sorted["Price"], color="mediumpurple")
plt.title("Top 10 Book Prices (All Pages)")
plt.xlabel("Book Title")
plt.ylabel("Price (£)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("C:/Users/tepeg/Desktop/Scraping_Analysis/book_prices_paginated.png")
