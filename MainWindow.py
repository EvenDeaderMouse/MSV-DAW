from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtCore import QObject, pyqtSlot

# Importieren Sie Ihre GUI-Klasse aus der generierten Datei
from DAW import Ui_MainWindow

# Importieren Sie Ihre Session-Klasse
from Session import Session, States

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialisieren der GUI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Initialisieren der Session
        self.session = Session()

        # Verbindung der Schaltflächen mit Methoden
        self.ui.recordButton.clicked.connect(self.startRecording)
        self.ui.stopButton.clicked.connect(self.stopRecording)
        self.ui.playButton.clicked.connect(self.playRecording)

    # Methoden, die auf Benutzeraktionen reagieren
    def startRecording(self):
        self.session.record()

    def stopRecording(self):
        self.session.stop()

    def playRecording(self):
        self.session.play()

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
