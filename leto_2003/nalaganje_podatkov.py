# knjige pridobljene 19. 3. 2026
import os
import requests
import traceback
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time


knjige_directory = 'knjige_03_html'
base_url = "https://www.goodreads.com"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9"
}

def download_url_to_string(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
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


def get_book_links(max_books=300):
    url = "https://www.goodreads.com/book/popular_by_date/2003"

    options = Options()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(5)

    book_links = []

    # klikaj "Show more", dokler nimamo 300 knjig ali ni več gumba
    while len(book_links) < max_books:
        try:
            show_more = driver.find_element(By.XPATH, "//button[contains(., 'Show more')]")
            driver.execute_script("arguments[0].click();", show_more)
            time.sleep(2)
        except:
            break  # ni več gumba, končamo

        # pobrišemo že obstoječe linke, da ne podvajamo
        books = driver.find_elements(By.XPATH, "//a[contains(@href, '/book/show/')]")
        for book in books:
            link = book.get_attribute("href")
            if link and link not in book_links:
                book_links.append(link)
                if len(book_links) >= max_books:
                    break

    driver.quit()
    return book_links[:max_books]

#prenese in shrani knjige
def download_books():
    book_links = get_book_links()

    for idx, book_url in enumerate(book_links):
        book_html = download_url_to_string(book_url)
        if book_html:
            filename = f"knj_03_{idx+1}.html"
            save_string_to_file(book_html, knjige_directory, filename)
            print(f" Shranjena knjiga: {filename}")
        else:
            print(f"Napaka pri knjigi {book_url}")


download_books()