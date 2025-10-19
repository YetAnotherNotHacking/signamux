from src.encode import embed_in_wav
from src.decode import extract_from_wav
from src.encryption import encrypt_bytes, decrypt_bytes
import gzip
import numpy as np

def test_signal_mux():
    password = "averysecurepassphrase"
    infile = "secret.txt"
    carrier_in = "example_2p2e5.mp3"
    carrier_out = "secretdata.wav"
    seed = 42

    with open(infile, "rb") as f:
        raw = f.read()
    comp = gzip.compress(raw)
    enc = encrypt_bytes(password, comp)
    length = len(enc).to_bytes(4, "big")
    payload = length + enc

    embed_in_wav(carrier_in, carrier_out, payload, seed=seed)

    header = extract_from_wav(carrier_out, 4, seed=seed)
    length = int.from_bytes(header, "big")
    blob = extract_from_wav(carrier_out, 4 + length, seed=seed)[4:4+length]
    dec = decrypt_bytes(password, blob)
    raw = gzip.decompress(dec)

    print("Recovered:", raw)

if __name__ == "__main__":
    test_signal_mux()