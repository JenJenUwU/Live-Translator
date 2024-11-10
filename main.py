import threading
import soundcard as sc
import numpy as np
from model import model_init
from record import update_data, save_audio
from transcribe import transcribe_chunk


def main(source, model, sample_rate=48000, seconds=10, transcribe_delay=1, update_delay=0.1):
    buffer = np.zeros((sample_rate * seconds, 2))
    update_thread = threading.Thread(target=update_data, args=(source, buffer, sample_rate, update_delay, seconds))
    save_thread = threading.Thread(target=save_audio, args=(buffer, sample_rate))
    transcribe_thread = threading.Thread(target=transcribe_chunk, args=(model, transcribe_delay))

    update_thread.start()
    save_thread.start()
    transcribe_thread.start()

    update_thread.join()
    save_thread.join()
    transcribe_thread.join()

print("Initializing...")
mic = sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True)
whisper_model = model_init()
print("Initialization complete.")
main(mic, whisper_model)