# -*- coding: utf-8 -*-
import os
import sys
from time import sleep

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from send2trash import send2trash


class Ui_ext_del_Window(object):
    def setupUi(self, ext_del_Window):
        ext_del_Window.setObjectName("body")
        ext_del_Window.resize(369, 188)
        ext_del_Window.setMinimumSize(QtCore.QSize(369, 188))
        ext_del_Window.setMaximumSize(QtCore.QSize(369, 188))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../../IMAGES/favicon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ext_del_Window.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(ext_del_Window)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.path_label = QtWidgets.QLabel(self.centralwidget)
        self.path_label.setAlignment(QtCore.Qt.AlignCenter)
        self.path_label.setObjectName("path_label")
        self.gridLayout.addWidget(self.path_label, 0, 0, 1, 1)
        self.path_entry = QtWidgets.QLineEdit(self.centralwidget)
        self.path_entry.setObjectName("path_entry")
        self.gridLayout.addWidget(self.path_entry, 1, 0, 1, 1)
        self.browse_btn = QtWidgets.QPushButton(self.centralwidget)
        self.browse_btn.setObjectName("browse_btn")
        self.gridLayout.addWidget(self.browse_btn, 1, 1, 1, 1)
        self.ex_label = QtWidgets.QLabel(self.centralwidget)
        self.ex_label.setAlignment(QtCore.Qt.AlignCenter)
        self.ex_label.setObjectName("ex_label")
        self.gridLayout.addWidget(self.ex_label, 2, 0, 1, 1)
        self.ext_entry = QtWidgets.QLineEdit(self.centralwidget)
        self.ext_entry.setObjectName("ext_entry")
        self.gridLayout.addWidget(self.ext_entry, 3, 0, 1, 1)
        self.del_btn = QtWidgets.QPushButton(self.centralwidget)
        self.del_btn.setObjectName("del_btn")
        self.gridLayout.addWidget(self.del_btn, 3, 1, 1, 1)
        ext_del_Window.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(ext_del_Window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 369, 21))
        self.menubar.setObjectName("menubar")

        self.menufile = QtWidgets.QMenu(self.menubar)
        self.menufile.setObjectName("menufile")
        ext_del_Window.setMenuBar(self.menubar)

        self.actionOpen = QtWidgets.QAction(ext_del_Window)
        self.actionOpen.setObjectName("actionOpen")

        self.actionQuit = QtWidgets.QAction(ext_del_Window)
        self.actionQuit.setObjectName("actionQuit")

        self.menufile.addAction(self.actionOpen)
        self.menufile.addAction(self.actionQuit)
        self.menubar.addAction(self.menufile.menuAction())

        self.retranslateUi(ext_del_Window)
        QtCore.QMetaObject.connectSlotsByName(ext_del_Window)
        ext_del_Window.setTabOrder(self.path_entry, self.browse_btn)
        ext_del_Window.setTabOrder(self.browse_btn, self.ext_entry)

    def retranslateUi(self, ext_del_Window):
        _translate = QtCore.QCoreApplication.translate
        ext_del_Window.setWindowTitle(_translate("ext_del_Window", "Delete by extension"))
        self.path_label.setText(_translate("ext_del_Window", "Folder path"))
        self.browse_btn.setText(_translate("ext_del_Window", "Browse"))
        self.ex_label.setText(_translate("ext_del_Window", "Target extension"))
        self.del_btn.setText(_translate("ext_del_Window", "DELETE"))
        self.menufile.setTitle(_translate("ext_del_Window", "File"))
        self.actionOpen.setText(_translate("ext_del_Window", "Open"))
        self.actionQuit.setText(_translate("ext_del_Window", "Quit"))


class DelByEx(QtWidgets.QMainWindow, Ui_ext_del_Window):
    switch_main_win = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        with open("assets/style.css", "r") as file:
            sheet = file.read()
        self.setStyleSheet(sheet)

        # if self.menufile.:
        #     self.pop_message(typ=QMessageBox.Information, text="hovered")

        self.directory = None
        self.target_ext = ""
        self.browse_btn.clicked.connect(self.get_dir)
        self.del_btn.clicked.connect(self.deleter)

        self.path_entry.textChanged.connect(lambda: self.warning_empty(element=self.path_entry))
        self.ext_entry.textChanged.connect(lambda: self.warning_empty(element=self.ext_entry))

        self.actionQuit.triggered.connect(self.close)
        self.actionOpen.triggered.connect(self.get_dir)

    def closeEvent(self, event):
        self.switch_main_win.emit()
        event.accept()

    def get_dir(self):
        self.directory = QFileDialog.getExistingDirectory(self)
        self.path_entry.setText(self.directory)

    def deleter(self):
        if not self.path_entry.text() or self.path_entry.text().isspace():
            self.alert_empty(self.path_entry)
        elif not self.ext_entry.text() or self.ext_entry.text().isspace():
            self.alert_empty(self.ext_entry)
        else:
            self.target_ext = self.ext_entry.text()
            counter = 0
            self.directory = self.path_entry.text()
            if os.path.exists(self.directory):
                files = os.listdir(self.directory)
                os.chdir(self.directory)
                for file in files:
                    if os.path.isfile(file):  # verifie si si il s'agit d'un fichier
                        extension = file.split(".")[-1]
                        if self.target_ext == extension:
                            send2trash(file)
                            counter += 1
                if counter < 1:
                    self.pop_message(typ=QMessageBox.Information,
                                     text="Aucun fichier ayant cette extension n'a été trouvé !!!!")
                    self.ext_entry.setStyleSheet("border: 2px solid red;")

                else:
                    self.pop_message(typ=QMessageBox.Information,
                                     text=f"Opération effectue, {counter} fichier(s) ont été supprimer avec succès")
            else:
                self.pop_message(typ=QMessageBox.Warning, text="Ce répertoire n’existe pas !!!! ")
                self.path_entry.setStyleSheet("border: 2px solid red;")

    def alert_empty(self, element):
        for i in range(3):
            element.setStyleSheet("border: 1px solid black;")
            QtWidgets.QApplication.processEvents()
            sleep(0.1)
            element.setStyleSheet("border: 2px solid red;")
            QtWidgets.QApplication.processEvents()
            sleep(0.1)

    def warning_empty(self, element):
        if not element.text():
            element.setStyleSheet("border: 2px solid red;")
        else:
            element.setStyleSheet("border: 1px solid black;")

    def pop_message(self, typ, text=""):
        msg = QMessageBox()
        msg.setIcon(typ)
        msg.setText(f"{text}")
        msg.setWindowTitle("Notification")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def goto_main_window(self):
        self.switch_main_win.emit()
        self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ext_del_Window = DelByEx()
    ext_del_Window.show()
    sys.exit(app.exec_())
