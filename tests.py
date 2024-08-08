# -*- coding: utf-8 -*-
import hashlib
import os
import shutil
import sys
from time import sleep

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from send2trash import send2trash


def is_window_open(window_class):
    appl = QtWidgets.QApplication.instance()
    for widget in appl.topLevelWidgets():
        if isinstance(widget, window_class):
            return True
    return False


def resource_path(relative_path):
    """get the absolute path to resource"""
    try:
        # Pyinstaller creates a temp folder and stores in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def warning_empty(element):
    if not element.text():
        element.setStyleSheet("border: 2px solid red;")
    else:
        element.setStyleSheet("border: 1px solid black;")


def alert_empty(element):
    for i in range(3):
        element.setStyleSheet("border: 1px solid black;")
        QtWidgets.QApplication.processEvents()
        sleep(0.1)
        element.setStyleSheet("border: 2px solid red;")
        QtWidgets.QApplication.processEvents()
        sleep(0.1)
    QtWidgets.QApplication.processEvents()


def pop_message(typ, wIco, title="Info", text=""):
    QtWidgets.QApplication.processEvents()
    msg = QMessageBox()
    msg.setIcon(typ)
    msg.setText(f"{text}")
    msg.setWindowTitle(title)
    msg.setStandardButtons(QMessageBox.Ok)

    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(resource_path(wIco)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    msg.setWindowIcon(icon)
    msg.exec_()


class Ui_main(object):
    def setupUi(self, main):
        main.setObjectName("body")
        main.resize(369, 188)
        main.setMinimumSize(QtCore.QSize(369, 188))
        main.setMaximumSize(QtCore.QSize(369, 188))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("assets/favicon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        main.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(main)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.ok_btn = QtWidgets.QPushButton(self.centralwidget)
        self.ok_btn.setObjectName("ok_btn")
        self.gridLayout.addWidget(self.ok_btn, 1, 0, 1, 2)

        self.windowslist = QtWidgets.QComboBox(self.centralwidget)
        self.windowslist.setObjectName("windowslist")
        self.gridLayout.addWidget(self.windowslist, 0, 0, 1, 2)

        main.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(main)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 369, 21))
        self.menubar.setObjectName("menubar")
        main.setMenuBar(self.menubar)

        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")

        self.actionGoTo = QtWidgets.QMenu(main)
        self.actionGoTo.setObjectName("actionOpen")

        self.actionFileRanger = QtWidgets.QAction(main)
        self.actionFileRanger.setObjectName("actionFileRanger")
        self.actionFileDeleter = QtWidgets.QAction(main)
        self.actionFileDeleter.setObjectName("actionFileDeleter")
        self.actionDuplicatedFilesRemover = QtWidgets.QAction(main)
        self.actionDuplicatedFilesRemover.setObjectName("actionDuplicatedFilesRemover")

        self.actionGoTo.addAction(self.actionFileRanger)
        self.actionGoTo.addAction(self.actionFileDeleter)
        self.actionGoTo.addAction(self.actionDuplicatedFilesRemover)

        self.actionQuit = QtWidgets.QAction(main)
        self.actionQuit.setObjectName("actionQuit")

        self.menuFile.addAction(self.actionGoTo.menuAction())
        self.menuFile.addAction(self.actionQuit)

        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(main)
        QtCore.QMetaObject.connectSlotsByName(main)
        main.setTabOrder(self.windowslist, self.ok_btn)

    def retranslateUi(self, main):
        _translate = QtCore.QCoreApplication.translate
        main.setWindowTitle(_translate("main", "File manager"))
        self.ok_btn.setText(_translate("main", "OK"))
        self.menuFile.setTitle(_translate("main", "file"))

        self.actionGoTo.setTitle(_translate("main", "Go to"))
        self.actionFileRanger.setText(_translate("main", "File ranger"))
        self.actionFileDeleter.setText(_translate("main", "File deleter"))
        self.actionDuplicatedFilesRemover.setText(_translate("main", "Duplicated files remover"))

        self.actionQuit.setText(_translate("main", "Exit"))


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


class Ui_RangeWindow(object):
    def setupUi(self, RangeWindow):
        RangeWindow.setObjectName("body")
        # RangeWindow.resize(412, 174)

        RangeWindow.resize(369, 188)
        RangeWindow.setMinimumSize(QtCore.QSize(0, 0))
        RangeWindow.setMaximumSize(QtCore.QSize(412, 225))
        RangeWindow.setAcceptDrops(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("assets/favicon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        RangeWindow.setWindowIcon(icon)
        RangeWindow.setWindowOpacity(1.0)
        self.centralwidget = QtWidgets.QWidget(RangeWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 1, 0, 1, 2)

        self.browse_btn = QtWidgets.QPushButton(self.centralwidget)
        self.browse_btn.setObjectName("browse_btn")
        self.gridLayout.addWidget(self.browse_btn, 1, 2, 1, 1)

        self.range_btn = QtWidgets.QPushButton(self.centralwidget)
        self.range_btn.setObjectName("range_btn")
        self.gridLayout.addWidget(self.range_btn, 7, 2, 1, 1)

        self.name_pat = QtWidgets.QLineEdit(self.centralwidget)
        self.name_pat.setObjectName("name_pat")
        self.gridLayout.addWidget(self.name_pat, 7, 1, 1, 1)

        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setObjectName("comboBox")
        self.gridLayout.addWidget(self.comboBox, 3, 0, 3, 2)

        self.name_pat_label = QtWidgets.QLabel(self.centralwidget)
        self.name_pat_label.setEnabled(True)
        self.name_pat_label.setAlignment(QtCore.Qt.AlignCenter)
        self.name_pat_label.setObjectName("name_pat_label")
        self.gridLayout.addWidget(self.name_pat_label, 6, 1, 1, 1)

        self.rgn_mde_label = QtWidgets.QLabel(self.centralwidget)
        self.rgn_mde_label.setAlignment(QtCore.Qt.AlignCenter)
        self.rgn_mde_label.setObjectName("rgn_mde_label")
        self.gridLayout.addWidget(self.rgn_mde_label, 2, 0, 1, 2)

        self.path_label = QtWidgets.QLabel(self.centralwidget)
        self.path_label.setAlignment(QtCore.Qt.AlignCenter)
        self.path_label.setObjectName("path_label")
        self.gridLayout.addWidget(self.path_label, 0, 0, 1, 2)
        RangeWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(RangeWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 412, 21))
        self.menubar.setObjectName("menubar")
        RangeWindow.setMenuBar(self.menubar)

        self.menufile = QtWidgets.QMenu(self.menubar)
        self.menufile.setObjectName("menufile")
        RangeWindow.setMenuBar(self.menubar)

        self.actionOpen = QtWidgets.QAction(RangeWindow)
        self.actionOpen.setObjectName("actionOpen")

        self.actionQuit = QtWidgets.QAction(RangeWindow)
        self.actionQuit.setObjectName("actionQuit")

        self.menufile.addAction(self.actionOpen)
        self.menufile.addAction(self.actionQuit)
        self.menubar.addAction(self.menufile.menuAction())

        self.retranslateUi(RangeWindow)
        QtCore.QMetaObject.connectSlotsByName(RangeWindow)
        RangeWindow.setTabOrder(self.lineEdit, self.browse_btn)
        RangeWindow.setTabOrder(self.browse_btn, self.comboBox)

    def retranslateUi(self, RangeWindow):
        _translate = QtCore.QCoreApplication.translate
        RangeWindow.setWindowTitle(_translate("RangeWindow", "File ranger"))
        self.browse_btn.setText(_translate("RangeWindow", "Browse"))
        self.range_btn.setText(_translate("RangeWindow", "RANGE"))
        self.name_pat_label.setText(_translate("RangeWindow", "Name pattern"))
        self.rgn_mde_label.setText(_translate("RangeWindow", "Range mode"))
        self.path_label.setText(_translate("RangeWindow", "Folder path"))

        self.menufile.setTitle(_translate("RangeWindow", "File"))
        self.actionOpen.setText(_translate("RangeWindow", "Open"))
        self.actionQuit.setText(_translate("RangeWindow", "Quit"))


# **********************************************************************************************************************
class Main(QtWidgets.QMainWindow, Ui_main):
    switch_classer_win = QtCore.pyqtSignal()
    switch_deleter_win = QtCore.pyqtSignal()
    switch_remover_win = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowOpacity(0.9)

        with open("assets/style.css", "r") as file:
            sheet = file.read()
        self.setStyleSheet(sheet)

        self.windowslist.addItems(["File ranger", "File deleter", "Duplicated files remover"])

        self.ok_btn.clicked.connect(self.goto_sub_window)

        self.actionFileRanger.triggered.connect(self.switch_classer_win.emit)
        self.actionFileDeleter.triggered.connect(self.switch_deleter_win.emit)
        self.actionDuplicatedFilesRemover.triggered.connect(self.switch_remover_win.emit)

        self.actionQuit.triggered.connect(self.close)

    def goto_sub_window(self):
        match self.windowslist.currentText():
            case "File ranger":
                self.switch_classer_win.emit()
            case "File deleter":
                self.switch_deleter_win.emit()
            case "Duplicated files remover":
                self.switch_remover_win.emit()

    def closeEvent(self, event):
        reponse = QMessageBox.question(self, 'Confirmation', "Êtes-vous sûr de vouloir quitter ?",
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reponse == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


class DelByEx(QtWidgets.QMainWindow, Ui_ext_del_Window):
    switch_main_win = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        with open("assets/style.css", "r") as file:
            sheet = file.read()
        self.setStyleSheet(sheet)

        self.directory = None
        self.target_ext = ""
        self.browse_btn.clicked.connect(self.get_dir)
        self.del_btn.clicked.connect(self.deleter)

        self.path_entry.textChanged.connect(lambda: warning_empty(element=self.path_entry))
        self.ext_entry.textChanged.connect(lambda: warning_empty(element=self.ext_entry))

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
            alert_empty(self.path_entry)
        elif not self.ext_entry.text() or self.ext_entry.text().isspace():
            alert_empty(self.ext_entry)
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
                    pop_message(typ=QMessageBox.Information,
                                wIco='D:\\DATAS\\Pycharm_projet\\BOOKS\\apps\\file_manager\\assets\\info.ico',
                                text="Aucun fichier ayant cette extension n'a été trouvé !!!!")
                    self.ext_entry.setStyleSheet("border: 2px solid red;")

                else:
                    pop_message(typ=QMessageBox.Information,
                                wIco='D:\\DATAS\\Pycharm_projet\\BOOKS\\apps\\file_manager\\assets\\info.ico',
                                text=f"Opération effectue, {counter} fichier(s) ont été supprimer avec succès")
            else:
                pop_message(typ=QMessageBox.Warning,
                            wIco='D:\\DATAS\\Pycharm_projet\\BOOKS\\apps\\file_manager\\assets\\warn.png',
                            title="Avertissement",
                            text="Ce répertoire n’existe pas !!!! ")
                self.path_entry.setStyleSheet("border: 2px solid red;")

    def goto_main_window(self):
        self.switch_main_win.emit()
        self.close()


class Del_dbles(QtWidgets.QMainWindow, Ui_dup_del_Window):
    switch_main_win = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QApplication.processEvents()
        super().__init__()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(resource_path("assets/favicon.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        with open(resource_path('assets/style.css'), "r") as file:
            sheet = file.read()
        self.setStyleSheet(sheet)

        self.directory = None
        self.setupUi(self)

        self.browse_btn.clicked.connect(self.get_dir)
        self.del_btn.clicked.connect(self.deleter)

        self.path_entry.textChanged.connect(lambda: warning_empty(element=self.path_entry))
        self.pattern_entry.textChanged.connect(lambda: warning_empty(element=self.pattern_entry))
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
        QtWidgets.QApplication.processEvents()

    def deleter(self):
        global txt
        global alrt
        if not self.path_entry.text() or self.path_entry.text().isspace():
            alert_empty(self.path_entry)
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
                                alert_empty(self.pattern_entry)
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
                    pop_message(wIco='D:\\DATAS\\Pycharm_projet\\BOOKS\\apps\\file_manager\\assets\\info.ico',
                                typ=QMessageBox.Information,
                                text=f"Aucun {txt} n'a été trouvé !!!!")
                    if alrt:
                        self.pattern_entry.setStyleSheet("border: 2px solid red;")
                else:
                    pop_message(typ=QMessageBox.Information,
                                wIco='D:\\DATAS\\Pycharm_projet\\BOOKS\\apps\\file_manager\\assets\\info.ico',
                                text=f"Opération effectue, {counter} {txt} ont été supprimer avec succès")
            else:
                pop_message(wIco='D:\\DATAS\\Pycharm_projet\\BOOKS\\apps\\file_manager\\assets\\warn.png',
                            title="Avertissement",
                            typ=QMessageBox.Warning,
                            text="Ce répertoire n’existe pas !!!!")
                self.path_entry.setStyleSheet("border: 2px solid red;")
        QtWidgets.QApplication.processEvents()

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

    def goto_main_window(self):
        self.switch_main_win.emit()


class RangeWndow(QtWidgets.QMainWindow, Ui_RangeWindow):
    switch_main_win = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.directory = None
        self.setupUi(self)
        with open("assets/style.css", "r") as file:
            sheet = file.read()
        self.setStyleSheet(sheet)

        self.comboBox.addItems(["Range by extension", "Range by name"])
        self.comboBox.currentIndexChanged.connect(self.on_combobox_changed)

        self.browse_btn.clicked.connect(self.get_dir)
        self.range_btn.clicked.connect(self.ranger)

        self.name_pat_label.setEnabled(False)
        self.name_pat.setEnabled(False)
        self.name_pat.setStyleSheet("background-color: rgb(66, 65, 65);\nborder-style: none;")
        self.name_pat_label.setStyleSheet("color: rgb(66, 65, 65);")

        self.name_pat.textChanged.connect(lambda: warning_empty(element=self.name_pat))
        self.lineEdit.textChanged.connect(lambda: warning_empty(element=self.lineEdit))

        self.actionQuit.triggered.connect(self.close)
        self.actionOpen.triggered.connect(self.get_dir)

    def closeEvent(self, event):
        self.switch_main_win.emit()
        event.accept()

    def on_combobox_changed(self, index):
        if self.comboBox.currentText() == 'Range by name':
            self.name_pat_label.setEnabled(True)
            self.name_pat_label.setStyleSheet("color: white")
            self.name_pat.setEnabled(True)
            self.name_pat.setStyleSheet("")

        else:
            self.name_pat_label.setEnabled(False)
            self.name_pat_label.setStyleSheet("color: rgb(66, 65, 65);")
            self.name_pat.setText("")
            self.name_pat.setEnabled(False)
            self.name_pat.setStyleSheet("background-color: rgb(66, 65, 65);\nborder-style: none;")

    def get_dir(self):
        self.directory = QFileDialog.getExistingDirectory(self)
        self.lineEdit.setText(self.directory)

    def ranger(self):
        if not self.lineEdit.text() or self.lineEdit.text().isspace():
            alert_empty(self.lineEdit)
        else:
            counter = 0
            if not self.directory:
                self.directory = self.lineEdit.text()
            files = os.listdir(self.directory)
            os.chdir(self.directory)
            match self.comboBox.currentText():
                case "Range by extension":
                    for file in files:
                        if os.path.isfile(file):  # verifie si si il s'agit d'un fichier
                            extension = file.split(".")[-1]
                            subpath = os.path.join(self.directory, extension)
                            if os.path.exists(os.path.join(subpath,
                                                           file)):  # si le fichier n'existe pas dans le dossier destinataire
                                send2trash(file)
                            else:
                                if os.path.exists(extension):
                                    shutil.move(file, subpath)
                                else:
                                    os.mkdir(extension)
                                    shutil.move(file, subpath)
                                counter += 1

                case "Range by name":
                    if not self.name_pat.text() or self.name_pat.text().isspace():
                        alert_empty(self.name_pat)
                    else:
                        name_pattern = self.name_pat.text()
                        for file in files:
                            if os.path.isfile(file):
                                extension = file.split(".")[-1]
                                filename = file[:-len(extension) - 1]
                                subpath = self.directory + "/" + name_pattern
                                if os.path.exists(os.path.join(subpath,
                                                               file)):  # si le fichier n'existe pas dans le dossier destinataire
                                    send2trash(file)
                                else:
                                    if name_pattern.upper() in filename.upper():  # verifie si si il s'agit d'un fichier
                                        if os.path.exists(name_pattern):
                                            shutil.move(file, subpath)
                                        else:
                                            os.mkdir(name_pattern)
                                            shutil.move(file, subpath)
                                        counter += 1
            pop_message(typ=QMessageBox.Information,
                        wIco='D:\\DATAS\\Pycharm_projet\\BOOKS\\apps\\file_manager\\assets\\info.ico',
                        text=f"Opération effectue, {counter} fichier(s) ont été ranger avec succès")

    def goto_main_window(self):
        self.switch_main_win.emit()
        self.close()


class Controler:

    def __init__(self):
        pass

    def show_main_win(self):
        self.main_win = Main()

        self.main_win.switch_deleter_win.connect(self.show_deleter_win)
        self.main_win.switch_classer_win.connect(self.show_classer_win)
        self.main_win.switch_remover_win.connect(self.show_remover_win)

        # self.main_win.setStyleSheet(self.fade_in)
        self.main_win.show()
        # self.main_win.setStyleSheet('')

    def show_deleter_win(self):
        # if not is_window_open(DelByEx):
        self.main_win.close()
        self.deleter = DelByEx()
        self.deleter.switch_main_win.connect(self.show_main_win)
        self.deleter.show()

    def show_classer_win(self):
        # if not is_window_open(RangeWndow):
        self.main_win.close()
        self.ranger = RangeWndow()
        self.ranger.switch_main_win.connect(self.show_main_win)
        self.ranger.show()

    def show_remover_win(self):
        # if not is_window_open(Del_dbles):
        self.main_win.close()
        self.dbl_rem = Del_dbles()
        self.dbl_rem.switch_main_win.connect(self.show_main_win)
        self.dbl_rem.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ctrl = Controler()
    ctrl.show_main_win()
    sys.exit(app.exec_())
