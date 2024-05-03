import requests
from bs4 import BeautifulSoup

def get_amazon_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }  # Using a User-Agent to avoid being blocked
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        products = soup.find_all('div', class_='sg-col-inner')

        for product in products:
            title_element = product.find('span', class_='a-size-base-plus a-color-base a-text-normal')
            price_element = product.find('span', class_='a-offscreen')

            if title_element and price_element:
                title = title_element.get_text().strip()
                price = price_element.get_text().strip()

                print("Title:", title)
                print("Price:", price)
                print()
    else:
        print("Failed to fetch page")

url = "https://www.amazon.com/s?k=samsung+g9+monitor&crid=2S74VN5QEJ4XK&sprefix=samsung+g9+monitor%2Caps%2C100&ref=nb_sb_noss_1"
get_amazon_data(url)