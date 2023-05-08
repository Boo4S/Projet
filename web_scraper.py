import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QStackedWidget, QFrame, QPushButton, QLabel, QSizePolicy, QComboBox, QCheckBox
from qtawesome import icon
from PySide6.QtCore import QEasingCurve, QPropertyAnimation, QAbstractTableModel, Qt
from PySide6.QtWidgets import QGraphicsOpacityEffect, QProgressBar, QLineEdit, QSpacerItem, QTableView, QTextEdit, QTableWidget, QTableWidgetItem
from serpapi import GoogleSearch
from Fonction import ArticleTableModel, PlotWidget, prepare_data_for_plot
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Interface CCleaner")
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
        self.cleaner_button.enterEvent = lambda event: self.create_opacity_animation(self.cleaner_button, 1, 0.7).start()
        self.cleaner_button.leaveEvent = lambda event: self.create_opacity_animation(self.cleaner_button, 0.7, 1).start()

        self.registry_button = QPushButton(icon('fa5s.archive', color='white'), "Vue d'ensemble")
        self.registry_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.registry_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        self.registry_button.setStyleSheet(button_style)
        self.menu_layout.addWidget(self.registry_button)
        self.cleaner_button.enterEvent = lambda event: self.create_opacity_animation(self.cleaner_button, 1, 0.7).start()
        self.cleaner_button.leaveEvent = lambda event: self.create_opacity_animation(self.cleaner_button, 0.7, 1).start()

        self.tools_button = QPushButton(icon('fa5s.toolbox', color='white'), "Stats")
        self.tools_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.tools_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        self.tools_button.setStyleSheet(button_style)
        self.menu_layout.addWidget(self.tools_button)
        self.cleaner_button.enterEvent = lambda event: self.create_opacity_animation(self.cleaner_button, 1, 0.7).start()
        self.cleaner_button.leaveEvent = lambda event: self.create_opacity_animation(self.cleaner_button, 0.7, 1).start()

        self.options_button = QPushButton(icon('fa5s.cogs', color='white'), "Concurrents")
        self.options_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        self.options_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        self.options_button.setStyleSheet(button_style)
        self.menu_layout.addWidget(self.options_button)
        self.cleaner_button.enterEvent = lambda event: self.create_opacity_animation(self.cleaner_button, 1, 0.7).start()
        self.cleaner_button.leaveEvent = lambda event: self.create_opacity_animation(self.cleaner_button, 0.7, 1).start()

        # Configuration de la page RESOSearch
        self.cleaner_layout = QVBoxLayout()

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
        self.language_combobox.addItem("Anglais")
        self.language_combobox.addItem("Français")
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

        # Création de la page Vue d'ensemble
        self.overview_layout = QVBoxLayout()

        # Configuration de la page Vue d'ensemble
        self.article_model = ArticleTableModel()
        self.article_table = QTableView()
        self.article_table.setModel(self.article_model)
        self.overview_layout.addWidget(self.article_table)

        self.overview_widget = QWidget()
        self.overview_widget.setLayout(self.overview_layout)
        self.stacked_widget.addWidget(self.overview_widget)

        # Ajoutez ces lignes pour définir l'attribut stats_widget et stats_layout
        self.stats_widget = QWidget()
        self.stats_layout = QVBoxLayout()

        # Configuration de la page Stats
        self.plot_widget = PlotWidget()
        self.stats_layout.addWidget(self.plot_widget)
        self.stats_widget.setLayout(self.stats_layout)
        self.stacked_widget.addWidget(self.stats_widget)

        # Configuration de la page Options
        self.options_page = QLabel("Bienvenue sur la page Options")
        self.options_page.setAlignment(Qt.AlignCenter)
        self.stacked_widget.addWidget(self.options_page)

        # Configuration du layout principal
        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.menu_widget)

        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.addWidget(self.stacked_widget)
        self.main_layout.addLayout(self.vertical_layout)

        # Configuration du widget central
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

    def update_statistics(self):
        keyword_counts = prepare_data_for_plot(self.articles)
        self.plot_widget.plot(keyword_counts)


    def create_opacity_animation(self, target_widget, start_value, end_value, duration=300):
        effect = QGraphicsOpacityEffect()
        target_widget.setGraphicsEffect(effect)

        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(duration)
        animation.setStartValue(start_value)
        animation.setEndValue(end_value)
        animation.setEasingCurve(QEasingCurve.OutCubic)
        return animation

    def search_article(self):
    # Effectuez la recherche d'articles ici et stockez les résultats dans `search_results`
        search_results = [
            {"date": "07/05/2023", "titre": "Article 1", "lien": "https://example.com/article1", "resumer": "Résumé de l'article 1"},
            {"date": "07/05/2023", "titre": "Article 2", "lien": "https://example.com/article2", "resumer": "Résumé de l'article 2"},
        ]

        # Mettez à jour le modèle de données avec les résultats de la recherche
        self.article_model.articles = search_results
        self.article_model.layoutChanged.emit()
        self.update_statistics()



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