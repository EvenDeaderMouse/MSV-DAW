import numpy as np
import pyaudio
import wave
import time
from datetime import datetime
import os
import EffectUtil
from multiprocessing import Process
from enum import Enum
from threading import Thread


class States(Enum):
    PAUSED = 'PAUSED'
    RECORDING = 'RECORDING'
    PLAYING = 'PLAYING'


class Session(object):
    def __init__(self, chunksize=512, audformat=pyaudio.paInt16, sample_rate=44100):
        self.CHUNKSIZE: int = chunksize
        self.AUDFORMAT = audformat
        self.SAMPLE_RATE: int = sample_rate
        self.STATE = States.PAUSED
        self.tempFilePointerDict: dict = {}
        self.cDir: str = os.getcwd()
        self.pyAudio = pyaudio.PyAudio()  # create one
        self.activeInput: dict = dict(self.getInputDevices()['dInput'])  # take default machine input device
        self.activeOutput: dict = dict(self.getOutputDevices()['dOutput'])
        self.inputCHANNELS: int = self.activeInput["maxInputChannels"]
        self.outputCHANNELS: int = self.activeOutput["maxOutputChannels"]
        self.BPM: int = 60
        self.temptrack = 0  ##Testing delete

    def getInputDevices(self):
        inputDevices = {}
        for i in range(0, self.pyAudio.get_device_count()):
            device = self.pyAudio.get_device_info_by_index(i)
            if device["maxInputChannels"] > 0:
                inputDevices.update({device["name"]: device})
        return {"dInput": self.pyAudio.get_default_input_device_info(), "InputDevices": inputDevices}

    def getOutputDevices(self):
        outputDevices = {}
        for i in range(0, self.pyAudio.get_device_count()):
            device = self.pyAudio.get_device_info_by_index(i)
            if device["maxOutputChannels"] > 0:
                outputDevices.update({device["name"]: device})
        return {"dOutput": self.pyAudio.get_default_output_device_info(), "OutputDevices": outputDevices}

    def play_buttonpress(self):  # button functionality and logic
        if self.STATE != States.PLAYING:
            if self.STATE == States.PAUSED:
                self.setSTATE(States.PLAYING)

            # maybe extrude this into async function and await all streams back
            playbackStreams = []
            for entry in self.tempFilePointerDict:
                playbackStreams.append(Process(target=self.playback, args=(self.tempFilePointerDict[entry],)))
            ####
            print("Playing in 3...")
            time.sleep(1 * (60 / self.BPM))
            print("Playing in 2...")
            time.sleep(1 * (60 / self.BPM))
            print("Playing in 1...")
            time.sleep(1 * (60 / self.BPM))
            for entry in playbackStreams:
                entry.start()
        else:
            self.stop_buttonpress()

    def playback(self, wavFile):  # actual playback of audio stream or maybe this needs to return stream class obj
        wave_Read = wave.open(wavFile, 'rb')
        p = pyaudio.PyAudio()
        stream = p.open(format=self.pyAudio.get_format_from_width(wave_Read.getsampwidth()),
                                   channels=wave_Read.getnchannels(),
                                   rate=wave_Read.getframerate(),
                                   output=True,
                                   frames_per_buffer=self.CHUNKSIZE)

        print("* playing")

        # while self.STATE != States.PAUSED:
        while len(data := wave_Read.readframes(self.CHUNKSIZE)):
            stream.write(data)

        print("* end playback")
        self.setSTATE(States.PAUSED)

        wave_Read.close()
        stream.stop_stream()
        stream.close()

    def stop_buttonpress(self):
        print("DAW stopped")
        self.setSTATE(States.PAUSED)

    def record_buttonpress(self, solo=True):  # effect arg or ui abfrage
        if self.activeOutput != None and self.activeInput != None and self.inputCHANNELS != None:
            if self.STATE != States.RECORDING:
                self.setSTATE(States.RECORDING)
                recording = Thread(target=self.record, daemon=True)
                if not solo:
                    play_stream = Thread(target=self.play_buttonpress, daemon=True)
                    play_stream.start()
                recording.start()
            else:
                self.stop_buttonpress()
                time.sleep(1)
                self.record_buttonpress(solo)
        else:
            # errorhandling
            pass

    def record(self):
        # newTrack = createNewTrack()->returns num/name
        print("Recording in 3...")
        time.sleep(1 * (60 / self.BPM))
        print("Recording in 2...")
        time.sleep(1 * (60 / self.BPM))
        print("Recording in 1...")
        time.sleep(1 * (60 / self.BPM))
        stream = self.pyAudio.open(format=self.AUDFORMAT,
                                   channels=self.inputCHANNELS,
                                   rate=self.SAMPLE_RATE,
                                   input=True,
                                   output=True,
                                   frames_per_buffer=self.CHUNKSIZE,
                                   input_device_index=self.activeInput["index"])

        print("* recording")

        tempFile = []
        while self.STATE != States.PAUSED:
            data = stream.read(self.CHUNKSIZE)
            # data += effects
            tempFile.append(data)
            # newTrack.updateGraph(tempFile)

        print("* end recording")
        self.setSTATE(States.PAUSED)

        stream.stop_stream()
        stream.close()

        WAVE_OUTPUT_TEMP_FILENAME = str(datetime.now()).replace(":", "-") + ".wav"
        wf = wave.open(WAVE_OUTPUT_TEMP_FILENAME, 'wb')
        wf.setnchannels(self.inputCHANNELS)
        wf.setsampwidth(pyaudio.get_sample_size(self.AUDFORMAT))
        wf.setframerate(self.SAMPLE_RATE)
        wf.writeframes(b''.join(tempFile))
        wf.close()
        a = self.getOutputDevices()
        self.tempFilePointerDict.update({self.temptrack: WAVE_OUTPUT_TEMP_FILENAME})#WIP
        self.temptrack += 1


    def deleteTrack(self, trackNum):
        try:
            del self.tempFilePointerDict[trackNum]
        except KeyError:
            pass

    # getter
    def getCHUNKSIZE(self):
        return self.CHUNKSIZE

    def getAUDFORMAT(self):
        return self.AUDFORMAT

    def getSAMPLE_RATE(self):
        return self.SAMPLE_RATE

    def getSTATE(self):
        return self.STATE

    def getTempFilePointerDict(self):
        return self.tempFilePointerDict

    def getCDir(self):
        return self.cDir

    def getActiveInput(self):
        return self.activeInput

    def getActiveOutput(self):
        return self.activeOutput

    def getInputCHANNELS(self):
        return self.inputCHANNELS

    def getPyAudio(self):
        return self.pyAudio

    def getBPM(self):
        return self.BPM

    # setter
    def setCHUNKSIZE(self, chunksize):
        self.CHUNKSIZE = chunksize

    def setAUDFORMAT(self, audformat):
        self.AUDFORMAT = audformat

    def setSAMPLE_RATE(self, sample_rate):
        self.SAMPLE_RATE = sample_rate

    def setSTATE(self, state):
        if isinstance(state, States):
            self.STATE = state
        elif isinstance(state, str):
            match state.upper():
                case 'PLAYING':
                    self.STATE = States.PLAYING
                case 'PAUSED':
                    self.STATE = States.PAUSED
                case 'RECORDING':
                    self.STATE = States.RECORDING
        else:
            # errorhandling
            pass

    def setActiveInput(self, device):
        if isinstance(device, dict):
            self.activeInput = device
            self.setInputCHANNELS(self.activeInput["maxInputChannels"])
        elif isinstance(device, str):
            self.activeInput = self.getInputDevices()['InputDevices'][device]
            self.setInputCHANNELS(self.activeInput["maxInputChannels"])

    def setActiveOutput(self, device):
        if isinstance(device, dict):
            self.activeOutput = device
        elif isinstance(device, str):
            self.activeOutput = self.getOutputDevices()['OutputDevices'][device]

    def setInputCHANNELS(self, inputCHANNELS):
        self.inputCHANNELS = inputCHANNELS

    def setOutputCHANNELS(self, outputCHANNELS):
        self.outputCHANNELS = outputCHANNELS

    def setPyAudio(self, pyaudio: pyaudio.PyAudio):
        self.pyAudio = pyaudio

    def setBPM(self, BPM: int):
        self.BPM = BPM


"""    def setTempFilePointerDict(self, temp:dict):
         self.tempFilePointerDict = temp

    def setCDir(self):
         self.cDir"""
