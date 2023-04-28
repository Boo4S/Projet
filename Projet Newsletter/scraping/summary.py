from typing import List, Dict
import pandas as pd

def generer_resume_articles(articles: List[Dict]) -> pd.DataFrame:
    """
    Génère un résumé des articles donnés sous forme d'un DataFrame Pandas.
    """
    resume = pd.DataFrame(articles, columns=["titre", "source", "date", "resume", "url"])
    resume = resume.sort_values(by=["date"], ascending=False)
    return resume

def generer_fichier_resume_articles(articles: List[Dict], nom_fichier: str):
    """
    Génère un résumé des articles donnés sous forme d'un fichier Excel.
    """
    resume = generer_resume_articles(articles)
    resume.to_excel(nom_fichier, index=False)
