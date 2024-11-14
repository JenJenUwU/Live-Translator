import time

def transcribe_chunk(model,buffer,translator, translate_to,delay):
    while True:
        print('\033[1A', end='\x1b[2K')
        print('\033[1A', end='\x1b[2K')
        time.sleep(delay)
        segments, info = model.transcribe(buffer, beam_size=5)
        transcription = " ".join(segment.text for segment in segments)
        print(transcription)
        print(translator.translate(transcription,dest=translate_to).text)
