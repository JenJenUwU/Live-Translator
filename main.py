import threading
import torch
import soundcard as sc
import numpy as np
from model import model_init
from record import update_data
from transcribe import transcribe_chunk
from googletrans import Translator




def main(source, model, translator, sample_rate=16000, seconds=15, transcribe_delay=5, update_delay=0.1, translate_to="en"):
    buffer = np.zeros(sample_rate * seconds)

    stop_event = threading.Event()

    update_thread = threading.Thread(target=update_data, args=(source, buffer, sample_rate, update_delay, stop_event))
    transcribe_thread = threading.Thread(target=transcribe_chunk, args=(model, buffer, translator, translate_to, transcribe_delay, stop_event))

    update_thread.start()
    transcribe_thread.start()

    try:
        while not stop_event.is_set():
            user_input = input("Type 'stop' to stop transcription: \n")
            if user_input.lower() == "stop":
                stop_event.set()
                print("Stopping transcription...")

    except KeyboardInterrupt:
        stop_event.set()
        print("Transcription stopped manually (Ctrl+C).")

    update_thread.join()
    transcribe_thread.join()

print("Initializing...")
mic = sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True)

if torch.cuda.is_available():
    whisper_model = model_init()
else:
    whisper_model = model_init(device="cpu", compute_type="float32")

google_translator = Translator()
print("Initialization complete.")
print()

main(mic, whisper_model, google_translator)