import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

def extract_category_content(category_url):
    response = requests.get(category_url)
    category_soup = BeautifulSoup(response.content, 'html.parser')

    main_content = category_soup.find('main')
    if main_content:
        content_text = main_content.get_text(separator='\n', strip=True)
    else:
        content_text = "Contenu non trouvé"
    return content_text

def extract_links(base_url, soup, total_links):
    categories = []
    for index, a_tag in enumerate(soup.find_all('a', href=True)):
        title = a_tag.get_text().strip()
        link = a_tag['href']
        full_url = urljoin(base_url, link)

        content_text = extract_category_content(full_url)
        categories.append({
            'title': title,
            'url': full_url,
            'text': content_text
        })

        # Mise à jour manuelle de la barre de progression
        print(f"Traitement des catégories : {index + 1}/{total_links} complété")

    return categories

def extract_main_content(base_url):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    main_div = soup.find('div', class_='css-175oi2r r-1yzf0co r-1sc18lr')
    if main_div:
        all_a_tags = main_div.find_all('a', href=True)
        total_links = len(all_a_tags)
        return extract_links(base_url, main_div, total_links)
    else:
        print("Erreur : Div spécifiée pour les liens introuvable.")
        return []

def main():
    base_url = "https://docs.bscscan.com"  # Remplacez par l'URL réelle
    categories_data = extract_main_content(base_url)

    json_name = '_'.join(base_url.split('//')[1].split('.')[:-1]) + '.json'

    with open(json_name, 'w', encoding='utf-8') as f:
        json.dump(categories_data, f, ensure_ascii=False, indent=4)
    print(f"Extraction terminée. Données enregistrées dans {json_name}.")

if __name__ == "__main__":
    main()
