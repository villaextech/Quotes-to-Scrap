import requests
import csv
from bs4 import BeautifulSoup

csv_file = 'scraped_quotes.csv'
csv_header = ['qoute', 'author', 'tags']

def scrape_quotes(url):
    response = requests.get(url)
    #print(response.status_code)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    quote_elements = soup.find_all('div', class_='quote')
    #print(quote_elements)
    scraped_data = [] 

    #print(len(quote_elements))

    for element in quote_elements:
        quote = element.find('span', class_='text').text
        author = element.find('small', class_='author').text
        tag_elements = element.find('div', class_='tags').find_all('a', class_='tag')
        tags = [tag.text for tag in tag_elements]

        data = {
            "qoute": quote,
            "author": author,
            "tags": ', '.join(tags)
        }
        print(data)
        scraped_data.append(data)

    with open(csv_file, 'a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=csv_header)
        
        # If the file is empty, write the header
        if file.tell() == 0:
            writer.writeheader()

        writer.writerows(scraped_data)

# Iterate through pages
for page_num in range(1, 11):
    url = f"https://quotes.toscrape.com/page/{page_num}/"
    print(f"Scraping page {page_num}...")
    scrape_quotes(url)
    #cprint(scrape_quotes)
print(f'Data scraped and saved to {csv_file}')