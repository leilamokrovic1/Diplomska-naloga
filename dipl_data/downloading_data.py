import os
import requests
import traceback
from bs4 import BeautifulSoup


knjige_directory = 'knjige_html'
base_url = "https://www.goodreads.com"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.111 Safari/537.36",
    "Referer": "https://www.goodreads.com/"
}

def download_url_to_string(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Napaka {response.status_code} pri dostopu do {url}")
            return None
    except Exception:
        print(f"Napaka pri prenosu strani {url}: \n{traceback.format_exc()}")
        return None


def save_string_to_file(text, directory, filename):
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, "w", encoding="utf-8") as file_out:
        file_out.write(text)


def get_book_links():
    url = "https://www.goodreads.com/shelf/show/novels"
    html = download_url_to_string(url)

    if not html:
        print("Napaka pri prenosu glavne strani.")
        return []

    soup = BeautifulSoup(html, "html.parser")
    book_links = []

    # poišče prvih 50 romanov
    for book in soup.select("a.bookTitle")[:50]:  
        link = book.get("href")
        if link and link.startswith("/book/show/"):  #le prave knjige
            book_links.append(base_url + link)

    return book_links

#prenese in shrani knjige
def download_books():
    book_links = get_book_links()

    for idx, book_url in enumerate(book_links):
        book_html = download_url_to_string(book_url)
        if book_html:
            filename = f"knjiga_{idx+1}.html"
            save_string_to_file(book_html, knjige_directory, filename)
            print(f" Shranjena knjiga: {filename}")
        else:
            print(f"Napaka pri knjigi {book_url}")


download_books()
