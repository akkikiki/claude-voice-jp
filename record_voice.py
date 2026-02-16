import sounddevice as sd
import soundfile as sf

duration = 10  # seconds
sr = 16000

input("Press Enter to start recording...")
print("Recording... speak now!")
audio = sd.rec(int(duration * sr), samplerate=sr, channels=1)
sd.wait()
sf.write("my_voice.wav", audio, sr)
print("Saved to my_voice.wav")
