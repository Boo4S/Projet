def choix_fonctionnalite():
    print("Sélectionnez les fonctionnalités à utiliser :")
    print("1. Extraire les articles pertinents")
    print("2. Générer un fichier Excel contenant les informations des articles extraits")
    print("3. Vérifier les doublons d'articles")
    print("4. Résumer les articles extraits")
    print("5. Traduire les articles extraits en français")
    choix = input("Entrez les numéros de fonctionnalités séparés par des virgules (ex. 1,2,3) : ")
    choix = choix.split(",")
    choix = [int(x) for x in choix]
    fonctionnalites = {
        "extraire_articles": 1 in choix,
        "generer_fichier": 2 in choix,
        "verifier_doublons": 3 in choix,
        "resumer_articles": 4 in choix,
        "traduire_articles": 5 in choix,
    }
    return fonctionnalites
