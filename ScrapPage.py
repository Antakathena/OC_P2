# Nous voulons une fonction qui scrappe les infos voulues dans une page livre
#setup
import requests
from bs4 import BeautifulSoup
import csv

SESSION = requests.Session()
url_home_page = "https://books.toscrape.com/"
REVIEW_RATINGS = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}


def scrap_books_url(url: str) -> list:
    """
    C'est la fonction qui récupére les url des livres d'une catégorie.
    Elle s'applique sur l'url d'une page catégorie.

    Input:
    url : url vers la première page correspondant à une catégorie

    Output:
    Liste contenant les url des livres appartenant à une catégorie
    """
    assert url.startswith("https://books.toscrape.com/catalogue/category/"), \
           f"Cette fonction ne fonctionne que sur les url https://books.toscrape. Reçu: {url}"
    category_page_content = SESSION.get(url)
    soup = BeautifulSoup(category_page_content.text, "lxml")

    clean_links_to_books = []
    for h3 in soup.find_all("h3"):
        link = h3.a.attrs["href"]
        absolute_link = link.replace("../../../", f"{url_home_page}catalogue/")
        clean_links_to_books.append(absolute_link)
    # On doit trouver l'url de la {page suivante} et faire tourner la fonction scrap_books_url() dessus \net ajouter les url trouvées à la liste des livres.
    balises_a = soup.find_all("a")
    balises_a[-1]
    if balises_a[-1].text == "next":
        page_suivante = balises_a[-1].attrs["href"]
        url = url.split("/")[:-1]  # split divise une chaine de caractères en plusieurs elt séparés par /
        url = "/".join(url + [page_suivante])
        return clean_links_to_books + scrap_books_url(url) # concatenation de liste, extend modifie l'ancienne liste

    return clean_links_to_books

def scrap_book_page(books_pages : str):
    """
    C'est la fonction qui récupère les informations sur un livre.
    Elle s'applique sur l'url d'une page livre.
    Elle renvoie un dictionnaire avec toutes les informations voulues sur le livre.

    Input : 
    books_pages = url vers une page livre du catalogue

    Output :
    Dictionnaire contenant les informations sur le livre
    
    """
    # assert préconditions
    assert books_pages.startswith("https://books.toscrape.com/catalogue/"), \
           f"Cette fonction ne fonctionne que sur les url https://books.toscrape/catalogue/. Reçu: {books_pages}"
    URLpageLivre = books_pages
    ContenuPage = SESSION.get(URLpageLivre)
    soup = BeautifulSoup(ContenuPage.text, "lxml")
    upc = soup.find("td").text
    title = soup.title.text.strip().replace("| Books to Scrape - Sandbox", "").strip()
    price_including_tax = soup.find(text="Price (incl. tax)").findNext('td').text.strip('Â').replace("£", "")
    price_excluding_tax = soup.find(text="Price (excl. tax)").findNext('td').text.strip('Â').replace("£", "")
    number_available = soup.find(text="Availability").findNext('td').text.replace("In stock (", "").replace("available)", "").strip()
    try:
        product_description = soup.find(id= "product_description").findNext("p").text
    except AttributeError:
        product_description = None
    links = soup.find_all("a")
    category = links[3].text
    balisesP = soup.find_all("p")
    star_rating= balisesP[2]
    review_rating = star_rating.attrs["class"][1]
    review_rating = REVIEW_RATINGS[review_rating]
    image_url = soup.find("img").attrs["src"].replace("../../","http://books.toscrape.com/")

    book_infos = {}
    book_infos["product_page_url"] = URLpageLivre
    book_infos["universal_ product_code (upc)"] = upc
    book_infos["title"]= title
    book_infos["price_including_tax"]= price_including_tax
    book_infos["price_excluding_tax"]= price_excluding_tax
    book_infos["number_available"]= number_available
    book_infos["product_description"]= product_description
    book_infos["category"]= category
    book_infos["review_rating"]= review_rating
    book_infos["image_url"]= image_url

    return book_infos

   
if __name__ == "__main__":
    #On récupère la page d'accueil
    home_page = SESSION.get(url_home_page)
    soup = BeautifulSoup(home_page.text, "lxml")

    # puis on scrappe les liens vers les pages des catégories
    categories_pages = {}
    for link in soup.find_all("a")[3:53]: #les autres a ne sont pas des liens vers des catégories
        categories_pages[link.text.strip()] = url_home_page + link.attrs["href"]

    # puis les liens vers les livres à partir des pages d'une catégorie
    books_pages = {}
    for categorie, url_categorie in categories_pages.items(): # sans item, on itere qu'à travers les keys
        books_pages[categorie.strip()] = scrap_books_url(url_categorie)
        print(f"Catégorie scrapée: {categorie}, nombre de livres: {len(books_pages[categorie.strip()])}")

    #puis les infos des livres à partir de ces liens trouvés sur les pages d'une catégorie
    books_infos = {}
    for categorie, books_url in books_pages.items():
        books_infos[categorie] = []
        for book_url in books_url:
            book_info = scrap_book_page(book_url)
            books_infos[categorie].append(book_info)
        print(f"Pages de la catégorie {categorie} scrapée")
        
try: 
    for categorie in books_infos: 
        with open(f'{categorie}.csv', 'w', encoding="utf-8") as file:
            headers = ["product_page_url","universal_ product_code (upc)","title" ,"price_including_tax","price_excluding_tax" ,"number_available","product_description","category","review_rating","image_url"]
            writer = csv.DictWriter(file, headers)
            writer.writerows(books_infos[categorie])

except IOError:
    print("I/O error")    
            

"""
    assert books_pages["Travel"][0] == "https://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html", \
        f"La fonction retourne la mauvaise url.\n Reçu:{books_pages["Travel"][0]}. Attendu: https://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html"
    assert len(books_pages["Travel"]) == 11, \
        f"Il manque des url sur la page Travel.\n Reçu:{books_pages["Travel"]}. Attendu: 11."
    assert len(books_pages["Sequential Art"]) == 75
    test_scrap_book_page = scrap_book_page("https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html")
    assert test_scrap_book_page["title"] == "A Light in the Attic", f"La fonction retourne la mauvaise réponse. Valeur reçue: '{test_scrap_book_page['title']}'"
"""
    

"""
# with open ("img", "wb") as
# session page.content
"""