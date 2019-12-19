from PyQt5.QtWidgets import QApplication
import sys
import mainwindow as mw

__author__      =   "Jose Ramon Lozano Pinilla, Javier Nogales Fernandez"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = mw.MainWindow()
    w.MainWindow.show()
    app.exec_()