import threading
import soundcard as sc
import numpy as np
from model import model_init
from record import update_data
from transcribe import transcribe_chunk
from googletrans import Translator




def main(source, model, translator, sample_rate=16000, seconds=15, transcribe_delay=5, update_delay=0.1, translate_to="en"):
    buffer = np.zeros(sample_rate * seconds)
    update_thread = threading.Thread(target=update_data, args=(source, buffer, sample_rate, update_delay))
    transcribe_thread = threading.Thread(target=transcribe_chunk, args=(model,buffer, translator, translate_to, transcribe_delay))

    update_thread.start()
    transcribe_thread.start()

    update_thread.join()
    transcribe_thread.join()

print("Initializing...")
mic = sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True)
whisper_model = model_init()
google_translator = Translator()
print("Initialization complete.")
print()
try:
    main(mic, whisper_model, google_translator)
except KeyboardInterrupt:
    print("Exiting...")