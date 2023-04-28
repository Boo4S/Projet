import requests
from bs4 import BeautifulSoup


def extraire_articles_recherche(mots_cles, date_debut, date_fin):
    """
    Recherche sur Google les articles pertinents pour les mots clés donnés dans la plage de dates spécifiée.
    """
    url = f"https://www.google.com/search?q={mots_cles}&tbs=cdr:1,cd_min:{date_debut},cd_max:{date_fin}&tbm=nws"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    articles = []
    for result in soup.find_all("div", class_="g"):
        article = extraire_article(result)
        if article is not None:
            articles.append(article)
    return articles


def extraire_article(result):
    """
    Extrait les informations d'un article à partir d'un résultat de recherche Google.
    """
    try:
        titre = result.find("h3", class_="r").get_text()
        url = result.find("a")["href"]
        date = result.find("span", class_="f").get_text()
        source = result.find("span", class_="p").get_text()
        resume = result.find("div", class_="st").get_text()
        article = {
            "titre": titre,
            "url": url,
            "date": date,
            "source": source,
            "resume": resume,
        }
        return article
    except AttributeError:
        return None
