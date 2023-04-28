from tkinter import *
from tkinter import messagebox
from datetime import date
from main import *
from recherche import rechercher_articles


class InterfaceUtilisateur:

    def __init__(self, master):
        self.master = master
        self.master.title("Revue de presse")
        self.master.geometry("600x400")

        # Champ de texte pour les mots-clés
        self.mots_cles_label = Label(self.master, text="Mots-clés :")
        self.mots_cles_label.pack()
        self.mots_cles_entry = Entry(self.master)
        self.mots_cles_entry.pack()

        # Plage de dates pour filtrer les résultats
        self.dates_label = Label(self.master, text="Dates :")
        self.dates_label.pack()
        self.de_label = Label(self.master, text="De :")
        self.de_label.pack()
        self.de_entry = Entry(self.master)
        self.de_entry.pack()
        self.a_label = Label(self.master, text="À :")
        self.a_label.pack()
        self.a_entry = Entry(self.master)
        self.a_entry.pack()

        # Cases à cocher pour les fonctionnalités
        self.fonctionnalites_label = Label(self.master, text="Fonctionnalités :")
        self.fonctionnalites_label.pack()
        self.extraire_articles_var = IntVar()
        self.extraire_articles_checkbox = Checkbutton(self.master, text="Extraire les articles", variable=self.extraire_articles_var)
        self.extraire_articles_checkbox.pack()
        self.generer_fichier_var = IntVar()
        self.generer_fichier_checkbox = Checkbutton(self.master, text="Générer un fichier Excel", variable=self.generer_fichier_var)
        self.generer_fichier_checkbox.pack()
        self.verifier_doublons_var = IntVar()
        self.verifier_doublons_checkbox = Checkbutton(self.master, text="Vérifier les doublons", variable=self.verifier_doublons_var)
        self.verifier_doublons_checkbox.pack()
        self.resumer_articles_var = IntVar()
        self.resumer_articles_checkbox = Checkbutton(self.master, text="Résumer les articles", variable=self.resumer_articles_var)
        self.resumer_articles_checkbox.pack()
        self.traduire_articles_var = IntVar()
        self.traduire_articles_checkbox = Checkbutton(self.master, text="Traduire les articles", variable=self.traduire_articles_var)
        self.traduire_articles_checkbox.pack()

        # Bouton pour lancer la recherche
        self.lancer_recherche_button = Button(self.master, text="Lancer la recherche", command=self.lancer_recherche)
        self.lancer_recherche_button.pack()

    def lancer_recherche(self):
        # Récupération des valeurs des champs de texte
        mots_cles = self.mots_cles_entry.get()
        de = self.de_entry.get()
        a = self.a_entry.get()

        # Vérification des valeurs des champs de texte
        if mots_cles == "":
            messagebox.showerror("Erreur", "Veuillez entrer des mots-clés.")
            return
        if de == "" or a == "":
            dates = None
        else:
            try:
                dates = (date.fromisoformat(de), date.fromisoformat(a))
            except ValueError:
                messagebox.showerror("Erreur", "Veuillez entrer des dates valides au format ISO (AAAA-MM-JJ).")
                return

                # Vérification des cases à cocher pour les fonctionnalités
        extraire_articles = True if self.extraire_articles_var.get() else False
        generer_fichier = True if self.generer_fichier_var.get() else False
        verifier_doublons = True if self.verifier_doublons_var.get() else False
        resumer_articles = True if self.resumer_articles_var.get() else False
        traduire_articles = True if self.traduire_articles_var.get() else False


        # Lancement de la recherche
        resultats = rechercher_articles(mots_cles, dates, extraire_articles, generer_fichier, verifier_doublons, resumer_articles, traduire_articles)

        # Affichage des résultats dans une nouvelle fenêtre
        if resultats:
            fenetre_resultats = Toplevel(self.master)
            fenetre_resultats.title("Résultats de la recherche")
            fenetre_resultats.geometry("800x600")

            scrollbar = Scrollbar(fenetre_resultats)
            scrollbar.pack(side=RIGHT, fill=Y)

            liste_articles = Listbox(fenetre_resultats, yscrollcommand=scrollbar.set)
            for article in resultats:
                liste_articles.insert(END, article["titre"] + " - " + article["date"] + " - " + article["lien"])
            liste_articles.pack(fill=BOTH, expand=True)

            scrollbar.config(command=liste_articles.yview)

            fenetre_resultats.mainloop()
        else:
            messagebox.showinfo("Information", "Aucun résultat trouvé pour cette recherche.")

