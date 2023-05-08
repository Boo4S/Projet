from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QStackedWidget, QFrame, QPushButton, QLabel, QSizePolicy, QComboBox, QCheckBox



class ArticleTableModel(QAbstractTableModel):
    def __init__(self, articles=None, parent=None):
        super(ArticleTableModel, self).__init__(parent)
        self.articles = articles if articles is not None else []

    def rowCount(self, parent=QModelIndex()):
        return len(self.articles)

    def columnCount(self, parent=QModelIndex()):
        return 4


    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or role != Qt.DisplayRole:
            return None
        article = self.articles[index.row()]
        column = index.column()
        if column == 0:
            return article["date"]
        elif column == 1:
            return article["titre"]
        elif column == 2:
            return article["lien"]
        elif column == 3:
            return article["resumer"]
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole or orientation != Qt.Horizontal:
            return None
        if section == 0:
            return "date"
        elif section == 1:
            return "titre"
        elif section == 2:
            return "lien"
        elif section == 3:
            return "resumer"
        return None

class PlotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def plot(self, data):
        ax = self.figure.add_subplot(111)
        data.plot(kind='bar', x='keyword', y='count', legend=False, ax=ax)
        ax.set_xlabel('Mots-clés')
        ax.set_ylabel('Nombre d\'articles')
        ax.set_title('Nombre d\'articles par mot-clé')
        self.canvas.draw()

def prepare_data_for_plot(articles):
        keywords = []
        for article in articles:
            keywords.extend(article["keywords"])

        keyword_counts = pd.Series(keywords).value_counts().reset_index()
        keyword_counts.columns = ['keyword', 'count']
        
        return keyword_counts
