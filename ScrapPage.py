# Nous voulons une fonction qui scrappe les infos voulues dans une page livre
#setup
import requests
from bs4 import BeautifulSoup

SESSION = requests.Session()
url_home_page = "https://books.toscrape.com/"


def scrap_books_url(URL: str) -> list:
    """
    C'est la fonction qui récupére les URL des livres d'une catégorie.
    Elle s'applique sur l'url d'une page catégorie.

    Input:
    URL : URL vers la première page correspondant à une catégorie

    Output:
    Liste contenant les URL des livres appartenant à une catégorie
    """
    assert URL.startswith("https://books.toscrape.com/catalogue/category/"), \
           f"Cette fonction ne fonctionne que sur les URL https://books.toscrape. Reçu: {URL}"
    category_page_content = SESSION.get(URL)
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
        URL = URL.split("/")[:-1]  # split divise une chaine de caractères en plusieurs elt séparés par /
        URL = "/".join(URL + [page_suivante])
        return clean_links_to_books + scrap_books_url(URL) # concatenation de liste, extend modifie l'ancienne liste

    return clean_links_to_books

def scrap_book_page(books_pages : str):
    """
    C'est la fonction qui récupère les informations sur un livre.
    Elle s'applique sur l'url d'une page livre.
    Elle renvoie un dictionnaire avec toutes les informations voulues sur le livre.

    Input : 
    books_pages = URL vers une page livre du catalogue

    Output :
    Dictionnaire contenant les informations sur le livre
    
    """
    # assert préconditions
    assert books_pages.startswith("https://books.toscrape.com/catalogue/"), \
           f"Cette fonction ne fonctionne que sur les URL https://books.toscrape. Reçu: {books_pages}"
    assert books_pages.endswith("index.html"), f"Cette fonction ne fonctionne que sur une page livre. Reçu : {books_pages}" 
    URLpageLivre = books_pages
    ContenuPage = SESSION.get(URLpageLivre)
    soup = BeautifulSoup(ContenuPage.text, "lxml")
    upc = soup.find("td").text
    title = soup.title.text.strip().replace("| Books to Scrape - Sandbox", "")
    price_including_tax = soup.find(text="Price (incl. tax)").findNext('td').text.strip('Â')
    price_excluding_tax = soup.find(text="Price (excl. tax)").findNext('td').text.strip('Â')
    number_available = soup.find(text="Availability").findNext('td').text.replace("In stock (", "").replace("available)", "")
    product_description = soup.find(id= "product_description").findNext("p").text
    links = soup.find_all("a")
    category = links[3].text
    balisesP = soup.find_all("p")
    star_rating= balisesP[2]
    review_rating = star_rating.attrs["class"][1]
    image_url = soup.find("img").attrs["src"].replace("../../","http://books.toscrape.com/")
    
    BookInfos = {}
    BookInfos["product_page_url"] = URLpageLivre
    BookInfos["universal_ product_code (upc)"] = upc
    BookInfos["title"]= title
    BookInfos["price_including_tax"]= price_including_tax
    BookInfos["price_excluding_tax"]= price_excluding_tax
    BookInfos["number_available"]= number_available
    BookInfos["product_description"]= product_description
    BookInfos["category"]= category
    BookInfos["review_rating"]= review_rating
    BookInfos["image_url"]= image_url
    
    
    # assert postconditions
    test_scrap_book_page = scrap_book_page("http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html")
    assert test_scrap_book_page["title"] == "A Light in the Attic", f"La fonction retourne la mauvaise réponse."

    return BookInfos

   
if __name__ == "__main__":
    #On récupère la page d'accueil
    home_page = SESSION.get(url_home_page)
    soup = BeautifulSoup(home_page.text, "lxml")

    #puis on scrappe les liens vers les pages n°1 de chaque catégorie du catalogue
    links = []
    for link in soup.find_all("a"):
        links.append(link.attrs["href"])
    categories_links = []
    for l in links [3:53]: #les autres a ne sont pas des liens vers des catégories
        categories_links.append(url_home_page + l)

    #On récupère les url des livres à partir de ces pages catégories
    books_pages = []
    for URL in categories_links :
        scrap_books_url(URL)
        books_pages.extend( scrap_books_url(URL))

    #On récupère les infos des livres à partir des url des page livre
    for book_page in books_pages:
        scrap_book_page(book_page)

    #text fonction scrap_books_url()
    test_scrap_books_url = scrap_books_url("https://books.toscrape.com/catalogue/category/books/travel_2/index.html")

    assert test_scrap_books_url[0] == "https://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html", \
        f"La fonction retourne la mauvaise url.\n Reçu: {test_scrap_books_url[0]}. Attendu: https://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html"
    assert len(test_scrap_books_url) == 11, \
        f"Il manque des URL sur la page Travel.\n Reçu: {len(test_scrap_books_url)}. Attendu: 11."

    # Test de la pagination dans la récupération des url de livres par catégorie (pour les catégories de plus de 20 livres)
    URL = "https://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html"
    BooksUrl_List = scrap_books_url(URL)
    assert len(BooksUrl_List) == 75



