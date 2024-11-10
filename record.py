import soundfile as sf
import numpy as np
import time


def update_data(source, buffer, sample_rate, update_seconds, total_seconds):
    with source.recorder(samplerate=sample_rate, blocksize=8192) as rec:
        while True:
            new_data = rec.record(numframes=(sample_rate * update_seconds))
            updated_buffer = np.concatenate((buffer, new_data), axis=0)
            buffer[:] = updated_buffer[-(int(sample_rate * total_seconds)):]  # Update buffer in place

def save_audio(buffer, sample_rate, delay=1):
    while True:
        time.sleep(delay)
        sf.write(file="output/temp.wav", data=buffer, samplerate=sample_rate)

