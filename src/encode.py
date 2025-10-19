import numpy as np
import os
import wave
from pydub import AudioSegment
import gzip
import tempfile
from src.encryption import encrypt_bytes, decrypt_bytes

def _bytes_to_bits(b: bytes) -> np.ndarray:
    arr = np.frombuffer(b, dtype=np.uint8)
    bits = np.unpackbits(arr)
    
    return bits

def _bits_to_bytes(bits: np.ndarray) -> bytes:
    packed = np.packbits(bits)
    
    return packed.tobytes()


def embed_in_wav(carrier_in: str, carrier_out: str, payload: bytes, lsb: int = 1, seed: int | None = None):
    temp_wav = None

    try:
        if not carrier_in.lower().endswith(".wav"):
            temp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    
            audio = AudioSegment.from_file(carrier_in)
            audio = audio.set_frame_rate(44100).set_channels(1).set_sample_width(2)
            audio.export(temp_wav.name, format="wav")
    
            carrier_in = temp_wav.name

        with wave.open(carrier_in, 'rb') as r:
            params = r.getparams()
    
            if params.sampwidth != 2:
                raise ValueError("only 16-bit pcm supported")
    
            frames = r.readframes(params.nframes)

        samples = np.frombuffer(frames, dtype=np.int16).copy()
        bits = np.unpackbits(np.frombuffer(payload, dtype=np.uint8))
    
        total_bits = bits.size
        capacity = samples.size * lsb
        
        if total_bits > capacity:
            raise ValueError(f"payload too large ({total_bits} bits) for capacity {capacity} bits")
        
        rng = np.random.default_rng(seed)
    
        indices = rng.permutation(samples.size)[:total_bits]
        
        if lsb == 1:
            samples[indices] = (samples[indices] & ~1) | bits.astype(np.int16)
        
        else:
            mask = (1 << lsb) - 1
            for i in range(total_bits):
                idx = indices[i]
                samples[idx] = (samples[idx] & ~mask) | int(bits[i])
        
        with wave.open(carrier_out, 'wb') as w:
            w.setparams(params)
            w.writeframes(samples.tobytes())
    
    finally:
        if temp_wav and os.path.exists(temp_wav.name):
            os.unlink(temp_wav.name)

def extract_and_unpack_file(password: str, carrier_in: str, outpath: str, seed: int | None = None):
    with open(infile, 'rb') as f:
        raw = f.read()
    
    compressed = gzip.compress(raw)
    encrypted = encrypt_bytes(password, compressed)
    
    length = len(encrypted).to_bytes(4, 'big')
    payload = length + encrypted
    
    embed_in_wav(carrier_in, carrier_out, payload, lsb=1, seed=seed)