import time

def transcribe_chunk(model,delay):
    while True:
        word = ""
        time.sleep(delay)
        segments, info = model.transcribe("output/temp.wav", beam_size=5)
        print()
        print()
        print()
        print()
        for segment in segments:
            word += str(segment.text)
        print(word)