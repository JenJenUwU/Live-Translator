from model import model_init
import os
import numpy as np
import soundcard as sc
import soundfile as sf

# Run on GPU with FP16
model = model_init()

# or run on GPU with INT8
# model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
# or run on CPU with INT8
# model = WhisperModel(model_size, device="cpu", compute_type="int8")

OUTPUT = "output/temp.wav"
SAMPLE_RATE = 48000
CHUNK_DURATION = 0.2  # Recording chunk duration in seconds
MINIMUM_CHUNK_LENGTH = 2  # Minimum length of a recorded section in seconds
BLOCKSIZE = 8192  # Recommended block size
# Note: 8192 seems to work well as an alternative block size
SILENCE_THRESHOLD_DB = -40  # Threshold for detecting silence, based on observed volume

# Ensure the output directory exists
os.makedirs("output", exist_ok=True)

# Get the microphone with loopback enabled
mic = sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True)

try:
    with mic.recorder(samplerate=SAMPLE_RATE, blocksize=BLOCKSIZE) as source:
        print("Program Initialized")
        recording_buffer = []  # Buffer to store audio data
        while True:
            # Record a short chunk of audio
            data = source.record(numframes=int(CHUNK_DURATION * SAMPLE_RATE))

            # Calculate the volume in decibels
            rms = np.sqrt(np.mean(data**2))
            volume_db = 20 * np.log10(rms + 1e-6)  # Convert amplitude to decibels

            # Check if the volume is below the silence threshold
            if volume_db < SILENCE_THRESHOLD_DB:
                if recording_buffer:
                    # Save the recorded audio buffer if it meets the minimum length requirement
                    total_buffer_duration = len(recording_buffer) * CHUNK_DURATION
                    if total_buffer_duration >= MINIMUM_CHUNK_LENGTH:
                        sentence_data = np.concatenate(recording_buffer, axis=0)
                        sf.write(file=OUTPUT, data=sentence_data[:, 0], samplerate=SAMPLE_RATE)
                        segments, info = model.transcribe(OUTPUT, beam_size=5)
                        for segment in segments:
                            print(segment.text)
                    recording_buffer = []
            else:
                # Add the chunk to the buffer
                recording_buffer.append(data)
                in_silence = False

except KeyboardInterrupt:
    print("\nRecording stopped.")
    # Save any remaining audio in the buffer if it meets the minimum length requirement
    if recording_buffer:
        total_buffer_duration = len(recording_buffer) * CHUNK_DURATION
        if total_buffer_duration >= MINIMUM_CHUNK_LENGTH:
            sentence_data = np.concatenate(recording_buffer, axis=0)
            sf.write(file=OUTPUT, data=sentence_data[:, 0], samplerate=SAMPLE_RATE)