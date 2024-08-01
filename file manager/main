# -*- coding: utf-8 -*-
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

from del_b_ext_window import DelByEx
from dup_rem_window import Del_dbles
from file_class_window import RangeWndow


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

    # def closeEvent(self, event):
    #     reponse = QMessageBox.question(self, 'Confirmation', "Êtes-vous sûr de vouloir quitter ?",
    #                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    #
    #     if reponse == QMessageBox.Yes:
    #         event.accept()
    #     else:
    #         event.ignore()


# def is_window_open(window_class):
#     appl = QtWidgets.QApplication.instance()
#     for widget in appl.topLevelWidgets():
#         if isinstance(widget, window_class):
#             return True
#     return False


class Controler:
    fade_in = '''
    QWidget {
        background-color: white;
        opacity: 0;
        transition: opacity 0.5s;
    }
    '''

    fade_out = '''
    QWidget {
        background-color: white;
        opacity: 1;
        transition: opacity 0.5s;
    }
    '''

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
        #     self.main_win.close()
        self.deleter = DelByEx()
        self.deleter.switch_main_win.connect(self.show_main_win)
        self.deleter.show()

    def show_classer_win(self):
        # if not is_window_open(RangeWndow):
        #     self.main_win.close()
        self.ranger = RangeWndow()
        self.ranger.switch_main_win.connect(self.show_main_win)
        self.ranger.show()

    def show_remover_win(self):
        # if not is_window_open(Del_dbles):
        #     self.main_win.close()
        self.dbl_rem = Del_dbles()
        self.dbl_rem.switch_main_win.connect(self.show_main_win)
        self.dbl_rem.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ctrl = Controler()
    ctrl.show_main_win()
    sys.exit(app.exec_())
