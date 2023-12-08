import pyaudio
import numpy as np

FORMAT = pyaudio.paInt16
CHANNELS = 1
# Constants for DTMF detection
SAMPLE_RATE = 48000  # Samples per second
CHUNK_SIZE = 1500  # Size of each audio chunk
THRESHOLD = 3000  # Threshold for detecting a signal

# DTMF Frequencies
DTMF_FREQUENCIES = {
    (697, 1209): '1', (697, 1336): '2', (697, 1477): '3', (697, 1633): 'A',
    (770, 1209): '4', (770, 1336): '5', (770, 1477): '6', (770, 1633): 'B',
    (852, 1209): '7', (852, 1336): '8', (852, 1477): '9', (852, 1633): 'C',
    (941, 1209): '*', (941, 1336): '0', (941, 1477): '#', (941, 1633): 'D'
}

def goertzel(samples, target_freq, sample_rate):
    N = len(samples)
    k = int(0.5 + ((N * target_freq) / sample_rate))
    omega = (2.0 * np.pi * k) / N
    cosine = np.cos(omega)
    sine = np.sin(omega)
    coeff = 2.0 * cosine

    q0 = 0.0
    q1 = 0.0
    q2 = 0.0

    for sample in samples:
        q0 = coeff * q1 - q2 + sample
        q2 = q1
        q1 = q0

    real = (q1 - q2 * cosine)
    imaginary = (q2 * sine)
    power = real ** 2 + imaginary ** 2
    return power


def detect_dtmf_tones(chunk, sample_rate):
    chunk = np.frombuffer(chunk, dtype=np.int16)
    detected_tones = []
    max_val = np.max(np.abs(chunk))
    normalized_samples = chunk / max_val
    for freq in {freq for freq_pair in DTMF_FREQUENCIES.keys() for freq in freq_pair}:
        power = goertzel(normalized_samples, freq, sample_rate)
        if power > THRESHOLD:
            detected_tones.append(freq)
    for freq_pair, tone in DTMF_FREQUENCIES.items():
        if all(freq in detected_tones for freq in freq_pair):
            return tone
    return None

# PyAudio
audio = pyaudio.PyAudio()
num_devices = audio.get_device_count()
device_index = 0
# ask user for which device to use
# first print out all available devices
for i in range(num_devices):
    device_info = audio.get_device_info_by_index(i)
    if device_info['maxInputChannels'] > 0:
        print(device_info)

# ask user for input
device_index = int(input("Which device to use? "))
device_info = audio.get_device_info_by_index(device_index)

# Open stream
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=SAMPLE_RATE, input=True, frames_per_buffer=CHUNK_SIZE, input_device_index=device_index)

print("Listening for DTMF tones...")

try:
    tone_on = False
    tone_sequence = []
    while True:
        chunk = stream.read(CHUNK_SIZE)
        tone = detect_dtmf_tones(chunk, SAMPLE_RATE)
        if tone:
            if not tone_on:
                tone_sequence.append(tone)
                print(f"DTMF Tone Detected: {tone}")
            tone_on = True
        else:
            tone_on = False
except KeyboardInterrupt:
    print('Detected DTMF Tones:', tone_sequence)
    print("\nExiting...")
finally:
    # Close the stream and terminate PyAudio
    stream.stop_stream()
    stream.close()
    audio.terminate()
