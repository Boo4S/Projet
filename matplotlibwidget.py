from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MatplotlibWidget(QWidget):
    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(parent)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)


    def update_data(self, keyword_data, website_data, country_data):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.bar(keyword_data.keys(), keyword_data.values())
        ax.set_title('Keyword Data')
        ax.set_xlabel('Keywords')
        ax.set_ylabel('Frequency')
        self.canvas.draw()

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.bar(website_data.keys(), website_data.values())
        ax.set_title('Website Data')
        ax.set_xlabel('Websites')
        ax.set_ylabel('Frequency')
        self.canvas.draw()

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.bar(country_data.keys(), country_data.values())
        ax.set_title('Country Data')
        ax.set_xlabel('Countries')
        ax.set_ylabel('Frequency')
        self.canvas.draw()
