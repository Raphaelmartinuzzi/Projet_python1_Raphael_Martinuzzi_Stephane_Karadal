# Projet_python1_Raphael_Martinuzzi_Stephane_Karadal

Dans ce projet, nous avons réalisé un script en Python pour récupérer les informations du site books.toscrape.com, qui sert à s’entraîner au web scraping.

Notre programme permet d’enregistrer toutes les données des livres présents sur le site, triées par catégorie, et de sauvegarder aussi les images.

D’abord, nous commençons par importer les bibliothèques nécessaires :

"pandas" pour créer les fichiers CSV, "requests" pour télécharger les pages du site, "scrapy" (avec "Selector") pour analyser le code HTML, "urljoin" pour gérer les liens, et "os", "time", "hashlib" pour la gestion des fichiers, des dossiers et des noms d’images.

Ensuite, on définit l’URL de base du site, puis on crée deux dossiers :

"outputs/csv" pour les fichiers CSV,
"outputs/images" pour enregistrer les images des livres.

Le programme télécharge ensuite la page d’accueil du site et utilise "Selector" pour trouver les differentes catégories de livres.

On récupère à la fois le nom de chaque catégorie et bien sûr son lien.
Après ça, on fait une boucle sur chaque catégorie.

Pour chacune :
->On affiche son nom dans la console (pour suivre la progression).
->On télécharge la page correspondante.
->On récupère tous les liens vers les livres de cette page.
->Pour chaque livre, on ouvre sa page et on récupère :

le titre, le prix, la disponibilité, la note (nombre d’étoiles), le code UPC, l’URL de l’image. La fonction "filename_from_title" nous sert à créer un nom unique pour chaque image grâce au code UPC et à un hash du titre.

Ensuite, on télécharge l’image du livre et on la sauvegarde dans le dossier correspondant à sa catégorie.

À la fin de chaque catégorie, on rassemble toutes les informations des livres dans un DataFrame avec "pandas", puis on enregistre le tout dans un fichier CSV dans le dossier "outputs/csv".

Le programme affiche enfin un message indiquant combien de livres ont été enregistrés pour cette catégorie et où les images ont été sauvegardées.

Ce projet nous a permis de mieux comprendre :
->comment utiliser "requests" pour télécharger des pages web,
->comment extraire des informations précises dans du HTML avec "scrapy.Selector",
->comment structurer des données avec "pandas",
->et comment sauvegarder des images et des fichiers CSV automatiquement.
