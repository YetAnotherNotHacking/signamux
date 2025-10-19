import numpy as np
import os
import wave
import gzip
from src.encryption import encrypt_bytes, decrypt_bytes

def _bytes_to_bits(b: bytes) -> np.ndarray:
    arr = np.frombuffer(b, dtype=np.uint8)
    bits = np.unpackbits(arr)

    return bits

def _bits_to_bytes(bits: np.ndarray) -> bytes:
    packed = np.packbits(bits)
    
    return packed.tobytes()

def extract_from_wav(carrier_in: str, length_bytes: int, lsb: int = 1, seed: int | None = None) -> bytes:
    with wave.open(carrier_in, 'rb') as r:
        params = r.getparams()
        if params.sampwidth != 2:
            raise ValueError("only 16-bit pcm is supported, something went wrong with converstion.")
        frames = r.readframes(params.nframes)

    samples = np.frombuffer(frames, dtype=np.int16)
    
    total_bits = length_bytes * 8
    
    rng = np.random.default_rng(seed)
    indices = rng.permutation(samples.size)[:total_bits]
    
    if lsb == 1:
        bits = (samples[indices] & 1).astype(np.uint8)
    else:
        mask = (1 << lsb) - 1
        bits = (samples[indices] & mask).astype(np.uint8)
    
    return _bits_to_bytes(bits)[:length_bytes]

def extract_and_unpack_file(password: str, carrier_in: str, outpath: str, seed: int | None = None):
    header = extract_from_wav(carrier_in, 4, lsb=1, seed=seed)
    length = int.from_bytes(header, 'big')
    
    blob = extract_from_wav(carrier_in, 4 + length, lsb=1, seed=seed)[4:4+length]
    
    decrypted = decrypt_bytes(password, blob)
    raw = gzip.decompress(decrypted)
    
    with open(outpath, 'wb') as f:
        f.write(raw)