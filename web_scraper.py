import requests
import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QStackedWidget, QFrame, QPushButton, QLabel, QSizePolicy, QComboBox, QCheckBox
from qtawesome import icon
from PySide6.QtCore import QEasingCurve, QPropertyAnimation, QAbstractTableModel, Qt, QDate
from PySide6.QtWidgets import QGraphicsOpacityEffect, QProgressBar, QLineEdit, QSpacerItem, QTableView, QTextEdit, QTableWidget, QTableWidgetItem, QDateEdit,QToolBar, QHeaderView
from PySide6.QtGui import QAction, QPainter
from serpapi import GoogleSearch
from Fonction import ArticleTableModel, PlotWidget
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from PySide6.QtCharts import QChart, QChartView, QLineSeries
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Interface RESOSearch")
        self.setGeometry(100, 100, 500, 400)

        # Création des widgets
        self.central_widget = QWidget()
        self.menu_widget = QFrame()
        self.menu_layout = QVBoxLayout()
        self.stacked_widget = QStackedWidget()

        # Configuration du menu
        self.menu_widget.setFixedWidth(200)
        self.menu_widget.setLayout(self.menu_layout)
        self.menu_widget.setFrameShape(QFrame.StyledPanel)

        # Créez un modèle de données pour les articles
        article_model = ArticleTableModel()
        self.article_model = article_model

        # Configurer la vue des articles
        self.table_view = QTableView()
        self.table_view.setModel(self.article_model)

        # Boutons du menu
        button_style = """
        QPushButton {
            color: white;
            background-color: #5F9EA0;
            font-weight: bold;
            border: none;
            padding: 10px;
        }
        QPushButton:hover {
            background-color: #7FB1B5;
        }
        """
        # Boutons du menu
        self.cleaner_button = QPushButton(icon('fa5s.broom', color='white'), "RESOSearch")
        self.cleaner_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.cleaner_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        self.cleaner_button.setStyleSheet(button_style)
        self.menu_layout.addWidget(self.cleaner_button)

        self.registry_button = QPushButton(icon('fa5s.archive', color='white'), "Visualisation des données")
        self.registry_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.registry_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        self.registry_button.setStyleSheet(button_style)
        self.menu_layout.addWidget(self.registry_button)

        # Bouton Veille concurrentielle
        self.competitive_intel_button = QPushButton(icon('fa5s.cogs', color='white'), "Veille concurrentielle")
        self.competitive_intel_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.competitive_intel_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        self.competitive_intel_button.setStyleSheet(button_style)
        self.menu_layout.addWidget(self.competitive_intel_button)

        # Bouton Veille stratégique
        self.strategic_intel_button = QPushButton(icon('fa5s.cogs', color='white'), "Veille stratégique")
        self.strategic_intel_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        self.strategic_intel_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        self.strategic_intel_button.setStyleSheet(button_style)
        self.menu_layout.addWidget(self.strategic_intel_button)


        # Configuration de la page RESOSearch
        self.cleaner_layout = QVBoxLayout()

        # Création de la barre d'outils
        self.toolbar = QToolBar()
        self.toolbar.setMovable(False)
        self.addToolBar(self.toolbar)


        # Création des actions pour les thèmes
        cybersec_action = QAction("Cybersécurité", self)
        cybersec_action.triggered.connect(lambda: self.update_keywords("cybersécurité, sécurité informatique, protection des données"))
        self.toolbar.addAction(cybersec_action)

        ai_action = QAction("Intelligence artificielle", self)
        ai_action.triggered.connect(lambda: self.update_keywords("intelligence artificielle, IA, machine learning, deep learning"))
        self.toolbar.addAction(ai_action)

        bigdata_action = QAction("Big Data", self)
        bigdata_action.triggered.connect(lambda: self.update_keywords("big data, données massives, analyse de données"))
        self.toolbar.addAction(bigdata_action)

        # Création d'un QVBoxLayout pour la première colonne
        self.column1_layout = QVBoxLayout()

        # Ajout de la zone de texte
        self.search_text = QLineEdit()
        self.search_text.setPlaceholderText("Entrez des mots-clés pour rechercher des articles")
        self.search_text.setFixedWidth(200)
        self.search_text.setFixedHeight(30)
        self.search_text.setStyleSheet("color: white; background-color: #353535; border: 1px solid white;")

        self.column1_layout.addWidget(self.search_text, alignment=Qt.AlignTop)

        # Création d'un QVBoxLayout pour les options d'extraction
        self.export_options_layout = QVBoxLayout()

        # Ajout des QCheckBox pour les formats d'extraction
        self.export_excel_checkbox = QCheckBox("Exporter en Excel")
        self.export_options_layout.addWidget(self.export_excel_checkbox)

        self.export_word_checkbox = QCheckBox("Exporter en Word")
        self.export_options_layout.addWidget(self.export_word_checkbox)

        # Création d'un QVBoxLayout pour les sélecteurs de dates
        self.date_range_layout = QVBoxLayout()

        # Ajout d'un QLabel pour la date de début
        self.start_date_label = QLabel("Date de début :")
        self.date_range_layout.addWidget(self.start_date_label)

        # Ajout du sélecteur de date de début
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setDate(QDate.currentDate())
        self.start_date_edit.setCalendarPopup(True)
        self.date_range_layout.addWidget(self.start_date_edit)

        # Ajout d'un QLabel pour la date de fin
        self.end_date_label = QLabel("Date de fin :")
        self.date_range_layout.addWidget(self.end_date_label)

        # Ajout du sélecteur de date de fin
        self.end_date_edit = QDateEdit()
        self.end_date_edit.setDate(QDate.currentDate())
        self.end_date_edit.setCalendarPopup(True)
        self.date_range_layout.addWidget(self.end_date_edit)

        # Ajout du QVBoxLayout des sélecteurs de dates à la première colonne
        self.column1_layout.addLayout(self.date_range_layout)

        # Ajout d'un QSpacerItem pour combler l'espace entre les options d'exportation et le bas de la fenêtre
        spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.export_options_layout.addItem(spacer)

        # Ajout du QVBoxLayout des options d'extraction à la première colonne
        self.column1_layout.addLayout(self.export_options_layout)


        # Création d'un QVBoxLayout pour la deuxième colonne
        self.column2_layout = QVBoxLayout()

        # Ajout de la QComboBox pour choisir le navigateur
        self.browser_combobox = QComboBox()
        self.browser_combobox.addItem("Google Chrome")
        self.browser_combobox.addItem("Mozilla Firefox")
        self.browser_combobox.addItem("Microsoft Edge")
        self.browser_combobox.addItem("Safari")
        self.browser_combobox.addItem("Opera")
        self.browser_combobox.setFixedWidth(150)
        self.browser_combobox.setFixedHeight(30)

        self.column2_layout.addWidget(self.browser_combobox)

        # Création d'un QVBoxLayout pour les options de langues
        self.language_options_layout = QVBoxLayout()

        # Ajout d'un QLabel pour expliquer l'option de choix de la langue
        self.language_label = QLabel("Choisissez la langue des articles :")
        self.language_options_layout.addWidget(self.language_label)

        # Ajout de la QComboBox pour choisir la langue
        self.language_combobox = QComboBox()
        self.language_combobox.addItem("Français")
        self.language_combobox.addItem("Anglais")
        self.language_combobox.addItem("Espagnol")
        self.language_combobox.addItem("Allemand")
        self.language_combobox.addItem("Italien")
        self.language_combobox.setFixedWidth(150)
        self.language_combobox.setFixedHeight(30)

        self.language_options_layout.addWidget(self.language_combobox)

        # Ajout d'un QSpacerItem pour pousser les options de langues vers le haut
        spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.language_options_layout.addItem(spacer)

        # Création d'un QVBoxLayout pour les options de partage
        self.share_options_layout = QVBoxLayout()

        # Ajout d'un QLabel pour expliquer l'option de partage
        self.share_label = QLabel("Partager les articles extraits sur :")
        self.share_options_layout.addWidget(self.share_label)

        # Ajout de la QComboBox pour choisir le mode de partage
        self.share_combobox = QComboBox()
        self.share_combobox.addItem("Aucun")
        self.share_combobox.addItem("Facebook")
        self.share_combobox.addItem("Twitter")
        self.share_combobox.addItem("LinkedIn")
        self.share_combobox.addItem("E-mail")
        self.share_combobox.setFixedWidth(150)
        self.share_combobox.setFixedHeight(30)

        self.share_options_layout.addWidget(self.share_combobox)

        # Ajout du QVBoxLayout des options de partage à la deuxième colonne
        self.column2_layout.addLayout(self.share_options_layout)

        # Ajout du QVBoxLayout des options de langues à la deuxième colonne
        self.column2_layout.addLayout(self.language_options_layout)

        # Ajout d'un QHBoxLayout pour contenir les deux colonnes
        self.top_layout = QHBoxLayout()
        self.top_layout.addLayout(self.column1_layout)
        self.top_layout.addLayout(self.column2_layout)

        # Ajout du QHBoxLayout au QVBoxLayout principal
        self.cleaner_layout.insertLayout(0, self.top_layout)

        # Ajout du QHBoxLayout au QVBoxLayout principal
        self.cleaner_layout.insertLayout(0, self.top_layout)

        # Ajout d'un QHBoxLayout pour contenir la zone de texte et le bouton de recherche
        self.top_layout = QHBoxLayout()
        self.top_layout.addWidget(self.search_text, alignment=Qt.AlignLeft)

        # Ajout du QHBoxLayout au QVBoxLayout principal
        self.cleaner_layout.insertLayout(0, self.top_layout)

        # Création d'un QHBoxLayout pour le bouton de recherche et la barre de progression
        self.button_progress_layout = QHBoxLayout()

        # Ajout d'un espace pour centrer le bouton de recherche
        left_spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.button_progress_layout.addItem(left_spacer)

       # Ajout du bouton de recherche
        self.search_button = QPushButton("Rechercher")
        self.search_button.setFixedSize(100, 30)
        self.search_button.clicked.connect(self.search_article)
        self.button_progress_layout.addWidget(self.search_button) 

        # Ajout d'un espace pour centrer le bouton de recherche
        right_spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.button_progress_layout.addItem(right_spacer)

        # Ajout du QHBoxLayout du bouton de recherche à la QVBoxLayout principale
        self.cleaner_layout.addLayout(self.button_progress_layout)

        # Ajout de la barre de progression
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.cleaner_layout.addWidget(self.progress_bar)


        self.cleaner_widget = QWidget()
        self.cleaner_widget.setLayout(self.cleaner_layout)
        self.stacked_widget.addWidget(self.cleaner_widget)

        # Création de la page Visualisation des données
        self.visualization_layout = QVBoxLayout()

        # Ajoutez un menu déroulant pour sélectionner le type de visualisation
        self.visualization_type_combobox = QComboBox()
        self.visualization_type_combobox.addItem("Répartition du mot-clé par pays")
        self.visualization_type_combobox.addItem("Sites rapportant le plus le mot-clé")
        self.visualization_type_combobox.addItem("Périodes d'utilisation maximale du mot-clé")
        self.visualization_type_combobox.addItem("Zone géographique avec un rapport d'activité")
        self.visualization_layout.addWidget(self.visualization_type_combobox)

        # Connectez la combobox au signal currentIndexChanged
        self.visualization_type_combobox.currentIndexChanged.connect(lambda: self.update_visualization(self.search_input.text()))

        # Créez un widget PlotWidget pour afficher le graphique dans votre application PySide6
        self.plot_widget = PlotWidget()

        # Ajoutez le widget PlotWidget à la mise en page
        self.visualization_layout.addWidget(self.plot_widget)

        self.visualization_widget = QWidget()
        self.visualization_widget.setLayout(self.visualization_layout)
        self.stacked_widget.addWidget(self.visualization_widget)

        # Configuration de la page de veille concurrentielle
        self.competitive_intel_layout = QVBoxLayout()

        # Liste des concurrents
        self.conc_label = QLabel("Concurrents :")
        self.competitive_intel_layout.addWidget(self.conc_label)

        self.conc_list = QComboBox()
        self.conc_list.addItem("Concurrent 1")
        self.conc_list.addItem("Concurrent 2")
        self.conc_list.addItem("Concurrent 3")
        self.competitive_intel_layout.addWidget(self.conc_list)

        # Champ de recherche pour ajouter un concurrent
        self.search_label = QLabel("Ajouter un concurrent :")
        self.competitive_intel_layout.addWidget(self.search_label)

        self.search_input = QLineEdit()
        self.competitive_intel_layout.addWidget(self.search_input)

        self.search_button = QPushButton("Ajouter")
        self.competitive_intel_layout.addWidget(self.search_button)

        # Tableau des informations sur les concurrents
        self.info_table = QTableWidget()
        self.info_table.setRowCount(10)
        self.info_table.setColumnCount(3)
        self.info_table.setHorizontalHeaderLabels(["Titre", "Date", "Source"])
        header = self.info_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.competitive_intel_layout.addWidget(self.info_table)

        # Filtres et bouton de rafraîchissement
        self.filters_layout = QHBoxLayout()
        self.keyword_filter = QLineEdit()
        self.keyword_filter.setPlaceholderText("Filtrer par mots-clés")
        self.filters_layout.addWidget(self.keyword_filter)

        self.source_filter = QLineEdit()
        self.source_filter.setPlaceholderText("Filtrer par source")
        self.filters_layout.addWidget(self.source_filter)

        self.refresh_button = QPushButton("Rafraîchir")
        self.filters_layout.addWidget(self.refresh_button)

        self.competitive_intel_layout.addLayout(self.filters_layout)

        # Ajout de la page de veille concurrentielle au QStackedWidget
        self.competitive_intel_widget = QWidget()
        self.competitive_intel_widget.setLayout(self.competitive_intel_layout)
        self.stacked_widget.addWidget(self.competitive_intel_widget)

        # Configuration du layout principal
        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.menu_widget)

        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.addWidget(self.stacked_widget)
        self.main_layout.addLayout(self.vertical_layout)

        # Configuration du widget central
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

    def update_keywords(self, keywords):
        self.search_text.setText(keywords)

    def create_opacity_animation(self, target_widget, start_value, end_value, duration=300):
        effect = QGraphicsOpacityEffect()
        target_widget.setGraphicsEffect(effect)

        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(duration)
        animation.setStartValue(start_value)
        animation.setEndValue(end_value)
        animation.setEasingCurve(QEasingCurve.OutCubic)
        return animation

def fetch_keyword_data(keyword):
    # Remplacez "your_api_key" par votre clé API SerpAPI
    api_key = "65bd35de40483d3f70e82ed97ba8a86eee6de3fdf4c761ea018f1a133769eb83"
    search_url = f"https://api.serpstack.com/search?access_key={api_key}&query={keyword}"

    response = requests.get(search_url)

    if response.status_code == 200:
        search_results = response.json()

        # Analysez les résultats de la recherche pour extraire les informations nécessaires
        country_count, site_count, date_count = analyze_search_results(search_results)

        # Retournez les données pour afficher un graphique de répartition par pays, sites et dates
        return country_count, site_count, date_count
    else:
        print("Erreur lors de la récupération des données de l'API SerpAPI.")
        return None


def update_visualization(self, keyword):
    visualization_type = self.visualization_type_combobox.currentIndex()

    # Récupérez les données en fonction du mot-clé et du type de visualisation sélectionné
    country_count, site_count, date_count = fetch_keyword_data(keyword)

    if data:
        # Mettez à jour le graphique avec les nouvelles données
        self.ax.clear()
        if visualization_type == 0:  # Répartition par pays
            data = country_count
        elif visualization_type == 1:  # Répartition par sites
            data = site_count
        elif visualization_type == 2:  # Répartition par dates
            data = date_count
        else:
            data = None

        if data:
            self.ax.bar(data.keys(), data.values())
            self.canvas.draw()


def analyze_search_results(search_results):
    country_count = {}
    site_count = {}
    date_count = {}

    for result in search_results['organic_results']:
        # Analyser le pays
        country = result['displayed_link'].split('.')[-1]
        if country in country_count:
            country_count[country] += 1
        else:
            country_count[country] = 1

        # Analyser le site
        site = result['displayed_link'].split('/')[0]
        if site in site_count:
            site_count[site] += 1
        else:
            site_count[site] = 1

        # Analyser la date
        date = result['snippet'].split(' ')[-1]
        if date in date_count:
            date_count[date] += 1
        else:
            date_count[date] = 1

    return country_count, site_count, date_count


def search_article(self):
     # Récupérez le mot-clé saisi par l'utilisateur
    keyword = self.search_input.text()

    # Obtenez les résultats de recherche à l'aide de l'API SerpAPI
    search_results = self.get_search_results(keyword)

    # Analysez les résultats de la recherche pour extraire les informations nécessaires
    data = self.analyze_search_results(search_results)

    # Mettez à jour les visualisations avec les nouvelles données
    self.update_visualizations(data)

def get_search_results(keyword):
    # Remplacez "your_api_key" par votre clé API SerpAPI
    api_key = "65bd35de40483d3f70e82ed97ba8a86eee6de3fdf4c761ea018f1a133769eb83"
    search_url = f"https://api.serpstack.com/search?access_key={api_key}&query={keyword}"

    response = requests.get(search_url)

    if response.status_code == 200:
        search_results = response.json()
        return search_results
    else:
        print("Erreur lors de la récupération des données de l'API SerpAPI.")
        return None


def update_statistics(self):
    # Obtenez le mot-clé saisi par l'utilisateur
    keyword = self.search_input.text()

    # Obtenez les résultats de recherche à l'aide de l'API SerpAPI
    search_results = get_search_results(keyword)

    # Analysez les résultats de la recherche pour extraire les informations nécessaires
    articles = analyze_search_results(search_results)

    # Mettez à jour le modèle de données des articles avec les nouvelles données
    self.article_model.articles = articles

    # Mettez à jour le tableau avec les nouvelles données
    self.table_view.setModel(self.article_model)

    # Préparez les données pour la visualisation
    data = prepare_data_for_plot(articles)

    # Mettez à jour la visualisation avec les nouvelles données
    self.plot_widget.plot(data)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Configuration de la palette de couleurs
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Highlight, QColor(142, 45, 197).lighter())
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)
    app.setStyle("Fusion")
    

    # Affichage de la fenêtre principale
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec())