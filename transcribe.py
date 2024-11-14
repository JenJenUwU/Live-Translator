import time
import numpy as np

def transcribe_chunk(model, buffer, translator, translate_to, delay):
    while True:
        print('\033[1A', end='\x1b[2K')
        print('\033[1A', end='\x1b[2K')
        time.sleep(delay)
        data_end_idx = np.count_nonzero(buffer)
        data_to_transcribe = buffer[-data_end_idx:]
        segments, _ = model.transcribe(data_to_transcribe, beam_size=5)
        transcription = " ".join(segment.text for segment in segments)
        print(transcription)
        print(translator.translate(transcription, dest=translate_to).text)
