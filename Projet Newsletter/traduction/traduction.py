import requests
from googletrans import Translator


def traduire_article(article):
    """
    Traduit un article en français en utilisant l'API Google Translate.
    """
    traduction = None
    try:
        translator = Translator()
        if "resume" in article:
            traduction = translator.translate(article["resume"], dest="fr").text
        if "titre" in article:
            titre_fr = translator.translate(article["titre"], dest="fr").text
            article["titre"] = titre_fr
        if "source" in article:
            source_fr = translator.translate(article["source"], dest="fr").text
            article["source"] = source_fr
    except Exception as e:
        print(f"Une erreur est survenue lors de la traduction : {e}")
    return article, traduction
