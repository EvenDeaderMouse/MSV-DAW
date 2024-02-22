import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter
import math


def createWavFile(filename, wave, sample_rate):
    wave = np.int16(wave)
    wavfile.write(filename, sample_rate, wave)


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


def cutWave(wave, length, sample_rate):
    newLength = np.linspace(0, length, sample_rate * length)
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


def reverbResponse(wave, samplerate, elevel=0.5, predelay=0., delay=0., lowpass=22000, highpass=0):
    if delay < predelay:
        if delay > 0:
            delay = predelay + delay
        else:
            delay = predelay

    reverbEff = butter_lowpass_filter(wave, lowpass, samplerate)  # apply lowpass
    if highpass > 0:
        reverbEff = butter_highpass_filter(reverbEff, highpass, samplerate)  # apply highpass
    if predelay > 0:
        predelayEff = np.linspace(0, 1, int(predelay * samplerate))  # predelay space
    else:
        predelayEff = np.array([])
    predelayEff = np.append(predelayEff, wave)  # predelay effect
    finishedReverb = addWaves(predelayEff, [reverbEff, ],
                              int(delay * samplerate))  # apply reverb effect after delay
    return finishedReverb * elevel


def reverb(wave, samplerate, elevel=0.5, predelay=0.1, delay=0.1, lowpass=22000, highpass=0, repeat=1, length=0):
    responses = []
    for i in range(1, repeat + 1):
        responses.append(
            reverbResponse(wave, samplerate=samplerate, elevel=elevel, predelay=predelay * i, delay=delay * i,
                           lowpass=lowpass, highpass=highpass))
    wave = wave * (0.9 - elevel)
    # apply effect level
    # v2.0 with 1-elevel there is a clipping issue -> needs filter
    addedWaves = addWaves(wave, responses)
    if length > 0:
        addedWaves = cutWave(addedWaves, length, samplerate)
    return addedWaves


def delayResponse(wave, samplerate, elevel=0.5, delay=0.1):
    if delay > 0:
        delayEff = np.linspace(0, 1, int(delay * samplerate))
    else:
        delayEff = np.array([])
    delayEff = np.append(delayEff, wave)  # predelay effect
    delayEff = elevel * delayEff
    return delayEff


def delay(wave, elevel=0.5, delay=0.1):
    delayResp = delayResponse(wave, elevel, delay)
    wave = wave * (1 - elevel)
    return addWaves(wave, [delayResp, ])


def distortSignal(wave, drive=0.3, level=0.5, volume=10):
    distResponse = []
    for sample in wave:
        clean = sample
        distorted = sample * drive
        filtered = ((((2.0 / np.pi) * math.atan(distorted) * level) + (
                clean * (1 - level))) / 2) * volume  # =>NEEDS filter before output
        distResponse.append(filtered)

    return np.asarray(distResponse)
