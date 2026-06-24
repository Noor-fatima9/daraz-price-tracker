import requests
from bs4 import BeautifulSoup
import smtplib
import csv
import os
from datetime import datetime

DARAZ_PRODUCT_URL = "https://www.daraz.pk/products/apple-iphone-15-i102543219.html"
TARGET_PRICE = 300000
YOUR_EMAIL = "noorfatimanoor931@gmail.com"
YOUR_EMAIL_PASSWORD = "CHANGE_THIS"
RECEIVER_EMAIL = "noorfatimanoor931@gmail.com"

def get_daraz_price():
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        page = requests.get(DARAZ_PRODUCT_URL, headers=headers, timeout=10)
        soup = BeautifulSoup(page.content, "html.parser")
        price_span = soup.find("span", class_="pdp-price")
        if not price_span:
            return None
        price_text = price_span.get_text().replace("Rs.", "").replace(",", "").strip()
        return float(price_text)
    except:
        return None

def send_email_alert(current_price):
    subject = f"Daraz Price Drop! Rs. {current_price}"
    body = f"Price: Rs. {current_price}\nLink: {DARAZ_PRODUCT_URL}"
    message = f"Subject: {subject}\n\n{body}"
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(YOUR_EMAIL, YOUR_EMAIL_PASSWORD)
            server.sendmail(YOUR_EMAIL, RECEIVER_EMAIL, message)
        print("Email sent!")
    except Exception as e:
        print(f"Email failed: {e}")

def save_to_csv(price):
    file_exists = os.path.isfile("daraz_price_history.csv")
    with open("daraz_price_history.csv", "a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Date", "Price_PKR"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M"), price])

if __name__ == "__main__":
    price = get_daraz_price()
    if price:
        print(f"Current Price: Rs. {price}")
        save_to_csv(price)
        if price < TARGET_PRICE:
            send_email_alert(price)
