import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QGridLayout,
    QPushButton,
    QVBoxLayout,
    QMainWindow,
    QMessageBox
)
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import Qt
from random import sample


class ControlsWidget(QWidget):
    def __init__(self, sudoku_widget):
        super().__init__()
        self.sudoku_widget = sudoku_widget
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Ajouter un bouton "Générer une grille"
        generate_button = QPushButton("Générer une grille")
        generate_button.clicked.connect(self.generate_grid)
        layout.addWidget(generate_button)

        # Ajouter un bouton "Sauvegarder"
        save_button = QPushButton("Sauvegarder")
        save_button.clicked.connect(self.save_grid)
        layout.addWidget(save_button)

        # Ajouter un bouton "Importer une grille"
        import_button = QPushButton("Importer une grille")
        import_button.clicked.connect(self.import_grid)
        layout.addWidget(import_button)

        # Ajouter un bouton "Reset"
        reset_button = QPushButton("Reset")
        reset_button.clicked.connect(self.reset_grid)
        layout.addWidget(reset_button)

        # Ajouter un bouton "Solution"
        solution_button = QPushButton("Solution")
        solution_button.clicked.connect(self.show_solution)  # Connexion du bouton à la méthode show_solution
        layout.addWidget(solution_button)

        # Ajouter un bouton "Vérifier"
        verify_button = QPushButton("Vérifier")
        verify_button.clicked.connect(self.verify_solution)
        layout.addWidget(verify_button)

        self.setLayout(layout)

    # générer une nouvelle grille
    def generate_grid(self):
        self.sudoku_widget.clearGrid()
        self.sudoku_widget.generateSudoku()

    # nettoyage de la grille pour réinitialiser et recommencer la partie
    def reset_grid(self):
        self.sudoku_widget.resetGrid()

    # afficher la solution
    def show_solution(self):
    # on repart de la grille d'origine vide
        board = [[self.sudoku_widget.cells[i][j].text() or '.' for j in range(9)] for i in range(9)]
        # si on a résolu on renvoi true
        if self.sudoku_widget.solveSudoku(board):

            for i in range(9):
                for j in range(9):
                    self.sudoku_widget.cells[i][j].setText(board[i][j])
        else:
            # sinon pas de solution, il y a un soucis
            QMessageBox.warning(self, "Pas de solution", "Il n'y a pas de solution pour cette grille.")

    # vérifier la grille terminée par l'utilisateur
    def verify_solution(self):
        # Obtenir la grille complétée par l'utilisateur
        user_completed_board = [[self.sudoku_widget.cells[i][j].text() or '.' for j in range(9)] for i in range(9)]

        # Créer une copie de la grille complétée par l'utilisateur
        user_completed_board_copy = [row[:] for row in user_completed_board]

        # Réinitialiser la grille complétée par l'utilisateur pour obtenir la grille nettoyée
        self.reset_grid()
        curr = [[self.sudoku_widget.cells[i][j].text() or '.' for j in range(9)] for i in range(9)]

        self.sudoku_widget.solveSudoku(curr)

        # Vérifier si la grille nettoyée correspond à la grille complétée par l'utilisateur d'origine
        if ((curr == user_completed_board_copy)):
            QMessageBox.information(self, "Vérification", "La grille est correcte! Bravo!")
        else:
            QMessageBox.information(self, "Vérification", "La grille est incorrecte. Veuillez réessayer.")

    def save_grid(self):
        # Obtenir la grille actuelle
        current_grid = [[self.sudoku_widget.cells[i][j].text() or '.' for j in range(9)] for i in range(9)]

        # Demander à l'utilisateur de choisir un emplacement de fichier pour sauvegarder la grille
        file_path, _ = QFileDialog.getSaveFileName(self, "Sauvegarder la grille", "", "Fichiers texte (*.txt)")

        # Vérifier si l'utilisateur a annulé la sauvegarde
        if file_path:
            # Écrire la grille dans le fichier texte
            with open(file_path, 'w') as file:
                for row in current_grid:
                    file.write(' '.join(row) + '\n')

            QMessageBox.information(self, "Sauvegarde réussie", "La grille a été sauvegardée avec succès!")

    def import_grid(self):
        # Demander à l'utilisateur de choisir un fichier à importer
        file_path, _ = QFileDialog.getOpenFileName(self, "Importer une grille", "", "Fichiers texte (*.txt)")

        # Vérifier si l'utilisateur a annulé l'importation
        if file_path:
            # Lire le contenu du fichier et remplir la grille avec les données
            with open(file_path, 'r') as file:
                lines = file.readlines()
                for i, line in enumerate(lines):
                    numbers = line.strip().split()
                    for j, num in enumerate(numbers):
                        if num != '.':
                            self.sudoku_widget.cells[i][j].setText(num)

