import csv
import random
import re
import requests
import time
from bs4 import BeautifulSoup

user_agents = [
    # Random user agents in an attempt to disguise scraping traffic
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
]

url_list = [
    "https://en.wikipedia.org/wiki/Austin,_Texas",
    "https://en.wikipedia.org/wiki/Cardamom",
    "https://en.wikipedia.org/wiki/Keyboard_technology",
    "https://en.wikipedia.org/wiki/Denby_Pottery_Company",
    "https://en.wikipedia.org/wiki/Computer_security",
    "https://en.wikipedia.org/wiki/Prusa_i3",
    "https://en.wikipedia.org/wiki/Gross_domestic_product",
    "https://en.wikipedia.org/wiki/Ultimate_Fighting_Championship",
]

excluded_headings = [
    'Bibliography',
    'External links',
    'Further reading',
    'Gallery',
    'Notes',
    'References',
    'See also',
]

def scrape_from_url(url):
    for _ in range(3):  # Try 3 times to accommodate blocked requests
        try:
            headers = {
                "User-Agent": random.choice(user_agents)
            }
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                print("Successfully fetched page {}. Response code: {}".format(url, response.status_code))
                soup = BeautifulSoup(response.content, 'html.parser')

                # Find the content div
                content_div = soup.find('div', id='bodyContent')

                if content_div:
                    # Open CSV file for writing
                    with open('looted.csv', mode='w', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerow(['HEADING', 'LEVEL', 'CONTENT'])

                        # Find all the headings
                        headings = content_div.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

                        for heading in headings:
                            # Extract heading text and remove all [edit] links
                            heading_text = heading.get_text().strip()
                            heading_text = re.sub("\[edit\]", "", heading_text)

                            # Skip excluded headings
                            if heading_text in excluded_headings:
                                continue

                            # Determine the level of the heading
                            level = int(heading.name[1])

                            # Find the next sibling, which is usually a paragraph or a list
                            sibling = heading.find_next_sibling(['p', 'ul', 'ol'])
                            if sibling:
                                # Extract up to 150 characters, stripping unnecessary whitespace
                                text = sibling.get_text()[:150].strip()
                                text = re.sub("[\t\n]+", ", ", text)
                                if len(text) > 147:
                                    text = text[:147] + '...'  # Append ellipsis if more than 147 characters

                                # Write to CSV
                            writer.writerow([heading_text, level, text or 'No sibling text found.'])
                break

            else:
                print("Failed to fetch page. Response code:", response.status_code)
                time.sleep(2)  # Wait for a while before retrying

        except Exception as e:
            print("Encountered error while sending request: ", e)
            time.sleep(2)  # Wait for a while before retrying

scrape_from_url(random.choice(url_list))
