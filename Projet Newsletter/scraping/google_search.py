import requests
import json
import os


def google_search(query, cx):
    """
    Effectue une recherche Google en utilisant l'API Google Custom Search Engine (CSE).
    Renvoie une liste de résultats sous forme de dictionnaires contenant les informations suivantes :
    - titre
    - URL
    - description
    - source
    - date
    """
    api_key = get_api_key()
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&cx={cx}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        results = []
        data = json.loads(response.text)
        if "items" in data:
            for item in data["items"]:
                result = {}
                result["titre"] = item.get("title", "")
                result["lien"] = item.get("link", "")
                result["description"] = item.get("snippet", "")
                result["source"] = item.get("displayLink", "")
                result["date"] = item.get("formattedDate", "")
                results.append(result)
        return results
    else:
        raise Exception("Une erreur est survenue lors de la recherche Google.")


def get_api_key():
    """
    Récupère la clé API Google à partir du fichier de configuration.
    """
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config", "config.json")
    with open(path, "r") as f:
        config = json.load(f)
        api_key = config["google"]["api_key"]
    return api_key
