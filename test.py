import pandas as pd
import requests
from scrapy import Selector
from urllib.parse import urljoin
import os
import time
import hashlib
 
base_url = "https://books.toscrape.com/"
 
def filename_from_title(upc, title):
    h = hashlib.sha1(title.encode('utf-8')).hexdigest()
    return f"{upc}_{h}.jpg"
 
os.makedirs("outputs/csv", exist_ok=True)
os.makedirs("outputs/images", exist_ok=True)
 
try:
    response = requests.get(base_url, timeout=10)
    response.encoding = "utf-8"
    selector = Selector(text=response.text)
except requests.RequestException as e:
    print("Erreur de connexion au site :", e)
    response = None
 
if response:
    categories_liens = selector.css('ul.nav-list ul li a::attr(href)').getall()
    categories_noms = [name.strip() for name in selector.css('ul.nav-list ul li a::text').getall()]
 
    for cat_nom, cat_lien in zip(categories_noms, categories_liens):
        print(f"\nScraping catégorie : {cat_nom}")
 
        cat_url = urljoin(base_url, cat_lien)
        page_suivant = cat_url
 
        livre_titre = []
        prix = []
        disponibilité = []
        note = []
        upcs = []
        image_urls = []
        produit_urls = []
 
        cat_image_path = f"outputs/images/{cat_nom.replace(' ', '_')}"
        os.makedirs(cat_image_path, exist_ok=True)
 
        while page_suivant:
            try:
                res = requests.get(page_suivant, timeout=5)
                res.encoding = "utf-8"
                sel = Selector(text=res.text)
            except requests.RequestException as e:
                print(f"Erreur téléchargement page {page_suivant} : {e}")
                break
 
            produit_liens = [urljoin(page_suivant, href) for href in sel.css('article.product_pod h3 a::attr(href)').getall()]
 
            for link in produit_liens:
                try:
                    page = requests.get(link, timeout=5)
                    page.encoding = "utf-8"
                    s = Selector(text=page.text)
                except requests.RequestException as e:
                    print(f"Erreur téléchargement livre {link} : {e}")
                    continue
 
                titre = s.css('div.product_main h1::text').get(default="Unknown")
                prix_livre = s.css('p.price_color::text').get(default="Unknown")
 
                dispo_text = s.css('.availability::text').getall()
                dispo_text = [a.strip() for a in dispo_text if a.strip()]
                disponibilité_livre = dispo_text[0] if dispo_text else "Unknown"
 
                upc = s.css('table.table.table-striped tr:nth-child(1) td::text').get()
                note_class = s.css('p.star-rating::attr(class)').get()
                note_livre = note_class.replace('star-rating', '').strip() if note_class else "Unknown"
 
                img_src = s.css(".carousel-inner img::attr(src)").get()
                if not img_src:
                    img_src = s.css('div.item.active img::attr(src)').get()
                img_url = urljoin(link, img_src) if img_src else "None"
 
                category_name = s.css("ul.breadcrumb li:nth-child(3) a::text").get(default=cat_nom)
 
                try:
                    img_data = requests.get(img_url, timeout=5).content
                    img_file = f"{cat_image_path}/{filename_from_title(upc, titre)}"
                    with open(img_file, "wb") as f:
                        f.write(img_data)
                except requests.RequestException as e:
                    print(f"Erreur téléchargement image {img_url} : {e}")
 
                livre_titre.append(titre)
                prix.append(prix_livre)
                disponibilité.append(disponibilité_livre)
                note.append(note_livre)
                upcs.append(upc)
                image_urls.append(img_url)
                produit_urls.append(link)
 
                time.sleep(0.1)
 
            next_page_rel = sel.css('li.next a::attr(href)').get()
            page_suivant = urljoin(page_suivant, next_page_rel) if next_page_rel else None
 
        df = pd.DataFrame({
            'Titre livre': livre_titre,
            'Prix': prix,
            'Disponibilité': disponibilité,
            'Note': note,
            'UPC': upcs,
            'Catégorie': [cat_nom] * len(livre_titre),
            'Image URL': image_urls,
            'Product URL': produit_urls
        })
 
        fichier_path = f"outputs/csv/category_{cat_nom.replace(' ', '_')}.csv"
        df.to_csv(fichier_path, index=False, encoding="utf-8-sig")
 
        print(f"{len(df)} livres enregistrés dans {fichier_path} et images dans {cat_image_path}")




