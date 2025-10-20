<div align="center">
  <img src="assets/logo.png" alt="Logo"><br>
  <h3>SignaMux</h3>
  <p>A simple steganography program</p>
</div>

## Features:
The program is able to:

 - take an input audio clip wav or mp3
 - produce outputs in the wav format
 - encrypt the data within using a password
 - produce sharable discrete packets of data for you to safely share

## Usage
To use the program:

**Encoding**:
 1. Open the program and ensure you are in the "encode" tab
 2. Prepare the audio to embed the text into in a mp3 or wav format.
 3. Open the program and select the input wav, and then another file to wrie it out to
 4. Type in an encryption phrase to the input for the password. Encryption is NOT optional.
 5. Paste in your text into the input box
 6. Press the encode button and retrieve your output

**Decoding**:
 1. Open the program and ensure you are in the "decode" tab
 2. Select the .wav (ONLY .WAV) file you have been given that includes the hidden signal
 3. Enter the passphrase you aggreed upon into the passphrase entry form
 4. Click decode, assuming the password and wav are valid the program should decode your message!

## Other
This program has only been tested on Linux (debian trixie) if you have issues on your operating system, please open an issue including the error the program throws.

This was created for the Siege event from HackClub following the "signal" theme.

Star if you like :D