# -*- coding: utf-8 -*-

import pyaudio
import wave

class AudioParams:
    aformat = pyaudio.paInt16
    channels = 2
    sampwidth = 2
    framerate = 16000
    chunk_size = 1024

def save_audio(params: AudioParams, fname: str, data: "bytes"):
    """ Save data into <fname> file according to audio parameters <params> """
    wf = wave.open(fname, 'wb')
    wf.setnchannels(params.channels)
    wf.setsampwidth(params.sampwidth)
    wf.setframerate(params.framerate)
    wf.writeframes(data)    
    print("File %s written" % fname)
    wf.close()

def play_audio(buffer: "bytes", params : AudioParams) -> bool:
    """ Play audio on the system default output device """
    try:
        audio = pyaudio.PyAudio()
        stream = audio.open(format=params.aformat,
                        channels=params.channels,
                        rate=params.framerate,
                        output=True)
        stream.write(buffer)
        stream.close()
        return True
    except OSError:
        print("Error: Cannot open device")
        return False
def init_audio_input(params: AudioParams) -> pyaudio.Stream:
    """ Return an audio stream to read on """
    audio = pyaudio.PyAudio()
    stream = audio.open(format=params.aformat,
                    channels=params.channels,
                    rate=params.framerate,
                    input=True,
                    frames_per_buffer=params.chunk_size)
    return stream