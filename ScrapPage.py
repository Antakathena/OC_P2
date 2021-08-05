# Nous voulons une fonction qui scrappe les infos voulus dans une page livre
#setup
import requests
from bs4 import BeautifulSoup

SESSION = requests.Session()

#on commence par aller chercher la page d'accueil et parcer
URLaccueil = "https://books.toscrape.com/"
ContenuPageAccueil = SESSION.get(URLaccueil)
soup = BeautifulSoup(ContenuPageAccueil.text, "lxml")

#puis on scrappe les liens vers les pages n°1 de chaque catégorie du catalogue
links = []
for link in soup.find_all("a"):
    links.append(link.attrs["href"])
categories_links = []
for l in links [3:53]:
    categories_links.append(URLaccueil + l)

#puis il faut que chacun de ces liens soit traité pour extraire les livres de la catégorie 
# while?

def scrap_books_Url(URL):
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
    ContenuCategory = SESSION.get(URL)
    soup = BeautifulSoup(ContenuCategory.text, "lxml")

    clean_Links_to_books = []
    for h3 in soup.find_all("h3"):
        link = h3.a.attrs["href"]
        absolute_link = link.replace("../../../", f"{URLaccueil}catalogue/")
        clean_Links_to_books.append(absolute_link)
    # On doit trouver l'url de la {page suivante} et faire tourner la fonction scrap_books_Url() dessus \net ajouter les url trouvées à la liste des livres.
    balises_a = soup.find_all("a")
    balises_a[-1]
    if balises_a[-1].text == "next":
        page_suivante = balises_a[-1].attrs["href"]
        URL = URL.split("/")[:-1]  # split divise une chaine de cartères en plusieurs elt séparés par /
        URL = "/".join(URL + [page_suivante])
        return clean_Links_to_books + scrap_books_Url(URL) # concatenation de liste, extend modifie l'ancienne liste

    return clean_Links_to_books

test_scrap_books_Url = scrap_books_Url("https://books.toscrape.com/catalogue/category/books/travel_2/index.html")

assert test_scrap_books_Url[0] == "https://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html", \
       f"La fonction retourne la mauvaise url.\n Reçu: {test_scrap_books_Url[0]}. Attendu: https://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html"
assert len(test_scrap_books_Url) == 11, \
       f"Il manque des URL sur la page Travel.\n Reçu: {len(test_scrap_books_Url)}. Attendu: 11."

# Test de la pagination
URL = "https://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html"
BooksUrl_List = scrap_books_Url(URL)
for URL in BooksUrl_List:
    print(URL)
print(len(BooksUrl_List))
assert len(BooksUrl_List) == 75

arg = BooksUrl_List[3]

def ScrapBookPage(arg):
    URLpageLivre = arg
    ContenuPage = SESSION.get(URLpageLivre)
    soup = BeautifulSoup(ContenuPage.text, "lxml")
    UPC = soup.find("td").text
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
    
    BookInfos = {}
    BookInfos["product_page_url"]= URLpageLivre
    BookInfos["universal_ product_code (upc)"]= UPC
    BookInfos["title"]= title
    BookInfos["price_including_tax"]= price_including_tax
    BookInfos["price_excluding_tax"]= price_excluding_tax
    BookInfos["number_available"]= number_available
    BookInfos["product_description"]= product_description
    BookInfos["category"]= category
    BookInfos["review_rating"]= review_rating
    
    return BookInfos
    
for i in ScrapBookPage(arg).items():
    print(i)
    
