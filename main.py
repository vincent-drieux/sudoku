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

import Sudo
import SudokuWindow
import Widget



def main():
    app = QApplication(sys.argv)
    main_window = SudokuWindow.SudokuMainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
