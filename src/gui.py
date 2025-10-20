import tkinter as tk
from tkinter import ttk, filedialog, simpledialog, messagebox
import tempfile
import gzip
import os
from src.encryption import encrypt_bytes, decrypt_bytes
from src.encode import embed_in_wav
from src.decode import extract_from_wav
#from encryption import encrypt_bytes, decrypt_bytes
#from decode import extract_from_wav
#from encode import embed_in_wav

def runGui():
    def browse_input_audio(entry):
        path = filedialog.askopenfilename(filetypes=[("WAV Files", "*.wav"), ("MP3 Files", "*.mp3")])
        if path: entry.config(state="normal"); entry.delete(0, "end"); entry.insert(0, path); entry.config(state="readonly")

    def browse_output_audio(entry):
        path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV Files", "*.wav")])
        if path: entry.config(state="normal"); entry.delete(0, "end"); entry.insert(0, path); entry.config(state="readonly")

    def encode_action():
        carrier_audio = encode_in_entry.get()
        carrier_audio_output = encode_out_entry.get()

        text = encode_text.get("1.0", "end").strip()
        passphrase = encode_pass_entry.get().strip()
        
        if not all([carrier_audio, carrier_audio_output, text, passphrase]):
            return messagebox.showerror("Error", "Missing required fields.")
        
        temp_file = os.path.join(tempfile.gettempdir(), "temptext.txt")
        
        with open(temp_file, "w") as f:
            f.write(text)
        
        with open(temp_file, "rb") as f:
            raw = f.read()
        
        comp = gzip.compress(raw)
        enc = encrypt_bytes(passphrase, comp)
        length = len(enc).to_bytes(4, "big")
        
        payload = length + enc
        
        embed_in_wav(carrier_audio, carrier_audio_output, payload, seed=347952174630859642)
        
        os.remove(temp_file) # their temp file could possibly be sensitive!
        
        messagebox.showinfo("Done", "Encoding complete.")



    def decode_action():
        audio_path = decode_in_entry.get()
        passphrase = decode_pass_entry.get().strip()

        if not all([audio_path, passphrase]):
            return messagebox.showerror("Error", "Missing required fields.")
        
        seed = 347952174630859642
        
        header = extract_from_wav(audio_path, 4, seed=seed)
        length = int.from_bytes(header, "big")
        
        blob = extract_from_wav(audio_path, 4 + length, seed=seed)[4:4+length]
        dec = decrypt_bytes(passphrase, blob)
        
        raw = gzip.decompress(dec)
        
        decode_output.delete("1.0", "end")
        
        decode_output.insert("1.0", raw.decode(errors="ignore"))

    root = tk.Tk()
    root.title("SignaMux Steganography Utility")
    root.geometry("420x450")
    root.resizable(False, False)

    notebook = ttk.Notebook(root)
    encode_tab = ttk.Frame(notebook)
    decode_tab = ttk.Frame(notebook)

    notebook.add(encode_tab, text="Encode")
    notebook.add(decode_tab, text="Decode")

    notebook.pack(expand=True, fill="both", pady=5)

    tk.Label(encode_tab, text="Input Audio:").pack(anchor="w", padx=10, pady=(10, 0))

    encode_in_entry = tk.Entry(encode_tab, width=45, state="readonly")
    encode_in_entry.pack(padx=10)

    tk.Button(encode_tab, text="Browse", command=lambda: browse_input_audio(encode_in_entry)).pack(pady=3)

    tk.Label(encode_tab, text="Output Audio:").pack(anchor="w", padx=10, pady=(5, 0))

    encode_out_entry = tk.Entry(encode_tab, width=45, state="readonly")
    encode_out_entry.pack(padx=10)

    tk.Button(encode_tab, text="Browse", command=lambda: browse_output_audio(encode_out_entry)).pack(pady=3)

    tk.Label(encode_tab, text="Passphrase:").pack(anchor="w", padx=10, pady=(5, 0))
    encode_pass_entry = tk.Entry(encode_tab, width=45, show="●")
    encode_pass_entry.pack(padx=10, pady=3)

    tk.Label(encode_tab, text="Text to Hide:").pack(anchor="w", padx=10, pady=(5, 0))
    encode_text = tk.Text(encode_tab, height=5, width=45)
    encode_text.pack(padx=10, pady=5)

    tk.Button(encode_tab, text="Encode", width=20, command=encode_action).pack(pady=10)

    tk.Label(decode_tab, text="Encoded Audio:").pack(anchor="w", padx=10, pady=(10, 0))

    decode_in_entry = tk.Entry(decode_tab, width=45, state="readonly")
    decode_in_entry.pack(padx=10)

    tk.Button(decode_tab, text="Browse", command=lambda: browse_input_audio(decode_in_entry)).pack(pady=3)

    tk.Label(decode_tab, text="Passphrase:").pack(anchor="w", padx=10, pady=(5, 0))

    decode_pass_entry = tk.Entry(decode_tab, width=45, show="●")
    decode_pass_entry.pack(padx=10, pady=3)

    tk.Label(decode_tab, text="Decoded Text:").pack(anchor="w", padx=10, pady=(5, 0))
    decode_output = tk.Text(decode_tab, height=6, width=45)
    decode_output.pack(padx=10, pady=5)

    tk.Button(decode_tab, text="Decode", width=20, command=decode_action).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    runGui()