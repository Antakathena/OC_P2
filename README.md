## Infos Générales :

 Scrap Bookstoscap.py est un programme python 3 qui récupère des informations concernant les livres présentés dans le catalogue en ligne Bookstoscrap.com.
 
## Utilité :

Le programme gratte le site internet grâce à Requests et BeautifulSoup.
Il créé un fichier csv par catégorie de livre présentée sur Bookstoscrap.com.
Chaque csv comporte, pour tous les livres de la catégorie, les informations suivantes :
product_page_url,  universal_product_code, title, price_including_tax, price_excluding_tax,
number_available, product_description, category, review_rating, image_url

Il créé également un dossier images « bookstocrap pictures ». Ce dossier contient  les images des couvertures de livres pour chaque catégorie.

## Fonctionnalités :

### Fonctions : 
La fonction create_pictures_folder créé un dossier où ranger les images d'une catégorie
La fonction scrap_books_urls récupère les URL des livres d'une catégorie. Elle s'applique sur l'URL d'une page catégorie.
La fonction get_image récupère l'image de couverture d'un livre à partir d'une page livre et créé un fichier jpeg dont le nom est la catégorie et le titre du livre.
La fonction scrap_book_page récupère les informations sur un livre. Elle s'applique sur l'url d'une page livre. Elle renvoie un dictionnaire avec toutes les informations voulues.

### Main :
On récupère la page d'accueil de Bookstoscrape.com
puis on scrappe les liens vers les 1ères pages des catégories
puis les liens vers les livres à partir de ces pages
puis les informations des livres à partir de ces liens trouvés sur les pages d'une catégorie
enfin, on créé un fichier csv par catégorie qui répertorie les informations extraites pour les livres de cette catégorie.

## Instruction de démarrage :
Dans un terminal, utiliser les commandes suivantes :

$ python3 -m venv env (créé un dossier env dans le répértoire où vous vous trouvez)

$ source env/bin/activate (sous linux) ou env\Scripts\activate.bat (pour activer l'environnement virtuel sous windows)
  
$ git clone https://github.com/Antakathena/OC_P2

$ cd ../chemin/du/dossier (de la copie de OC_P2 dans votre dossier env)

$ pip install -r requirements.txt

$ python Scrap_Bookstoscrap.py

