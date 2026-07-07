import os
import csv
import re
from bs4 import BeautifulSoup

html_folder = 'knjige_html'
output_txt_folder = 'knjige_opisi'
csv_output_file = 'knjige_metadata.csv'

os.makedirs(output_txt_folder, exist_ok=True)

with open(csv_output_file, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Knjiga', 'Originalni naslov', 'Avtor(ji)', 'Žanri']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # preštejemo knjige
    for i, filename in enumerate(sorted(os.listdir(html_folder)), 1):
        if filename.endswith('.html'):
            file_path = os.path.join(html_folder, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')

                # naslov
                title_tag = soup.find('h1', {'data-testid': 'bookTitle'})
                original_title = title_tag.text.strip() if title_tag else 'Unknown Title'

                # avtorji
                author_tags = soup.find_all('span', class_='ContributorLink__name')
                authors = ', '.join([tag.text.strip() for tag in author_tags]) if author_tags else 'Unknown Author'

                # žanri
                genres_div = soup.find('div', {'data-testid': 'genresList'})
                genres = []
                if genres_div:
                    genre_links = genres_div.find_all('a')
                    for link in genre_links:
                        genre_text = link.get_text(strip=True)
                        if genre_text:
                            genres.append(genre_text)
                genres = ', '.join(sorted(set(genres))) if genres else 'Unknown'

                # opisi
                desc_div = soup.find('div', {'data-testid': 'description'})
                if desc_div:
                    span_tags = desc_div.find_all('span')
                    if len(span_tags) > 1:
                        full_description = span_tags[1].get_text(separator='\n').strip()
                    else:
                        full_description = span_tags[0].get_text(separator='\n').strip()
                else:
                    full_description = 'No description available.'

               
                knjiga_ime = f"knjiga_{i}"
                txt_path = os.path.join(output_txt_folder, f"{knjiga_ime}.txt")
                with open(txt_path, 'w', encoding='utf-8') as txt_file:
                    txt_file.write(full_description)

                
                writer.writerow({
                    'Knjiga': knjiga_ime.replace("_", " ").capitalize(),
                    'Originalni naslov': original_title,
                    'Avtor(ji)': authors,
                    'Žanri': genres
                })

print("vse bi moralo biti ok")
