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
from PyQt5.QtCore import Qt
from random import sample


class Sudoku(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):
        grid = QGridLayout()
        grid.setSpacing(0)  # Aucun espacement entre les widgets
        self.setLayout(grid)

        self.cells = [[None for _ in range(9)] for _ in range(9)]

        # gestion de la grille vide, placement, taille, boutons etc
        for i in range(9):
            for j in range(9):
                button = QPushButton()
                button.setFixedSize(50, 50)
                button.clicked.connect(lambda _, i=i, j=j: self.onButtonClick(i, j))  # Connecter le signal clicked
                # pour que gestion particulière pour faire une disposition en blocs de 3
                if (i == 2 or i == 5):
                    if (j == 2 or j == 5):
                        button.setStyleSheet(
                            "QPushButton { border: 2px solid black; font-size: 20px; margin: 0px; padding: 0px; background-color: white; margin-bottom : 3px; margin-right : 3px;}" +
                            "QPushButton:pressed { background-color: #A9A9A9; }" +
                            "QPushButton:flat { margin: 0; padding: 0; }"  # Supprimer les marges pour les boutons plats
                        )
                    else:
                        button.setStyleSheet(
                            "QPushButton { border: 2px solid black; font-size: 20px; margin: 0px; padding: 0px; background-color: white; margin-bottom : 3px;}" +
                            "QPushButton:pressed { background-color: #A9A9A9; }" +
                            "QPushButton:flat { margin: 0; padding: 0; }"  # Supprimer les marges pour les boutons plats
                        )
                elif (j == 2 or j == 5):
                    button.setStyleSheet(
                        "QPushButton { border: 2px solid black; font-size: 20px; margin: 0px; padding: 0px; background-color: white; margin-right : 3px;}" +
                        "QPushButton:pressed { background-color: #A9A9A9; }" +
                        "QPushButton:flat { margin: 0; padding: 0; }"  # Supprimer les marges pour les boutons plats
                    )
                else:
                    button.setStyleSheet(
                        "QPushButton { border: 2px solid black; font-size: 20px; margin: 0px; padding: 0px; background-color: white;}" +
                        "QPushButton:pressed { background-color: #A9A9A9; }" +
                        "QPushButton:flat { margin: 0; padding: 0; }"  # Supprimer les marges pour les boutons plats
                    )

                self.cells[i][j] = button
                grid.addWidget(button, i, j)

        # Ne pas remplir la grille au démarrage
        self.clearGrid()

    # nettoyer la grille
    def clearGrid(self):
        for i in range(9):
            for j in range(9):
                self.cells[i][j].setText("")
                self.cells[i][j].setEnabled(True)

    # générer une grille de sudoku

    def generateSudoku(self):
        # Générer une grille Sudoku aléatoire et l'afficher
        example_board = self.generate_random_sudoku()

        for i in range(9):
            for j in range(9):
                if example_board[i][j] != 0:
                    self.cells[i][j].setText(str(example_board[i][j]))
                    self.cells[i][j].setEnabled(False)

    def resetGrid(self):
        for i in range(9):
            for j in range(9):
                if self.cells[i][j].isEnabled():
                    self.cells[i][j].setText("")

    # selection de la case par l'utilisateur
    def onButtonClick(self, i, j):
        button = self.cells[i][j]
        if button.isEnabled():
            self.active_cell = (i, j)
            self.setFocus()  # Donner le focus à la fenêtre principale pour permettre à l'utilisateur de saisir un numéro

    # évennement, ajouter un numéro, ou en enlever un
    def keyPressEvent(self, event):
        if hasattr(self, 'active_cell'):
            key = event.key()
            if Qt.Key_0 <= key <= Qt.Key_9:  # Vérifier si la touche appuyée est un chiffre de 0 à 9
                num = key - Qt.Key_0
                self.cells[self.active_cell[0]][self.active_cell[1]].setText(str(num))
            elif key == Qt.Key_Backspace or key == Qt.Key_Delete:
                self.cells[self.active_cell[0]][self.active_cell[1]].setText("")

    # attention, triche il y a !
    # --> je ne garantie pas une solution unique (ce n'est donc pas une "vraie" grille de sudoku
    # --> pour avoir cette garantie, il faudrait fixer un nombre de valeurs à enlever dans la grille complète (nb > 17 d'après la preuvre mathématiques)
    # --> ensuite boucler, tester les différentes solutions, si il en existe 1 et 1 seule, ok on a convergé
    # --> sinon, rajouter un numéro qui était enlevé, et recommencer
    def generate_random_sudoku(self):
        # Générer une grille Sudoku aléatoire valide
        base = 3
        side = base * base

        # Générer la grille de départ
        def pattern(r, c):
            return (base * (r % base) + r // base + c) % side

        def shuffle(s):
            return sample(s, len(s))

        rBase = range(base)
        rows = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase)]
        cols = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase)]
        nums = shuffle(range(1, base * base + 1))

        # Générer la grille de départ
        board = [[nums[pattern(r, c)] for c in cols] for r in rows]

        # Masquer quelques nombres pour créer une grille Sudoku incomplète
        squares = side * side
        empties = squares * 3 // 4
        for p in sample(range(squares), empties):
            board[p // side][p % side] = 0

        return board


    # test résolution



    # résoudre une grille de sudoku, backtracking classique
    def solveSudoku(self, board):
        if not self.isValidSudoku(board):
            return False

        empty_cell = self.findEmptyCell(board)
        if not empty_cell:
            return True  # La grille est déjà complète

        row, col = empty_cell

        for num in range(1, 10):
            if self.isValidPlacement(board, row, col, str(num)):
                board[row][col] = str(num)
                if self.solveSudoku(board):
                    return True
                board[row][col] = "."  # Retour en arrière si la solution n'est pas valide

        return False

    def isValidSudoku(self, board):
        # Vérifier les lignes
        for row in board:
            if not self.isValidSet(row):
                return False

        # Vérifier les colonnes
        for col in range(9):
            column = [board[row][col] for row in range(9)]
            if not self.isValidSet(column):
                return False

        # Vérifier les boîtes 3x3
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                box = [board[row][col] for row in range(i, i + 3) for col in range(j, j + 3)]
                if not self.isValidSet(box):
                    return False

        return True

    def isValidSet(self, nums):
        seen = set()
        for num in nums:
            if num != ".":
                if num in seen:
                    return False
                seen.add(num)
        return True

    def findEmptyCell(self, board):
        for row in range(9):
            for col in range(9):
                if board[row][col] == ".":
                    return row, col
        return None

    def isValidPlacement(self, board, row, col, num):
        # Vérifier la ligne
        if num in board[row]:
            return False

        # Vérifier la colonne
        if num in [board[i][col] for i in range(9)]:
            return False

        # Vérifier la boîte 3x3
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if board[i][j] == num:
                    return False

        return True