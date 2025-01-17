import numpy as np


def update_data(source, buffer, sample_rate, update_seconds, stop_event):
    with source.recorder(samplerate=sample_rate, blocksize=8192) as rec:
        while not stop_event.is_set():
            new_data = rec.record(numframes=int(sample_rate * update_seconds))
            if new_data.shape[1] == 2:
                new_data = np.mean(new_data, axis=1)
            new_data = new_data[:int(sample_rate * update_seconds)]
            buffer[:-int(sample_rate * update_seconds)] = buffer[int(sample_rate * update_seconds):]
            buffer[-int(sample_rate * update_seconds):] = new_data
