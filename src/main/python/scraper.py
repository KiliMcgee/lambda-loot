import requests
from bs4 import BeautifulSoup
import time
import random

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    # Add more user-agents as needed
]

def scrape_from_url(url):
    for _ in range(3):  # Try 3 times
        try:
            headers = {
                "User-Agent": random.choice(user_agents)
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                print("Successfully fetched page. Response code: ", response.status_code)
                soup = BeautifulSoup(response.content, 'html.parser')

                # Find the content div
                content_div = soup.find('div', class_='mw-parser-output')

                if content_div:
                    # Find all the headings
                    headings = content_div.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

                    current_section = None
                    for heading in headings:
                        # Exclude the "Contents" section
                        if heading.get('id') == 'toc':
                            continue

                        # Extract heading text
                        heading_text = heading.get_text().strip()

                        # Determine the level of the heading
                        level = int(heading.name[1])

                        # Determine the section
                        if level == 1:
                            print(f"\n{'=' * 60}\n{heading_text}\n{'=' * 60}")
                        elif level == 2:
                            current_section = heading_text
                            print(f"\n{'-' * 30}\n{heading_text}\n{'-' * 30}")
                        else:
                            if current_section:
                                print(f"\n{current_section} - {heading_text}")
                        print()

                break  # Exit the loop if successful
            else:
                print("Failed to fetch page. Response code: ", response.status_code)
                time.sleep(2)  # Wait for a while before retrying

        except Exception as e:
            print("Error:", e)
            time.sleep(2)  # Wait for a while before retrying

urlList = [
    "https://en.wikipedia.org/wiki/Austin,_Texas",
    "https://en.wikipedia.org/wiki/Cardamom",
    "https://en.wikipedia.org/wiki/Keyboard_technology",
    "https://en.wikipedia.org/wiki/Main_Page",
    "https://en.wikipedia.org/wiki/Ultimate_Fighting_Championship",
]
scrape_from_url(random.choice(urlList))
