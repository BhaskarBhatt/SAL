import librosa
import numpy as np

def analyze_syllables(audio_path, syllable_times, sample_rate=22050):
    y, sr = librosa.load(audio_path, sr=sample_rate)
    results = []
    for start_time, end_time in syllable_times:
        start_sample = int(start_time * sr)
        end_sample = int(end_time * sr)
        syllable_audio = y[start_sample:end_sample]
        duration = end_time - start_time 
        energy = np.sum(syllable_audio ** 2)

        pitches, magnitudes = librosa.piptrack(y=syllable_audio, sr=sr)
        pitch_values = pitches[pitches > 0]
        pitch = np.mean(pitch_values) if len(pitch_values) > 0 else 0 
        results.append({
            "start_time": start_time,
            "end_time": end_time,
            "duration": duration,
            "energy": energy,
            "pitch": pitch
        })
    return results

# audio_path = 'reCORD1.wav'
audio_path = 'REcord2.wav'
# syllable_times_audio_1 = [ (0.35204, 0.52287), (0.61274, 0.98644),]
syllable_times_audio_2 = [ (0.44428, 0.87839), (1.03750, 1.32410),]


# results = analyze_syllables(audio_path, syllable_times_audio_1)
results = analyze_syllables(audio_path, syllable_times_audio_2)
for i, result in enumerate(results, start=1):
    print(f"Syllable {i}:")
    print(f"  Start Time: {result['start_time']} seconds")
    print(f"  End Time: {result['end_time']} seconds")
    print(f"  Duration: {result['duration']} seconds")
    print(f"  Energy: {result['energy']}")
    print(f"  Pitch: {result['pitch']} Hz")
    print()


