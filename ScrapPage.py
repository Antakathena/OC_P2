# Nous voulons une fonction qui scrappe les infos voulus dans une page livre
#setup
import requests
from bs4 import BeautifulSoup

#on commence par aller chercher la page d'accueil et parcer
URLaccueil = "http://books.toscrape.com/"
requests.get(URLaccueil)
ContenuPageAccueil = requests.get(URLaccueil)
soup = BeautifulSoup(ContenuPageAccueil.text)

#puis on scrappe les liens vers les pages n°1 de chaque catégorie du catalogue
links = []
for link in soup.find_all("a"):
    links.append(link.attrs["href"])
    
categories_links = []
for l in links [3:53]:
    categories_links.append("http://books.toscrape.com/"+ l)

