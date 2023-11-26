import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

def extract_links(base_url, soup):
    links = []
    for a_tag in soup.find_all('a', href=True):
        title = a_tag.get_text().strip()
        link = a_tag['href']
        full_url = urljoin(base_url, link)
        links.append({'title': title, 'url': full_url})
    return links

def extract_main_content(base_url):
    page = requests.get(base_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Ici, vous devez utiliser le sélecteur approprié pour la div qui contient les liens
    main_div = soup.find('div', class_='css-175oi2r r-1yzf0co r-1sc18lr')
    if main_div:
        return extract_links(base_url, main_div)
    else:
        return []

def main():
    base_url = "https://docs.bscscan.com"
    categories_data = extract_main_content(base_url)

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(categories_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
