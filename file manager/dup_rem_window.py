# -*- coding: utf-8 -*-
import hashlib
import os
import sys
from time import sleep

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from send2trash import send2trash


class Ui_dup_del_Window(object):
    def setupUi(self, dup_del_Window):
        dup_del_Window.setObjectName("body")
        dup_del_Window.resize(369, 188)
        dup_del_Window.setMinimumSize(QtCore.QSize(369, 188))
        dup_del_Window.setMaximumSize(QtCore.QSize(369, 188))

        self.centralwidget = QtWidgets.QWidget(dup_del_Window)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.path_label = QtWidgets.QLabel(self.centralwidget)
        self.path_label.setMaximumSize(QtCore.QSize(16777215, 23))
        self.path_label.setAlignment(QtCore.Qt.AlignCenter)
        self.path_label.setObjectName("path_label")
        self.gridLayout.addWidget(self.path_label, 0, 0, 1, 1)
        self.path_entry = QtWidgets.QLineEdit(self.centralwidget)
        self.path_entry.setInputMask("")
        self.path_entry.setClearButtonEnabled(False)
        self.path_entry.setObjectName("path_entry")
        self.gridLayout.addWidget(self.path_entry, 1, 0, 1, 1)
        self.browse_btn = QtWidgets.QPushButton(self.centralwidget)
        self.browse_btn.setObjectName("browse_btn")
        self.gridLayout.addWidget(self.browse_btn, 1, 1, 1, 1)
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setMaximumSize(QtCore.QSize(16777215, 23))
        self.checkBox.setObjectName("checkBox")
        self.gridLayout.addWidget(self.checkBox, 2, 0, 1, 1)
        self.pattern_label = QtWidgets.QLabel(self.centralwidget)
        self.pattern_label.setMaximumSize(QtCore.QSize(16777215, 23))
        self.pattern_label.setAlignment(QtCore.Qt.AlignCenter)
        self.pattern_label.setObjectName("pattern_label")
        self.gridLayout.addWidget(self.pattern_label, 3, 0, 1, 1)
        self.pattern_entry = QtWidgets.QLineEdit(self.centralwidget)
        self.pattern_entry.setObjectName("pattern_entry")
        self.gridLayout.addWidget(self.pattern_entry, 4, 0, 1, 1)
        self.del_btn = QtWidgets.QPushButton(self.centralwidget)
        self.del_btn.setObjectName("del_btn")
        self.gridLayout.addWidget(self.del_btn, 4, 1, 1, 1)
        dup_del_Window.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(dup_del_Window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 369, 21))
        self.menubar.setObjectName("menubar")
        dup_del_Window.setMenuBar(self.menubar)

        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")

        self.actionOpen = QtWidgets.QAction(dup_del_Window)
        self.actionOpen.setObjectName("actionOpen")
        self.actionQuit = QtWidgets.QAction(dup_del_Window)
        self.actionQuit.setObjectName("actionQuit")

        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionQuit)

        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(dup_del_Window)
        QtCore.QMetaObject.connectSlotsByName(dup_del_Window)

    def retranslateUi(self, dup_del_Window):
        _translate = QtCore.QCoreApplication.translate
        dup_del_Window.setWindowTitle(_translate("dup_del_Window", "Duplicated file remover"))
        self.path_label.setText(_translate("dup_del_Window", "Folder path"))
        self.browse_btn.setText(_translate("dup_del_Window", "Browse"))
        self.checkBox.setText(_translate("dup_del_Window", "Use pattern"))
        self.pattern_label.setText(_translate("dup_del_Window", "Pattern"))
        self.del_btn.setText(_translate("dup_del_Window", "DELETE"))
        self.menuFile.setTitle(_translate("dup_del_Window", "File"))
        self.actionOpen.setText(_translate("dup_del_Window", "Open"))
        self.actionQuit.setText(_translate("dup_del_Window", "Quit"))


class Del_dbles(QtWidgets.QMainWindow, Ui_dup_del_Window):
    switch_main_win = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("assets/favicon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        with open("assets/style.css", "r") as file:
            sheet = file.read()
        self.setStyleSheet(sheet)

        self.directory = None
        self.setupUi(self)

        self.browse_btn.clicked.connect(self.get_dir)
        self.del_btn.clicked.connect(self.deleter)

        self.path_entry.textChanged.connect(lambda: self.warning_empty(element=self.path_entry))
        self.pattern_entry.textChanged.connect(lambda: self.warning_empty(element=self.pattern_entry))
        self.pattern_entry.setStyleSheet("background-color: rgb(66, 65, 65);\nborder-style: none;")

        self.pattern_label.setEnabled(False)
        self.pattern_entry.setEnabled(False)
        self.pattern_label.setStyleSheet("color: rgb(66, 65, 65);\nborder-style: none;")

        self.checkBox.clicked.connect(self.chexBox_checked)

        self.actionQuit.triggered.connect(self.close)
        self.actionOpen.triggered.connect(self.get_dir)

    def closeEvent(self, event):
        self.switch_main_win.emit()
        event.accept()
        self.close()
    def get_dir(self):
        self.directory = QFileDialog.getExistingDirectory(self)
        self.path_entry.setText(self.directory)

    def deleter(self):
        global txt
        global alrt
        if not self.path_entry.text() or self.path_entry.text().isspace():
            self.alert_empty(self.path_entry)
        else:
            counter = 0
            alrt = False
            self.directory = self.path_entry.text()
            if os.path.exists(self.directory):
                files = os.listdir(self.directory)
                os.chdir(self.directory)
                unique = dict()
                files = sorted(files, reverse=True)
                for file in files:

                    if os.path.isfile(file):
                        filename = file[:-len(file.split(".")[-1]) - 1]

                        if self.checkBox.isChecked():
                            alrt = True
                            dble_pattern = self.pattern_entry.text()
                            txt = f"fichier(s) ayant \"{dble_pattern}\" "

                            if not dble_pattern or dble_pattern.isspace():
                                self.alert_empty(self.pattern_entry)
                                return
                            else:

                                if dble_pattern.upper() in filename.upper():  # verifie si si il s'agit d'un fichier
                                    send2trash(file)
                                    counter += 1

                        else:
                            txt = "doublon(s)"

                            fileHash = hashlib.md5(open(file, 'rb').read()).hexdigest()

                            if fileHash not in unique:
                                unique[fileHash] = file

                            else:
                                send2trash(file)
                                counter += 1
                if counter < 1:
                    self.pop_message(wIco="assets/warn.png", title="Info", typ=QMessageBox.Information,
                                     text=f"Aucun {txt} n'a été trouvé !!!!")
                    if alrt:
                        self.pattern_entry.setStyleSheet("border: 2px solid red;")
                else:
                    self.pop_message(typ=QMessageBox.Information,
                                     text=f"Opération effectue, {counter} {txt} ont été supprimer avec succès")
            else:
                self.pop_message(wIco="assets/warn.png", title="Avertissement", typ=QMessageBox.Warning,
                                 text="Ce répertoire n’existe pas !!!!")
                self.path_entry.setStyleSheet("border: 2px solid red;")

    def chexBox_checked(self):
        if self.checkBox.isChecked():
            self.pattern_label.setEnabled(True)
            self.pattern_label.setStyleSheet("color: white;")
            self.pattern_entry.setEnabled(True)
            self.pattern_entry.setStyleSheet("")
        else:
            self.pattern_label.setEnabled(False)
            self.pattern_label.setStyleSheet("color: rgb(66, 65, 65);\nborder-style: none;")

            self.pattern_entry.setEnabled(False)
            self.pattern_entry.setText("")
            self.pattern_entry.setStyleSheet("background-color: rgb(66, 65, 65);\nborder-style: none;")

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

    def pop_message(self, typ, wIco, title="Notification", text=""):
        msg = QMessageBox()
        msg.setIcon(typ)
        msg.setText(f"{text}")
        msg.setWindowTitle(title)
        msg.setStandardButtons(QMessageBox.Ok)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(wIco), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        msg.setWindowIcon(icon)

        msg.exec_()

    def goto_main_window(self):
        self.switch_main_win.emit()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Del_dbles()
    ui.show()
    sys.exit(app.exec_())
