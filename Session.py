import numpy as np
import pyaudio
import wave
import time
from datetime import datetime
import os
import EffectUtil
from multiprocessing import Process
from enum import Enum


class States(Enum):
    PAUSED = 'PAUSED'
    RECORDING = 'RECORDING'
    PLAYING = 'PLAYING'


class Session(object):
    def __init__(self, chunksize=512, audformat=pyaudio.paInt16, sample_rate=48000):
        self.CHUNKSIZE: int = chunksize
        self.AUDFORMAT = audformat
        self.SAMPLE_RATE: int = sample_rate
        self.STATE = States.PAUSED
        self.tempFilePointerDict: dict = {}
        self.cDir: str = os.getcwd()
        self.activeInput: dict = dict(self.getInputDevices()['dInput'])  # take default machine input device
        self.activeOutput: dict = dict(self.getOutputDevices()['dOutput'])
        self.inputCHANNELS: int = self.activeInput["maxInputChannels"]
        self.pyaudio = pyaudio.PyAudio()  # create one
        self.BPM: int = 100

    def getInputDevices(self):
        inputDevices = {}
        for i in range(0, self.pyaudio.get_device_count()):
            device = self.pyaudio.get_device_info_by_index(i)
            if device["maxInputChannels"] > 0:
                inputDevices.update({device["name"]: device})
        return {"dInput": self.pyaudio.get_default_input_device_info(), "InputDevices": inputDevices}

    def getOutputDevices(self):
        outputDevices = {}
        for i in range(0, self.pyaudio.get_device_count()):
            device = self.pyaudio.get_device_info_by_index(i)
            if device["maxOutputChannels"] > 0:
                outputDevices.update({device["name"]: device})
        return {"dOutput": self.pyaudio.get_default_output_device_info(), "OutputDevices": outputDevices}

    def play(self):  # button functionality and logic
        if self.STATE != States.PLAYING:
            if self.STATE == States.PAUSED:
                self.setSTATE(States.PLAYING)
            # maybe extrude this into async function and await all streams back
            playbackStreams = []
            for entry in self.tempFilePointerDict:
                playbackStreams.append(Process(target=self.playback(entry)))
            ####
            print("Playing in 3...")
            time.sleep(1 * (self.BPM / 100))
            print("Playing in 2...")
            time.sleep(1 * (self.BPM / 100))
            print("Playing in 1...")
            time.sleep(1 * (self.BPM / 100))
            for entry in playbackStreams:
                entry.start()
                entry.join()

            # open stream with self.Values
            # while not paused and stream != '': play recording
        else:
            self.stop()

    def playback(self, wavFile):  # actual playback of audio stream or maybe this needs to return stream class obj
        wave_Read = wave.open(wavFile, 'rb')
        stream = self.pyaudio.open(format=self.AUDFORMAT,
                                   channels=self.inputCHANNELS,
                                   rate=self.SAMPLE_RATE,
                                   input=False,
                                   output=True,
                                   frames_per_buffer=self.CHUNKSIZE,
                                   output_device_index=self.activeOutput["index"],
                                   )

        print("* playing")

        while self.STATE != States.PAUSED:
            data = wave_Read.readframes(self.CHUNKSIZE)
            while data:
                stream.write(data)
                data = wave_Read.readframes(self.CHUNKSIZE)

        print("* end playback")
        self.setSTATE(States.PAUSED)

        wave_Read.close()
        stream.stop_stream()
        stream.close()

    def stop(self):
        self.setSTATE(States.PAUSED)

    """
    for simuplay:
        if not solo:
            play = Process(target=session.play())
            play.start()
            
        record = Process(target=session.record())
        record.start()
        
        play.join()
        record.join()
    """

    def record(self):
        if self.activeOutput != None and self.activeInput != None and self.inputCHANNELS != None:
            if self.STATE != States.RECORDING:
                self.setSTATE(States.RECORDING)
                # newTrack = createNewTrack()->returns num/name
                print("Recording in 3...")
                time.sleep(1 * (self.BPM / 100))
                print("Recording in 2...")
                time.sleep(1 * (self.BPM / 100))
                print("Recording in 1...")
                time.sleep(1 * (self.BPM / 100))
                stream = self.pyaudio.open(format=self.AUDFORMAT,
                                           channels=self.inputCHANNELS,
                                           rate=self.SAMPLE_RATE,
                                           input=True,
                                           output=True,
                                           frames_per_buffer=self.CHUNKSIZE,
                                           input_device_index=self.activeInput["index"],
                                           output_device_index=self.activeOutput["index"])

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

                WAVE_OUTPUT_TEMP_FILENAME = str(datetime.now()) + ".wav"

                wf = wave.open(WAVE_OUTPUT_TEMP_FILENAME, 'wb')
                wf.setnchannels(self.inputCHANNELS)
                wf.setsampwidth(pyaudio.get_sample_size(self.AUDFORMAT))
                wf.setframerate(self.SAMPLE_RATE)
                wf.writeframes(b''.join(tempFile))
                wf.close()
                self.tempFilePointerDict.update({'newTrack.Num': WAVE_OUTPUT_TEMP_FILENAME + ".wav"})
            else:
                self.stop()
                self.record()
        else:
            # errorhandling
            pass

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
        return self.pyaudio

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

    def setPyAudio(self, pyaudio:pyaudio.PyAudio):
        self.pyaudio = pyaudio

    def setBPM(self, BPM:int):
        self.BPM = BPM


"""    def setTempFilePointerDict(self, temp:dict):
         self.tempFilePointerDict = temp

    def setCDir(self):
         self.cDir"""
