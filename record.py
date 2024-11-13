import soundfile as sf
import numpy as np
import time


def update_data(source, buffer, sample_rate, update_seconds):
    with source.recorder(samplerate=sample_rate, blocksize=8192) as rec:
        while True:
            new_data = rec.record(numframes=int(sample_rate * update_seconds))
            buffer[:-int(sample_rate * update_seconds)] = buffer[int(sample_rate * update_seconds):]
            buffer[-int(sample_rate * update_seconds):] = new_data

def save_audio(buffer, sample_rate, target_filename, delay=0.1):
    while True:
        sf.write(file=target_filename, data=buffer, samplerate=sample_rate)
        time.sleep(delay)