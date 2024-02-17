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



if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
