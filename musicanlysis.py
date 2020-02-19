# Helper module for generating basic graphics from music
import config
import librosa

# TODO: create matrix of equalizer levels

# TODO: drum separation

# Load the audio as a waveform `y`
# Store the sampling rate as `sr`
y, sr = librosa.load(config.music_path)

# y_percussive = librosa.effects.percussive(y)
# y_harmonic = librosa.effects.percussive(y)
# librosa.output.write_wav('music/percussive.wav', y_percussive, sr)
# librosa.output.write_wav('music/harmonic.wav', y_harmonic, sr)

# # Run the default beat tracker
# tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
#
# print('Estimated tempo: {:.2f} beats per minute'.format(tempo))
#
# # Convert the frame indices of beat events into timestamps
# beat_times = librosa.frames_to_time(beat_frames, sr=sr)
#
# print(sr)
# print(beat_times)