"""Feature extraction identical to Notebook/ML_experiments.ipynb (16 kHz, 10 s, 40 MFCC x 100 frames)."""
from __future__ import annotations

from pathlib import Path

import librosa
import numpy as np

SR, DURATION, N_MFCC, MAX_LEN = 16000, 10, 40, 100
AUDIO_EXT = {".wav", ".flac", ".m4a", ".mp3", ".ogg"}


def _load_via_ffmpeg(path):
    """Decode with the ffmpeg binary bundled in imageio-ffmpeg when no system codec is available."""
    import subprocess
    import tempfile

    import imageio_ffmpeg
    with tempfile.TemporaryDirectory() as d:
        wav = Path(d) / "x.wav"
        subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-i", path, "-ac", "1", "-ar", str(SR),
                        "-t", str(DURATION), str(wav)], check=True, capture_output=True)
        return librosa.load(str(wav), sr=SR)


def mfcc(path: str) -> np.ndarray | None:
    try:
        try:
            y, sr = librosa.load(path, sr=SR, duration=DURATION)
        except Exception:
            y, sr = _load_via_ffmpeg(path)  # e.g. .m4a phone recordings
        m = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=N_MFCC)
    except Exception as e:  # unreadable codec etc.
        print(f"  skipped {Path(path).name}: {type(e).__name__}")
        return None
    if m.shape[1] < MAX_LEN:
        m = np.pad(m, ((0, 0), (0, MAX_LEN - m.shape[1])))
    return m[:, :MAX_LEN]


def stats(m: np.ndarray) -> np.ndarray:
    d1, d2 = librosa.feature.delta(m), librosa.feature.delta(m, order=2)
    return np.concatenate([m.mean(1), m.std(1), m.max(1), m.min(1), np.median(m, 1),
                           d1.mean(1), d1.std(1), d2.mean(1), d2.std(1)])


def load_dataset(root: Path, cache: Path):
    """Return (mfcc[N,40,100], stats[N,360], y[N], names[N]) for data/tractor/{normal,abnormal}."""
    if cache.exists():
        z = np.load(cache, allow_pickle=True)
        return z["mfcc"], z["stats"], z["y"], z["names"]
    M, S, y, names = [], [], [], []
    for label, cls in enumerate(["normal", "abnormal"]):
        for p in sorted((root / cls).iterdir()):
            if p.suffix.lower() not in AUDIO_EXT:
                continue
            m = mfcc(str(p))
            if m is None:
                continue
            M.append(m); S.append(stats(m)); y.append(label); names.append(p.name)
    M, S, y, names = np.array(M), np.array(S), np.array(y), np.array(names)
    cache.parent.mkdir(parents=True, exist_ok=True)
    np.savez(cache, mfcc=M, stats=S, y=y, names=names)
    return M, S, y, names
