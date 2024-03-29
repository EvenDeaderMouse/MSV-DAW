from queue import Queue

import numpy as np
import pyaudio
import wave
import time
from datetime import datetime
import os
import EffectUtil
from enum import Enum
from threading import Thread
import matplotlib.pyplot as plt


# from DAW import Ui_MainWindow


class States(Enum):
    PAUSED = 'PAUSED'
    RECORDING = 'RECORDING'
    PLAYING = 'PLAYING'


class Session(object):
    def __init__(self, ui=None, chunk_size=512, audformat=pyaudio.paInt16, sample_rate=48000):
        self.CHUNK_SIZE: int = chunk_size
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
        self.ui = ui
        self.effects: dict = {}

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
                playbackStreams.append(
                    Thread(target=self.playback, args=(self.tempFilePointerDict[entry],), daemon=True))
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
                        frames_per_buffer=self.CHUNK_SIZE)

        print("* playing")

        # while self.STATE != States.PAUSED:
        while len(data := wave_Read.readframes(self.CHUNK_SIZE)):
            stream.write(data, self.CHUNK_SIZE)


        print("* end playback")
        self.setSTATE(States.PAUSED)

        wave_Read.close()
        stream.stop_stream()
        stream.close()

    def stop_buttonpress(self):
        print("DAW stopped")
        self.setSTATE(States.PAUSED)
        # Stop playback


    def record_buttonpress(self):  # effect arg or ui abfrage
        if self.activeOutput is not None and self.activeInput is not None and self.inputCHANNELS is not None:
            if self.STATE != States.RECORDING:
                self.setSTATE(States.RECORDING)
                recording = Thread(target=self.record, args=[self.ui.createNewTrack(), ], daemon=True)
                if not self.ui.getSoloVal():
                    play_stream = Thread(target=self.play_buttonpress, daemon=True)
                    play_stream.start()
                recording.start()
            else:
                self.stop_buttonpress()
                time.sleep(1)
                self.record_buttonpress()
        else:
            # errorhandling
            pass

    def record(self, trackName):
        self.effects = self.ui.getAllEffectVal()
        print("Recording in 3...")
        time.sleep(1 * (60 / self.BPM))
        print("Recording in 2...")
        time.sleep(1 * (60 / self.BPM))
        print("Recording in 1...")
        time.sleep(1 * (60 / self.BPM))
        stream = self.pyAudio.open(format=pyaudio.paInt16,
                                   channels=self.inputCHANNELS,
                                   rate=self.SAMPLE_RATE,
                                   input=True,
                                   output=False,
                                   frames_per_buffer=self.CHUNK_SIZE,
                                   input_device_index=self.activeInput["index"])

        print("* recording")

        dataqueue = Queue()
        _queueEnd = object()
        Thread(target=self.processStream, args=[dataqueue, _queueEnd, trackName]).start()
        while self.getSTATE() != States.PAUSED:
            new_data = stream.read(self.CHUNK_SIZE)
            dataqueue.put(new_data)

        dataqueue.put(_queueEnd)
        print("End put")
        while not dataqueue.empty():
            pass    # i tried dataqueue.join() but for some reason it breakes the code and just stops at the same line

        print("* end recording")
        self.setSTATE(States.PAUSED)

        stream.stop_stream()
        stream.close()

    def processStream(self, dataqueue: Queue, _queueEnd, newTrackName):
        tempFile = []
        buffer = np.empty([0, 1], dtype=np.int16)
        interval = 2  # Snapshot interval in seconds
        samples_per_interval = int(self.SAMPLE_RATE * interval / self.CHUNK_SIZE)

        snapshot_counter = 0
        snapshot_data = []

        while True:
            data = dataqueue.get()
            if data != _queueEnd:
                data = np.frombuffer(data, dtype=np.int16)
                data = self.applyEffects(data)

                # Reshape data to have the same shape as buffer
                data = data.reshape(-1, 1)

                buffer = np.concatenate([buffer, data])

                # Check if enough samples are collected for a snapshot
                if len(buffer) >= samples_per_interval:
                    snapshot_data.append(np.mean(buffer[:samples_per_interval]))  # Take the mean of the samples
                    buffer = buffer[samples_per_interval:]  # Remove processed samples from buffer
                    snapshot_counter += 1

                # Check if it's time to create a snapshot
                if snapshot_counter == samples_per_interval:
                    # Convert snapshot data to image
                    plt.plot(snapshot_data)  # Example: Plotting the snapshot data
                    plt.xlabel('Time')
                    plt.ylabel('Amplitude')
                    plt.title('Audio Snapshot')
                    image_data = f'{newTrackName}_snapshot.png'
                    plt.savefig(image_data)  # Save the image
                    plt.close()  # Close the plot
                    snapshot_counter = 0  # Reset the snapshot counter
                    snapshot_data = []  # Clear snapshot data

                    # You can pass the image data to UI for display if needed
                    self.ui.updateTrack(newTrackName, image_data)

            else:
                break

        if len(buffer) > 0:
            tempFile.append(buffer.astype(dtype=np.int16).tobytes())

        dataqueue.task_done()

        WAVE_OUTPUT_TEMP_FILENAME = str(datetime.now()).replace(":", "-") + ".wav"
        wf = wave.open(WAVE_OUTPUT_TEMP_FILENAME, 'wb')
        wf.setnchannels(self.inputCHANNELS)
        wf.setsampwidth(pyaudio.get_sample_size(self.AUDFORMAT))
        wf.setframerate(self.SAMPLE_RATE)
        wf.writeframes(b''.join(tempFile))
        wf.close()
        self.tempFilePointerDict.update({newTrackName: WAVE_OUTPUT_TEMP_FILENAME})

    def applyEffects(self, data):
        for effect in self.effects:
            match effect:
                case "reverb":
                    data = EffectUtil.reverb(wave=data, samplerate=self.SAMPLE_RATE,
                                             elevel=self.effects[effect]["eLevel"],
                                             predelay=self.effects[effect]["preDelay"],
                                             delay=self.effects[effect]["delay"],
                                             lowpass=self.effects[effect]["lowPass"],
                                             highpass=self.effects[effect]["highPass"],
                                             repeat=self.effects[effect]["repeat"], length=0)

                case "distorion":
                    data = EffectUtil.distortSignal(wave=data, drive=self.effects[effect]["drive"],
                                                    level=self.effects[effect]["eLevel"],
                                                    volume=self.effects[effect]["volume"])
                case "delay":
                    data = EffectUtil.delay(wave=data, elevel=self.effects[effect]["eLevel"],
                                            delay=self.effects[effect]["delay"])
        return data

    def passTrackImageData(self, trackName, imageData):
        pass #self.ui.updateTrack(trackName, imageData)

    def deleteTrack(self, trackName):
        try:
            del self.tempFilePointerDict[trackName]
        except KeyError:
            pass

    # getter
    def getCHUNKSIZE(self):
        return self.CHUNK_SIZE

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
        self.CHUNK_SIZE = chunksize

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

    def setPyAudio(self, pyAudio: pyaudio.PyAudio):
        self.pyAudio = pyAudio

    def setBPM(self, BPM: int):
        self.BPM = BPM


"""    def setTempFilePointerDict(self, temp:dict):
         self.tempFilePointerDict = temp

    def setCDir(self):
         self.cDir"""
