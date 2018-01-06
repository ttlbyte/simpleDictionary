#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module implementing MainWindow."""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIcon
from Ui_ui_main import Ui_MainWindow
from query import translation
import webbrowser


class MainWindow(QMainWindow, Ui_MainWindow):

    """Class documentation goes here."""

    def __init__(self, parent=None):
        """
        Constructor.

        @param parent reference to the parent widget
        @type QWidget

        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.move(300, 200)
        self.setWindowIcon(QIcon('./icon.png'))
        self.actionExit.triggered.connect(self.close)
        self.func = 0
        self.actionAbout_author.triggered.connect(self.about)
        self.comboBox.activated.connect(self.function_selected)

    def function_selected(self, index):
        self.func = index

    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        """Slot documentation goes here."""
        # TODO: not implemented yet
        word = '-'.join(self.lineEdit.text().split())
        results = translation(word, func=self.func)
        if results.status == 1:
            self.textBrowser.setHtml(QtCore.QCoreApplication.translate("MainWindow", results.return_result()))
        else:
            self.show_error(results.error_message)

    def about(self):
        url = 'http://dftcode.me'
        webbrowser.open(url)

    def show_error(self, mess_str):
        self.error_dialog = QtWidgets.QErrorMessage()
        self.error_dialog.showMessage(mess_str)
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())
