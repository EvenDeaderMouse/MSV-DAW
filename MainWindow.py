from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtCore import QObject, pyqtSlot


# Importieren Sie Ihre GUI-Klasse aus der generierten Datei
from DAW import Ui_MainWindow

# Importieren Sie Ihre Session-Klasse
from Session import Session

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialisieren der GUI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Init Session
        self.session = Session(self.ui, chunk_size=512, sample_rate=48000)  # connects Backend
        self.ui.setInputDeviceDict(self.session.getInputDevices()['InputDevices'])  # list of all input devices
        self.ui.setOutputDeviceDict(outputDevices = self.session.getOutputDevices()['OutputDevices']) # list of all output devices
        self.ui.recordButton.clicked.connect(self.session.record_buttonpress)
        self.ui.stopButton.clicked.connect(self.session.stop_buttonpress)
        self.ui.playButton.clicked.connect(self.session.play_buttonpress)



if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
