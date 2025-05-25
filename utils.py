import soundfile as sf
import librosa
import numpy as np
import io

def load_and_validate_audio(file_bytes, target_sr=16000, min_sec=5, max_sec=10):
    audio, sr = sf.read(io.BytesIO(file_bytes))
    if sr != target_sr:
        audio = librosa.resample(audio, orig_sr=sr, target_sr=target_sr)
    duration = len(audio) / target_sr
    if duration < min_sec or duration > max_sec:
        raise ValueError(f"Audio duration must be between {min_sec} and {max_sec} seconds.")
    if audio.ndim > 1:
        audio = np.mean(audio, axis=1)  # Convert to mono
    audio = audio / (np.max(np.abs(audio)) + 1e-9)  # Avoid division by zero
    return audio.astype(np.float32), target_sr

def waveform_to_logmels(audio, sr=16000, n_mels=80):
    mel_spec = librosa.feature.melspectrogram(
        y=audio, sr=sr, n_fft=400, hop_length=160, n_mels=n_mels, fmin=0, fmax=8000
    )
    log_mel_spec = np.log(mel_spec + 1e-6)
    return log_mel_spec  # [n_mels, time]
