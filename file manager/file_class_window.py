import os
import shutil
import sys
from time import sleep

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from send2trash import send2trash


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

        self.name_pat.textChanged.connect(lambda: self.warning_empty(element=self.name_pat))
        self.lineEdit.textChanged.connect(lambda: self.warning_empty(element=self.lineEdit))

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
            self.alert_empty(self.lineEdit)
        else:
            counter = 0
            if not self.directory:
                self.directory = self.lineEdit.text()
            files = os.listdir(self.directory)
            os.chdir(self.directory)
            match self.comboBox.currentText():
                case "Range by extension":
                    for file in files:
                        if os.path.isfile(file):  # Check if it is a file
                            extension = file.split(".")[-1]
                            subpath = os.path.join(self.directory, extension)
                            if os.path.exists(os.path.join(subpath,
                                                           file)):  # if the file does not exist in the destination folder
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
                        self.alert_empty(self.name_pat)
                    else:
                        name_pattern = self.name_pat.text()
                        for file in files:
                            if os.path.isfile(file):
                                extension = file.split(".")[-1]
                                filename = file[:-len(extension) - 1]
                                subpath = self.directory + "/" + name_pattern
                                if os.path.exists(os.path.join(subpath,
                                                               file)):  # if the file does not exist in the destination folder
                                    send2trash(file)
                                else:
                                    if name_pattern.upper() in filename.upper():  # Check if it is a file
                                        if os.path.exists(name_pattern):
                                            shutil.move(file, subpath)
                                        else:
                                            os.mkdir(name_pattern)
                                            shutil.move(file, subpath)
                                        counter += 1
            self.pop_message(typ=QMessageBox.Information,
                             text=f"Opération effectue, {counter} fichier(s) ont été ranger avec succès")

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
    ui = RangeWndow()
    ui.show()
    sys.exit(app.exec_())
