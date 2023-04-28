import datetime
import hashlib
import os
import random
import string
import urllib.parse
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import pandas as pd
import googlesearch
import json

# Fonction pour extraire les articles pertinents à partir des résultats de recherche
def extraire_articles_recherche(mots_cles, date_debut, date_fin):
    # Formatage de la plage de dates pour la recherche Google
    date_debut_str = date_debut.strftime("%Y-%m-%d")
    date_fin_str = date_fin.strftime("%Y-%m-%d")
    plage_dates = f"daterange:{date_debut_str}-{date_fin_str}"

    # Recherche Google des articles pertinents
    query = f"{mots_cles} {plage_dates}"
    search_results = googlesearch.search(query, num_results=10, lang="fr")

    articles = []
    for url in search_results:
        try:
            # Extraction des informations pertinentes à partir de la page web
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            page = urlopen(req)
            soup = BeautifulSoup(page, 'html.parser')

            titre = soup.find('title').text
            date = soup.find('time').text
            contenu = soup.find_all('p')

            # Résumé automatique du contenu
            resumer = ""
            for p in contenu:
                resumer += p.text.strip() + " "
            resumer = resumer[:300] + "..." if len(resumer) > 300 else resumer

            # Stockage des informations dans un dictionnaire
            article = {
                "date": date,
                "site": url,
                "titre": titre,
                "resumer": resumer
            }
            articles.append(article)
        except:
            # Gestion des erreurs
            print(f"Erreur lors de l'extraction de l'article à partir de {url}")

    return articles

# Fonction pour vérifier les doublons d'articles
def verifier_doublons(articles):
    urls = set()
    titres = set()
    articles_uniques = []
    for article in articles:
        if article["site"] not in urls and article["titre"] not in titres:
            urls.add(article["site"])
            titres.add(article["titre"])
            articles_uniques.append(article)
    return articles_uniques

# Fonction pour générer un mot de passe aléatoire
def generer_mot_de_passe():
    # Génération d'un mot de passe aléatoire de 12 caractères
    lettres = string.ascii_letters + string.digits
    mot_de_passe = ''.join(random.choice(lettres) for i in range(12))
    return mot_de_passe

# Fonction pour créer un compte utilisateur
def creer_compte_utilisateur():
    username = input("Entrez un nom d'utilisateur : ")
    password = input("Entrez un mot de passe : ")
    # Hashage du mot de passe avec un sel pour plus de sécurité
    sel = generer_mot_de_passe()
    password_hash = hashlib.sha256((password + sel).encode()).hexdigest()
    # Écriture des informations d'identification dans un fichier JSON sécurisé
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config", "credentials.json")
    with open(path, "r") as f:
        credentials = json.load(f)
    credentials[username] = {
        "password_hash": password_hash,
        "sel": sel
    }
    with open(path, "w") as f:
        json.dump(credentials, f)
    print("Compte utilisateur créé avec succès.")

# Fonction pour vérifier les informations d'identification d'un utilisateur
def verifier_identification(username, password):
    # Récupération des informations d'identification du fichier JSON sécurisé
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config", "credentials.json")
    with open(path, "r") as f:
        credentials = json.load(f)
    if username in credentials:
        # Vérification du mot de passe hashé
        sel = credentials[username]["sel"]
        password_hash = hashlib.sha256((password + sel).encode()).hexdigest()
        if password_hash == credentials[username]["password_hash"]:
            return True
    return False

