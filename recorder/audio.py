import sounddevice as sd
import soundfile as sf
import threading
import time
import numpy as np

class AudioRecorder:
    def __init__(self, filename="recording.wav", samplerate=44100, channels=1):
        self.filename = filename
        self.samplerate = samplerate
        self.channels = channels
        self.is_recording = False
        self._input_stream = None
        self._file = None
        self.start_time = None

    def start(self):
        """Starts recording audio in a background thread/stream."""
        if self.is_recording:
            print("Audio is already recording.")
            return

        print(f"Starting audio recording to {self.filename}...")
        self.is_recording = True
        self.start_time = time.time()
        
        # Open file for writing
        self._file = sf.SoundFile(self.filename, mode='w', samplerate=self.samplerate, channels=self.channels)

        # Start input stream with callback
        self._input_stream = sd.InputStream(
            samplerate=self.samplerate,
            channels=self.channels,
            callback=self._audio_callback
        )
        self._input_stream.start()

    def stop(self):
        """Stops the recording."""
        if not self.is_recording:
            return

        print("Stopping audio recording...")
        self.is_recording = False
        if self._input_stream:
            self._input_stream.stop()
            self._input_stream.close()
        
        if self._file:
            self._file.close()
        print("Audio recording stopped.")

    def _audio_callback(self, indata, frames, time, status):
        """Callback called for each audio block."""
        if status:
            print(status, flush=True)
        if self.is_recording and self._file:
            self._file.write(indata)

# Example usage
if __name__ == "__main__":
    recorder = AudioRecorder()
    recorder.start()
    time.sleep(5)  # Record for 5 seconds
    recorder.stop()
