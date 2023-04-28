def trouver_doublons(articles, article):
    """
    Vérifie si un article est un doublon en se basant sur l'URL et le titre de l'article.
    """
    for a in articles:
        if a["url"] == article["url"] or a["titre"] == article["titre"]:
            return True
    return False
