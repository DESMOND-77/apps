import sys
import os
import yt_dlp
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QProgressBar, QTextEdit, 
                             QFileDialog, QMessageBox, QFrame, QSizePolicy)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor


class DownloadWorker(QThread):
    progress_updated = pyqtSignal(float)
    progress_text_updated = pyqtSignal(str)
    finished = pyqtSignal()
    error_occurred = pyqtSignal(str)
    info_loaded = pyqtSignal(dict)

    def __init__(self, url, download_path, format_type):
        super().__init__()
        self.url = url
        self.download_path = download_path
        self.format_type = format_type

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', '0%').replace('%', '')
            try:
                self.progress_updated.emit(float(percent))
            except:
                pass
        elif d['status'] == 'finished':
            self.progress_text_updated.emit("Téléchargement terminé!")

    def run(self):
        try:
            if self.format_type == "info":
                with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                    info = ydl.extract_info(self.url, download=False)
                    self.info_loaded.emit(info)
            else:
                download_path = self.download_path
                ydl_opts = {
                    'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
                    'progress_hooks': [self.progress_hook],
                    'quiet': True,
                }

                if self.format_type == "audio":
                    ydl_opts.update({
                        'format': 'bestaudio/best',
                        'extractaudio': True,
                        'audioformat': 'mp3',
                        'nopostoverwrites': True,
                    })
                    self.progress_text_updated.emit("Téléchargement audio direct (MP3)...")

                elif self.format_type == "video":
                    ydl_opts.update({
                        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                        'merge_output_format': 'mp4',
                    })
                    self.progress_text_updated.emit("Téléchargement vidéo (MP4 HD)...")

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([self.url])

                self.finished.emit()
                
        except Exception as e:
            self.error_occurred.emit(str(e))


class YouTubeDownloader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Downloader Premium")
        self.setGeometry(100, 100, 700, 600)
        self.setMinimumSize(650, 550)
        
        # Définir l'icône de l'application
        try:
            self.setWindowIcon(QIcon('YT.ico'))
        except:
            pass
        
        # Variables
        self.download_path = os.path.expanduser("~\\Downloads\\YT_downloader_premium")
        self.worker = None
        
        # Configuration du style
        self.setup_style()
        
        # Interface
        self.create_widgets()
        
    def setup_style(self):
        # Configuration des couleurs
        self.bg_color = QColor(240, 244, 249)
        self.accent_color = QColor(75, 139, 190)
        self.dark_color = QColor(51, 51, 51)
        
        # Appliquer la palette de couleurs
        palette = self.palette()
        palette.setColor(QPalette.Window, self.bg_color)
        palette.setColor(QPalette.WindowText, self.dark_color)
        palette.setColor(QPalette.Base, Qt.white)
        palette.setColor(QPalette.Text, self.dark_color)
        self.setPalette(palette)
        
    def create_widgets(self):
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # En-tête
        header_font = QFont('Segoe UI', 16, QFont.Bold)
        header_label = QLabel("YouTube Downloader Premium")
        header_label.setFont(header_font)
        header_label.setStyleSheet(f"color: {self.accent_color.name()};")
        main_layout.addWidget(header_label)
        
        subheader_label = QLabel("Téléchargez des vidéos et musiques en qualité maximale")
        subheader_label.setFont(QFont('Segoe UI', 9))
        main_layout.addWidget(subheader_label)
        
        # Séparateur
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(separator)
        
        # Section URL
        url_layout = QHBoxLayout()
        url_label = QLabel("URL YouTube:")
        url_label.setFont(QFont('Segoe UI', 10))
        url_layout.addWidget(url_label)
        
        self.url_entry = QLineEdit()
        self.url_entry.setFont(QFont('Segoe UI', 10))
        url_layout.addWidget(self.url_entry)
        
        self.load_btn = QPushButton("Charger")
        self.load_btn.setFont(QFont('Segoe UI', 10, QFont.Bold))
        self.load_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.accent_color.name()};
                color: white;
                padding: 6px;
                border: none;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: {self.accent_color.darker(110).name()};
            }}
        """)
        self.load_btn.clicked.connect(self.load_formats)
        url_layout.addWidget(self.load_btn)
        main_layout.addLayout(url_layout)
        
        # Section destination
        dest_layout = QHBoxLayout()
        dest_label = QLabel("Dossier de destination:")
        dest_label.setFont(QFont('Segoe UI', 10))
        dest_layout.addWidget(dest_label)
        
        self.dest_entry = QLineEdit(self.download_path)
        self.dest_entry.setFont(QFont('Segoe UI', 10))
        dest_layout.addWidget(self.dest_entry)
        
        self.browse_btn = QPushButton("Parcourir")
        self.browse_btn.setFont(QFont('Segoe UI', 10))
        self.browse_btn.clicked.connect(self.browse_directory)
        dest_layout.addWidget(self.browse_btn)
        main_layout.addLayout(dest_layout)
        
        # Boutons de téléchargement
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        self.mp3_btn = QPushButton("🎵 Télécharger MP3")
        self.mp3_btn.setFont(QFont('Segoe UI', 10, QFont.Bold))
        self.mp3_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.accent_color.name()};
                color: white;
                padding: 6px;
                border: none;
                border-radius: 4px;
                min-width: 150px;
            }}
            QPushButton:hover {{
                background-color: {self.accent_color.darker(110).name()};
            }}
            QPushButton:disabled {{
                background-color: #cccccc;
                color: #666666;
            }}
        """)
        self.mp3_btn.clicked.connect(lambda: self.start_download("audio"))
        self.mp3_btn.setEnabled(False)
        btn_layout.addWidget(self.mp3_btn)
        
        self.mp4_btn = QPushButton("🎬 Télécharger MP4 (HD)")
        self.mp4_btn.setFont(QFont('Segoe UI', 10, QFont.Bold))
        self.mp4_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.accent_color.name()};
                color: white;
                padding: 6px;
                border: none;
                border-radius: 4px;
                min-width: 150px;
            }}
            QPushButton:hover {{
                background-color: {self.accent_color.darker(110).name()};
            }}
            QPushButton:disabled {{
                background-color: #cccccc;
                color: #666666;
            }}
        """)
        self.mp4_btn.clicked.connect(lambda: self.start_download("video"))
        self.mp4_btn.setEnabled(False)
        btn_layout.addWidget(self.mp4_btn)
        
        btn_layout.addStretch()
        main_layout.addLayout(btn_layout)
        
        # Barre de progression
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #e0e0e0;
                border-radius: 10px;
                text-align: center;
                height: 20px;
            }
            QProgressBar::chunk {
                background-color: #1ca715;
                border-radius: 10px;
            }
        """)
        main_layout.addWidget(self.progress_bar)
        
        self.progress_label = QLabel("Prêt à télécharger...")
        self.progress_label.setFont(QFont('Segoe UI', 9))
        self.progress_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.progress_label)
        
        # Informations vidéo
        info_group = QFrame()
        info_group.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        info_layout = QVBoxLayout(info_group)
        
        info_title = QLabel("Informations vidéo")
        info_title.setFont(QFont('Segoe UI', 10, QFont.Bold))
        info_layout.addWidget(info_title)
        
        self.video_info = QTextEdit()
        self.video_info.setFont(QFont('Segoe UI', 9))
        self.video_info.setReadOnly(True)
        info_layout.addWidget(self.video_info)
        
        main_layout.addWidget(info_group)
        
        # Barre de statut
        status_bar = self.statusBar()
        self.status_label = QLabel("© 2025 Yt_downloader | @DG")
        self.status_label.setStyleSheet("color: #666666;")
        self.status_label.setFont(QFont('Segoe UI', 8))
        status_bar.addPermanentWidget(self.status_label)
        
        # Ajuster les proportions
        main_layout.setStretchFactor(info_group, 1)
        
    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Sélectionner un dossier", self.download_path)
        if directory:
            self.download_path = directory
            self.dest_entry.setText(directory)
        
    def load_formats(self):
        url = self.url_entry.text()
        if not url:
            QMessageBox.critical(self, "Erreur", "Veuillez entrer une URL YouTube")
            return

        self.progress_label.setText("Chargement des formats...")
        self.progress_bar.setValue(0)
        
        self.worker = DownloadWorker(url, self.download_path, "info")
        self.worker.info_loaded.connect(self.show_video_info)
        self.worker.error_occurred.connect(self.show_error)
        self.worker.start()
        
    @pyqtSlot(dict)
    def show_video_info(self, info):
        info_text = f"Titre: {info.get('title', 'Inconnu')}\n"
        info_text += f"Chaîne: {info.get('uploader', 'Inconnu')}\n"
        info_text += f"Durée: {info.get('duration_string', 'Inconnue')}\n"
        info_text += f"Vues: {info.get('view_count', 'Inconnues')}\n"
        info_text += f"Description: {info.get('description', '')[:200]}...\n"
        
        self.video_info.setPlainText(info_text)
        self.progress_label.setText("Prêt à télécharger")
        self.mp3_btn.setEnabled(True)
        self.mp4_btn.setEnabled(True)
        
    def start_download(self, format_type):
        url = self.url_entry.text()
        if not url:
            QMessageBox.critical(self, "Erreur", "Veuillez entrer une URL YouTube")
            return

        self.progress_bar.setValue(0)
        
        self.worker = DownloadWorker(url, self.download_path, format_type)
        self.worker.progress_updated.connect(self.update_progress)
        self.worker.progress_text_updated.connect(self.update_progress_text)
        self.worker.finished.connect(self.download_finished)
        self.worker.error_occurred.connect(self.show_error)
        self.worker.start()
        
    @pyqtSlot(float)
    def update_progress(self, value):
        self.progress_bar.setValue(int(value))
        self.progress_label.setText(f"Téléchargement... {value:.1f}%")
        
    @pyqtSlot(str)
    def update_progress_text(self, text):
        self.progress_label.setText(text)
        
    @pyqtSlot()
    def download_finished(self):
        self.progress_bar.setValue(0)
        QMessageBox.information(self, "Succès", "Téléchargement terminé avec succès!")
        
    @pyqtSlot(str)
    def show_error(self, error_message):
        self.progress_label.setText("Erreur lors du téléchargement")
        self.progress_bar.setValue(0)
        QMessageBox.critical(self, "Erreur", f"Échec du téléchargement: {error_message}")
        self.mp3_btn.setEnabled(False)
        self.mp4_btn.setEnabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Définir le style de l'application
    app.setStyle('Fusion')
    
    window = YouTubeDownloader()
    window.show()
    
    sys.exit(app.exec_())