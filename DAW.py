# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainPage6.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from Session import Session, States


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(943, 600)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        MainWindow.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Data
        self.session = Session(self, chunksize=512, sample_rate=48000)  # connects Backend
        self.inputDevices = self.session.getInputDevices()['InputDevices']  # list of all input devices
        self.outputDevices = self.session.getOutputDevices()['OutputDevices']  # list of all output devices


        # Layout für Toolbar -> Start, Stop und Record Button
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 10, 501, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")

        # Toolbar für Start, Stop und Record
        self.toolbBar = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.toolbBar.setContentsMargins(0, 0, 0, 0)
        self.toolbBar.setObjectName("toolbBar")

        # Recordbutton
        self.recordButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.recordButton.setObjectName("recordButton")
        self.toolbBar.addWidget(self.recordButton)
        self.recordButton.clicked.connect(self.session.record_buttonpress)
        # self.recordButton calls -> self.session.record(), when pressed

        # StopButton
        self.stopButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.stopButton.setObjectName("stopButton")
        self.toolbBar.addWidget(self.stopButton)
        self.stopButton.clicked.connect(self.session.stop_buttonpress)
        # self.stopButton calls -> self.session.stop

        # PlayButton
        self.playButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.playButton.setObjectName("playButton")
        self.toolbBar.addWidget(self.playButton)
        self.playButton.clicked.connect(self.session.play_buttonpress)
        #self.playButton calls -> self.session.play(), when pressed

        # Area für Effekte
        self.effectArea = QtWidgets.QScrollArea(self.centralwidget)
        self.effectArea.setGeometry(QtCore.QRect(10, 100, 241, 461))
        self.effectArea.setWidgetResizable(True)
        self.effectArea.setObjectName("effectArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 239, 459))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalScrollBar = QtWidgets.QScrollBar(self.scrollAreaWidgetContents)
        self.verticalScrollBar.setGeometry(QtCore.QRect(220, 0, 16, 441))
        self.verticalScrollBar.setOrientation(QtCore.Qt.Vertical)
        self.verticalScrollBar.setObjectName("verticalScrollBar")

        # Reverb
        self.reverbBox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.reverbBox.setGeometry(QtCore.QRect(10, 10, 201, 171))
        self.reverbBox.setTitle("")
        self.reverbBox.setObjectName("reverbBox")
        self.reverbLabel = QtWidgets.QLabel(self.reverbBox)
        self.reverbLabel.setGeometry(QtCore.QRect(10, 10, 121, 21))
        self.reverbLabel.setObjectName("reverbLabel")

        # Reverb - Repeatdial
        self.repeat = QtWidgets.QDial(self.reverbBox)
        self.repeat.setGeometry(QtCore.QRect(150, 130, 31, 31))
        self.repeat.setMaximum(10)
        self.repeat.setObjectName("repeat")

        # Reverb - LowPassdial
        self.lowPass = QtWidgets.QDial(self.reverbBox)
        self.lowPass.setGeometry(QtCore.QRect(80, 130, 31, 31))
        self.lowPass.setMaximum(22)
        self.lowPass.setObjectName("lowPass")

        # Reverb - HighPassdial
        self.highPass = QtWidgets.QDial(self.reverbBox)
        self.highPass.setGeometry(QtCore.QRect(10, 130, 31, 31))
        self.highPass.setMaximum(22)
        self.highPass.setObjectName("highPass")

        # Reverb - ELeveldial
        self.elevel = QtWidgets.QDial(self.reverbBox)
        self.elevel.setGeometry(QtCore.QRect(10, 70, 31, 31))
        self.elevel.setMaximum(100)
        self.elevel.setObjectName("elevel")

        # Reverb - PreDelaydial
        self.preDelay = QtWidgets.QDial(self.reverbBox)
        self.preDelay.setGeometry(QtCore.QRect(80, 70, 31, 31))
        self.preDelay.setMaximum(100)
        self.preDelay.setObjectName("preDelay")

        # Reverb - Delaydial
        self.delay = QtWidgets.QDial(self.reverbBox)
        self.delay.setGeometry(QtCore.QRect(150, 70, 31, 31))
        self.delay.setMaximum(100)
        self.delay.setObjectName("delay")

        # Label für Dials
        self.label_6 = QtWidgets.QLabel(self.reverbBox)
        self.label_6.setGeometry(QtCore.QRect(10, 110, 51, 16))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.reverbBox)
        self.label_7.setGeometry(QtCore.QRect(70, 110, 51, 16))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.reverbBox)
        self.label_8.setGeometry(QtCore.QRect(140, 110, 41, 16))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.reverbBox)
        self.label_9.setGeometry(QtCore.QRect(10, 50, 41, 16))
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.reverbBox)
        self.label_10.setGeometry(QtCore.QRect(70, 50, 51, 16))
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.reverbBox)
        self.label_11.setGeometry(QtCore.QRect(140, 50, 41, 16))
        self.label_11.setObjectName("label_11")

        # Distortion
        self.distortionBox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.distortionBox.setGeometry(QtCore.QRect(10, 200, 171, 111))
        self.distortionBox.setTitle("")
        self.distortionBox.setObjectName("distortionBox")
        self.distortionLabel = QtWidgets.QLabel(self.distortionBox)
        self.distortionLabel.setGeometry(QtCore.QRect(10, 10, 151, 16))
        self.distortionLabel.setObjectName("distortionLabel")

        # Distortion - Drivedial
        self.drive = QtWidgets.QDial(self.distortionBox)
        self.drive.setGeometry(QtCore.QRect(10, 70, 31, 31))
        self.drive.setMaximum(100)
        self.drive.setObjectName("drive")

        # Distortion - ELeveldial
        self.elevel_3 = QtWidgets.QDial(self.distortionBox)
        self.elevel_3.setGeometry(QtCore.QRect(60, 70, 31, 31))
        self.elevel_3.setMaximum(100)
        self.elevel_3.setObjectName("elevel_3")

        # Distortion - Volumedial
        self.volume = QtWidgets.QDial(self.distortionBox)
        self.volume.setGeometry(QtCore.QRect(110, 70, 31, 31))
        self.volume.setMaximum(100)
        self.volume.setObjectName("volume")

        # Distortion - Labels
        self.label = QtWidgets.QLabel(self.distortionBox)
        self.label.setGeometry(QtCore.QRect(10, 50, 41, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.distortionBox)
        self.label_2.setGeometry(QtCore.QRect(60, 50, 41, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.distortionBox)
        self.label_3.setGeometry(QtCore.QRect(110, 50, 51, 16))
        self.label_3.setObjectName("label_3")

        # Delay
        self.delayBox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.delayBox.setGeometry(QtCore.QRect(10, 340, 171, 101))
        self.delayBox.setTitle("")
        self.delayBox.setObjectName("delayBox")
        self.delayLabel = QtWidgets.QLabel(self.delayBox)
        self.delayLabel.setGeometry(QtCore.QRect(10, 10, 151, 16))
        self.delayLabel.setObjectName("delayLabel")

        # Delay - Delaydial
        self.delayDelay = QtWidgets.QDial(self.delayBox)
        self.delayDelay.setGeometry(QtCore.QRect(10, 60, 31, 31))
        self.delayDelay.setMaximum(100)
        self.delayDelay.setObjectName("delayDelay")

        # Delay - ELevelDelayDial
        self.elevelDelay = QtWidgets.QDial(self.delayBox)
        self.elevelDelay.setGeometry(QtCore.QRect(120, 60, 31, 31))
        self.elevelDelay.setMaximum(100)
        self.elevelDelay.setObjectName("elevelDelay")

        # Delaylabels
        self.label_4 = QtWidgets.QLabel(self.delayBox)
        self.label_4.setGeometry(QtCore.QRect(10, 40, 51, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.delayBox)
        self.label_5.setGeometry(QtCore.QRect(120, 40, 41, 16))
        self.label_5.setObjectName("label_5")
        self.effectArea.setWidget(self.scrollAreaWidgetContents)

        # Trackbox
        self.trackBox = QtWidgets.QScrollArea(self.centralwidget)
        self.trackBox.setGeometry(QtCore.QRect(250, 100, 691, 461))
        self.trackBox.setWidgetResizable(True)
        self.trackBox.setObjectName("trackBox")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 689, 459))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.verticalScrollBar_2 = QtWidgets.QScrollBar(self.scrollAreaWidgetContents_2)
        self.verticalScrollBar_2.setGeometry(QtCore.QRect(670, 0, 16, 431))
        self.verticalScrollBar_2.setOrientation(QtCore.Qt.Vertical)
        self.verticalScrollBar_2.setObjectName("verticalScrollBar_2")
        self.horizontalScrollBar = QtWidgets.QScrollBar(self.scrollAreaWidgetContents_2)
        self.horizontalScrollBar.setGeometry(QtCore.QRect(0, 440, 661, 16))
        self.horizontalScrollBar.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalScrollBar.setObjectName("horizontalScrollBar")

        # Track1
        self.track1 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_2)
        self.track1.setGeometry(QtCore.QRect(10, 10, 581, 121))
        self.track1.setTitle("")
        self.track1.setObjectName("track1")


        # Track1 - Grafik
        self.trackGraphic = QtWidgets.QGraphicsView(self.track1)
        self.trackGraphic.setGeometry(QtCore.QRect(110, 10, 451, 101))
        self.trackGraphic.setObjectName("trackGraphic")

        # Track 1 - Volume
        self.track1Volume = QtWidgets.QSlider(self.track1)
        self.track1Volume.setGeometry(QtCore.QRect(0, 80, 101, 20))
        self.track1Volume.setOrientation(QtCore.Qt.Horizontal)
        self.track1Volume.setObjectName("track1Volume")
        self.track1Label = QtWidgets.QLabel(self.track1)
        self.track1Label.setGeometry(QtCore.QRect(0, 30, 71, 16))
        self.track1Label.setObjectName("track1Label")
        self.trackBox.setWidget(self.scrollAreaWidgetContents_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 943, 18))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # Button for playing while recording -> varname "solo": Bool I/O

        # Dynamic dropdown list for input and output device
        # get Data from session_instance.getInputDevices()
        # and
        # session_instance.getOutputDevices()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def createNewTrack(self):
        # get first Free Track num -> this class needs a object keeping score of all available tracks
        # creates new Track under last one in box
        # returns trackname/-num
        return 2  # later trackNum or Name

    def deleteTrack(self, trackNum):
        # self.session.deleteTrack(self, trackNum)
        # remove all UI elements with TrackNum
        return True

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "DAW - Digital Audio Workstation"))
        self.recordButton.setText(_translate("MainWindow", "Record"))
        self.stopButton.setText(_translate("MainWindow", "Stop"))
        self.playButton.setText(_translate("MainWindow", "Play"))
        self.reverbLabel.setText(_translate("MainWindow", "Reverb"))
        self.label_6.setText(_translate("MainWindow", "highPass"))
        self.label_7.setText(_translate("MainWindow", "lowPass"))
        self.label_8.setText(_translate("MainWindow", "repeat"))
        self.label_9.setText(_translate("MainWindow", "elevel"))
        self.label_10.setText(_translate("MainWindow", "preDelay"))
        self.label_11.setText(_translate("MainWindow", "delay"))
        self.distortionLabel.setText(_translate("MainWindow", "Distorion"))
        self.label.setText(_translate("MainWindow", "drive"))
        self.label_2.setText(_translate("MainWindow", "elevel"))
        self.label_3.setText(_translate("MainWindow", "volume"))
        self.delayLabel.setText(_translate("MainWindow", "Delay"))
        self.label_4.setText(_translate("MainWindow", "delay"))
        self.label_5.setText(_translate("MainWindow", "elevel"))
        self.track1Label.setText(_translate("MainWindow", "Track 1"))

    def getAllEffectVal(self):
        effectVals = {}
        effectVals.update({"reverb": self.getReverbVal()})
        effectVals.update({"distortion": self.getDistortionVal()})
        effectVals.update({"delay": self.getDelayVal()})
        return effectVals

    def getReverbVal(self):
        reverbVal = {}
        reverbVal.update({"eLevel": self.elevel.value()})
        reverbVal.update({"preDelay": self.preDelay.value()})
        reverbVal.update({"delay": self.delay.value()})
        reverbVal.update({"highPass": self.highPass.value()})
        reverbVal.update({"lowPass": self.lowPass.value()})
        reverbVal.update({"repeat": self.repeat.value()})
        return reverbVal

    def getDistortionVal(self):
        distortionVal = {}
        distortionVal.update({"eLevel": self.elevel_3.value()})
        distortionVal.update({"drive": self.drive.value()})
        distortionVal.update({"volume": self.volume.value()})
        return distortionVal

    def getDelayVal(self):
        delayVal = {}
        delayVal.update({"eLevel": self.elevelDelay.value()})
        delayVal.update({"delay": self.delayDelay.value()})
        return delayVal

    def getSoloVal(self):
        return True #self.solo.value()

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    DAW = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(DAW)
    DAW.show()
    sys.exit(app.exec_())
