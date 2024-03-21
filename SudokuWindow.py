import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QGridLayout,
    QPushButton,
    QVBoxLayout,
    QMainWindow,
    QMessageBox,

)
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtCore import Qt
from random import sample

import Sudo
import Widget

class SudokuMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sudoku")
        self.setGeometry(100, 100, 400, 500)  # Définir la taille de la fenêtre principale

        # Définir l'icône de la fenêtre
        icon_path = "C:/Users/vince/Downloads/migraine-ophtalmique.jpg"  # Remplacez cela par le chemin de votre image
        self.setWindowIcon(QIcon(icon_path))  # Importez également QIcon depuis PyQt5.QtGui

        # Créer un widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Créer une mise en page verticale pour le widget central
        layout = QVBoxLayout(central_widget)

        # Ajouter le widget Sudoku
        sudoku_widget = Sudo.Sudoku()
        layout.addWidget(sudoku_widget)

        # Ajouter le widget de contrôles
        controls_widget = Widget.ControlsWidget(sudoku_widget)
        layout.addWidget(controls_widget)

        self.create_menu_bar()  # Créer la barre de menu

    def create_menu_bar(self):
        # Créer un nouvel élément de menu
        menu_bar = self.menuBar()

        # Créer un menu déroulant
        options_menu = menu_bar.addMenu("Options")

        # Ajouter des actions au menu déroulant
        action_rules = QAction("Règles du Sudoku", self)
        action_rules.triggered.connect(self.show_sudoku_rules)  # Connectez l'action à une fonction
        options_menu.addAction(action_rules)

    def show_sudoku_rules(self):
        # Afficher une boîte de dialogue QMessageBox avec les règles du Sudoku
        rules_text = "Les règles du Sudoku sont simples :\n" \
                     "- Remplissez la grille avec des chiffres de 1 à 9\n" \
                     "- Chaque ligne, chaque colonne et chaque région 3x3 doit contenir tous les chiffres de 1 à 9 sans répétition\n" \
                     "- Une grille de Sudoku complète contient 81 chiffres\n" \
                     "- Certains chiffres sont déjà donnés au départ pour aider à démarrer\n"
        QMessageBox.information(self, "Règles du Sudoku", rules_text)