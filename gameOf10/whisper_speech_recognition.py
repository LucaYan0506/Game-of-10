import whisper
import queue
import threading
import torch
import sounddevice as sd
import numpy as np
import requests


def speech_recognition():
    model = whisper.load_model("small")  # Use the smallest model for speed
    audio_queue = queue.Queue()
    transcription = []
    end_of_speech = threading.Event()

    def audio_callback(indata, frames, time, status):
        if status:
            print(status, flush=True)
        audio_queue.put(indata.copy())

    def process_audio():
        audio_data = []
        while not end_of_speech.is_set():
            try:
                # Gets 2 seconds of audio from the audio queue at a time
                chunk = audio_queue.get(timeout=2.0)

                # Use only the first channel
                audio_data.extend(chunk[:, 0])

                if len(audio_data) >= 16000 * 2:  # Process 2 seconds of audio at a time
                    audio_np = np.array(audio_data, dtype=np.float32)

                    # Adjust this threshold as needed - signifies audio is coming in
                    if np.abs(audio_np).mean() > 0.0005:
                        audio_tensor = torch.from_numpy(audio_np).float()

                        with torch.no_grad():
                            # Send audio data to be transcribed
                            result = model.transcribe(audio_tensor, verbose=False)

                        if result["text"].strip() and len(result["text"].strip()) > 5:
                            transcription.append(result["text"].strip())

                            # End sentence if the last character of the transcription is a fullstop, exclamation, or a question mark
                            if result["text"].strip()[-1] in ".!?":
                                end_of_speech.set()
                    # Keep last 1.5 seconds for context
                    audio_data = audio_data[int(16000 * 1.5) :]
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Error in audio processing: {e}")
                end_of_speech.set()

    processing_thread = threading.Thread(target=process_audio, daemon=True)
    processing_thread.start()

    try:
        with sd.InputStream(
            callback=audio_callback, channels=1, samplerate=16000, dtype="float32"
        ):
            print(
                "Start speaking (the function will end when a full sentence is detected)..."
            )
            end_of_speech.wait()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        end_of_speech.set()  # Ensure the processing thread ends

    processing_thread.join()
    return " ".join(transcription)


if __name__ == "__main__":
        transcription = speech_recognition()
        print(f"Transcription: {transcription}")
        if ("place" in transcription.lower()):
            url = "http://127.0.0.1:8000/sendCommand/"

            payload = {
                "card": "place",
            }

            response = requests.post(url, json=payload)  # POST request
            print("Response status code:", response.status_code)
            print("Response body:", response.json()) 
        else:
            n = 1
            if ("one" in transcription.lower()):
                n = 1
            elif ("two" in transcription.lower()):
                n = 2
            elif ("three" in transcription.lower()):
                n = 3
            elif ("four" in transcription.lower()):
                n = 4
            elif ("five" in transcription.lower()):
                n = 5
            elif ("six" in transcription.lower()):
                n = 6
                

            url = "http://127.0.0.1:8000/sendCommand/"

            payload = {
                "command": "pick",
                "card": n,
            }

            response = requests.post(url, json=payload)  # POST request
            print("Response status code:", response.status_code)
            print("Response body:", response.json()) 
