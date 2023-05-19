import pickle
from serpapi import GoogleSearch
from PySide6.QtWidgets import QFileDialog , QTreeView, QGroupBox, QRadioButton, QListWidget, QProgressBar, QLineEdit, QSpacerItem, QTableView, QTextEdit, QTableWidget, QTableWidgetItem, QDateEdit,QToolBar, QHeaderView
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from googlesearch import search
from bs4 import BeautifulSoup
import requests

class ConcurrentWatch:
    def __init__(self, conc_list, search_input, add_button, remove_button, news_table):
        self.concurrents = []
        self.conc_list = conc_list
        self.search_input = search_input
        self.add_button = add_button
        self.remove_button = remove_button
        self.news_table = news_table

        # Charger les concurrents précédemment sauvegardés
        self.load_concurrents()

        # Mettre à jour la liste des concurrents
        self.update_conc_list()

        # Connecter les boutons à leurs méthodes respectives
        self.add_button.clicked.connect(self.add_concurrent)
        self.remove_button.clicked.connect(self.remove_concurrent)
        self.conc_list.currentIndexChanged.connect(self.handle_concurrent_selection)

    def add_concurrent(self):
        new_concurrent = self.search_input.text()
        if new_concurrent and new_concurrent not in self.concurrents:
            self.concurrents.append(new_concurrent)
            self.save_concurrents()
            self.update_conc_list()  # Mettre à jour la liste des concurrents après l'ajout

    def remove_concurrent(self):
        concurrent_to_remove = self.conc_list.currentText()
        if concurrent_to_remove:
            index = self.conc_list.currentIndex()
            # Retirer de la liste des concurrents
            if concurrent_to_remove in self.concurrents:
                self.concurrents.remove(concurrent_to_remove)
            # Retirer de la comboBox
            self.conc_list.removeItem(index)
            self.save_concurrents()

    def save_concurrents(self):
        with open("concurrents.pkl", "wb") as file:
            pickle.dump(self.concurrents, file)

    def load_concurrents(self):
        try:
            with open("concurrents.pkl", "rb") as file:
                self.concurrents = pickle.load(file)
        except FileNotFoundError:
            pass

    def update_conc_list(self):
        self.conc_list.clear()
        self.conc_list.addItems(self.concurrents)

    def search_news(self):
        concurrent_name = self.conc_list.currentText()
        if concurrent_name:
            api_key = "9b0d4c0366546a7bd81c14d13ae3f304ea744bff2faa67fab9eed518194b7f40"
            search_query = f'"{concurrent_name}" ("vérification d\'identité" OR "authentification" OR "KYC" OR "identité en ligne" OR "évènement" OR "salon" OR "fraud" OR "innovation" OR "partners")'
            
            # Calculez le premier et le dernier jour du mois précédent
            today = datetime.date.today()
            first_day_of_previous_month = today.replace(day=1) - datetime.timedelta(days=1)
            last_day_of_previous_month = first_day_of_previous_month.replace(day=1) - datetime.timedelta(days=1)
            
            start_index = 0
            has_results = True
            extracted_data = []
            
            while has_results and start_index < 50:
                params = {
                    "q": search_query,
                    "start": start_index,
                    "tbm": "nws",
                    "api_key": api_key,
                    "hl": "fr",
                    "gl": "fr",
                    "google_domain": "google.fr",
                    "per_page": 100,
                    "date_restrict": f"{first_day_of_previous_month}..{last_day_of_previous_month}" # Période de recherche
                }
                
                search = GoogleSearch(params)
                results = search.get_dict()
                results_key = "news_results" if "news_results" in results else "organic_results"
                
                # Vérifiez si le nombre de résultats est nul
                if results_key in results and len(results[results_key]) > 0:
                    extracted_data.extend(results[results_key])
                    if 'next' not in results:
                        has_results = False
                    else:
                        start_index += 100
                else:
                    # Effectuez une recherche sur la page principale si aucun résultat n'est trouvé dans l'onglet "actualité"
                    params["tbm"] = ""
                    search = GoogleSearch(params)
                    results = search.get_dict()
                    results_key = "organic_results" if "organic_results" in results else "news_results"
                    
                    if results_key in results and len(results[results_key]) > 0:
                        extracted_data.extend(results[results_key])
                        if 'next' not in results:
                            has_results = False
                        else:
                            start_index += 100
                    else:
                        has_results = False
                        
                # Ajouter la condition pour vérifier si le nombre d'articles est inférieur à 3
                if len(extracted_data) < 3:
                    params["tbm"] = ""
                    search = GoogleSearch(params)
                    results = search.get_dict()
                    results_key = "organic_results" if "organic_results" in results else "news_results"
                    
                    if results_key in results and len(results[results_key]) > 0:
                        extracted_data.extend(results[results_key])
                        if 'next' not in results:
                            has_results = False
                        else:
                            start_index += 100
                            
            self.update_table(extracted_data)

    def handle_concurrent_selection(self, index):
        self.search_news()

    def update_table(self, data):
        self.news_table.setRowCount(len(data))
        for i, item in enumerate(data):
            title = item['title'] if 'title' in item else ''
            date = item['date'] if 'date' in item else ''
            source = item['source'] if 'source' in item else ''
            
            self.news_table.setItem(i, 0, QTableWidgetItem(title))
            self.news_table.setItem(i, 1, QTableWidgetItem(date))
            self.news_table.setItem(i, 2, QTableWidgetItem(source))

    
