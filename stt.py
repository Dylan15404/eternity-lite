import speech_recognition as sr
import pyaudio
import time
import whisper
import integration

SAMPLE_RATE = 32000
PHRASE_TIME_LIMIT = 5

p = pyaudio.PyAudio()
r = sr.Recognizer()
mic = sr.Microphone(sample_rate=SAMPLE_RATE)

def start_whisper(callword):
    def callback(r, audio): #function thats called whenever audio is detected
        text = r.recognize_whisper(audio, "small.en")
        print(text)
        integration.run_integrator(text, callword)

    with mic as source:
        r.adjust_for_ambient_noise(source)
        print("Recognizing...")

    stop_listening = r.listen_in_background(mic, callback, phrase_time_limit=PHRASE_TIME_LIMIT) #listens in background and calls callback when there is audio
    for _ in range(50): time.sleep(0.1)
    while True: time.sleep(0.1)