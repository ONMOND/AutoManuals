import whisper
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

class AudioTranscriber:
    def __init__(self, model_size="base"):
        print(f"Loading Whisper model '{model_size}'...")
        self.model = whisper.load_model(model_size)
        print("Model loaded.")

    def transcribe(self, audio_path):
        """
        Transcribes the audio file and returns segments.
        Each segment contains: {'start': float, 'end': float, 'text': str}
        """
        print(f"Transcribing {audio_path}...")
        result = self.model.transcribe(audio_path)
        return result["segments"]

# Example usage
if __name__ == "__main__":
    transcriber = AudioTranscriber()
    # segments = transcriber.transcribe("recording.wav")
    # print(segments)
