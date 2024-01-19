import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter
import pyaudio
import wave
import time
import math

CHUNK = 512
FORMAT = pyaudio.paInt16

SAMPLE_RATE = 48000
RECORD_SECONDS = 10
"""
inputCHANNELS = None
chosenInput = None
chosenOutput = None
"""
WAVE_OUTPUT_FILENAME = "mic.wav"


def getInputDevices(pyaudio: pyaudio.PyAudio):
    inputDevices = {}
    for i in range(0, pyaudio.get_device_count()):
        device = pyaudio.get_device_info_by_index(i)
        if device["maxInputChannels"] > 0:
            inputDevices.update({device["name"]: device})
    return {"dInput": pyaudio.get_default_input_device_info(), "InputDevices": inputDevices}


def getOutputDevices(pyaudio: pyaudio.PyAudio):
    outputDevices = {}
    for i in range(0, pyaudio.get_device_count()):
        device = pyaudio.get_device_info_by_index(i)
        if device["maxOutputChannels"] > 0:
            outputDevices.update({device["name"]: device})
    return {"dOutput": pyaudio.get_default_output_device_info(), "OutputDevices": outputDevices}


def record(pyaudio: pyaudio.PyAudio, record_seconds, chosenOutput, chosenInput, inputCHANNELS):
    if chosenOutput != None and chosenInput != None and pyaudio != None and inputCHANNELS != None:
        global SAMPLE_RATE
        global FORMAT
        print("Recording in 3...")
        time.sleep(1)
        print("Recording in 2...")
        time.sleep(1)
        print("Recording in 1...")
        time.sleep(1)
        stream = pyaudio.open(format=FORMAT,
                              channels=inputCHANNELS,
                              rate=SAMPLE_RATE,
                              input=True,
                              output=True,
                              frames_per_buffer=CHUNK,
                              input_device_index=chosenInput["index"],
                              output_device_index=chosenOutput["index"])

        print("* recording")

        frames = []
        saveFile = []
        for i in range(0, int(SAMPLE_RATE / CHUNK * record_seconds)):
            data = stream.read(CHUNK)
            frames.append(data)
            saveFile.append(data)
            if stream.get_write_available() >= CHUNK:
                for frame in frames:
                    stream.write(frame)
                    frames = []
        print("* done recording")

        stream.stop_stream()
        stream.close()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(inputCHANNELS)
        wf.setsampwidth(pyaudio.get_sample_size(FORMAT))
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(b''.join(saveFile))
        wf.close()
        i = wavfile.read(WAVE_OUTPUT_FILENAME)
        aud = np.array(i[1], dtype=float)
        return aud

def createWavFile(filename, wave):
    wave = np.int16(wave)
    wavfile.write(filename, SAMPLE_RATE, wave)


def addWaves(baseWave, addedWaves, offset=0):
    for wave in addedWaves:
        if len(baseWave) >= len(wave) + offset:
            t = len(baseWave)
        else:
            t = len(wave) + offset

        newSamples = np.linspace(0, 1, t)

        newWave = np.empty([len(newSamples)], )

        for j in range(len(newSamples)):
            if j < len(baseWave):
                newWave[j] = baseWave[j]
            else:
                newWave[j] = 0
            if j >= offset:
                newWave[j] += wave[j - offset - 1]

        baseWave = newWave

    return baseWave


def cutWave(wave, length):
    newLength = np.linspace(0, length, SAMPLE_RATE * length)
    newWave = np.empty([len(newLength)], )

    for j in range(len(newLength)):
        newWave[j] = wave[j]

    return newWave


def butter_lowpass(cutoff, fs, order=5):
    return butter(order, cutoff, fs=fs, btype='low', analog=False)


def butter_highpass(cutoff, fs, order=5):
    return butter(order, cutoff, fs=fs, btype='highpass', analog=False)


def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


def butter_highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


def reverbResponse(wave,  elevel=0.5,predelay=0., delay=0., lowpass=22000, highpass=0):
    if delay < predelay:
        if delay > 0:
            delay = predelay + delay
        else:
            delay = predelay

    reverbEff = butter_lowpass_filter(wave, lowpass, SAMPLE_RATE)  # apply lowpass
    if highpass > 0:
        reverbEff = butter_highpass_filter(reverbEff, highpass, SAMPLE_RATE)  # apply highpass
    if predelay > 0:
        predelayEff = np.linspace(0, 1, int(predelay * SAMPLE_RATE))  # predelay space
    else:
        predelayEff = np.array([])
    predelayEff = np.append(predelayEff, wave)  # predelay effect
    finishedReverb = addWaves(predelayEff, [reverbEff, ],
                              int(delay * SAMPLE_RATE))  # apply reverb effect after delay
    return finishedReverb * elevel


def reverb(wave, elevel=0.5, predelay=0.1, delay=0.1, lowpass=22000, highpass=0, repeat=1, length=0):
    responses = []
    for i in range(1, repeat+1):
        responses.append(reverbResponse(wave, elevel, predelay * i, delay * i, lowpass, highpass))
    wave = wave * (0.9 - elevel)  # apply effect level # v2.0 with 1-elevel there is a clipping issue -> needs filter
    addedWaves = addWaves(wave, responses)
    if length > 0:
        addedWaves = cutWave(addedWaves, length)
    return addedWaves


def delayResponse(wave, elevel=0.5, delay=0.1):
    if delay > 0:
        delayEff = np.linspace(0, 1, int(delay * SAMPLE_RATE))
    else:
        delayEff = np.array([])
    delayEff = np.append(delayEff, wave)  # predelay effect
    delayEff = elevel * delayEff
    return delayEff


def delay(wave, elevel=0.5, delay=0.1):
    delayResp = delayResponse(wave, elevel, delay)
    wave = wave * (1 - elevel)
    return addWaves(wave, [delayResp,])


def distortSignal(baseWave, drive=0.3, level=0.5, volume=10):
    distResponse = []
    for sample in baseWave:
        clean = sample
        distorted = sample * drive
        filtered = ((((2.0 / np.pi) * math.atan(distorted) * level) + (clean * (1 - level))) / 2) * volume  # =>NEEDS filter before output
        distResponse.append(filtered)

    return np.asarray(distResponse)



