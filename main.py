import asyncio
import time
import os
from recorder.browser import BrowserRecorder
from recorder.audio import AudioRecorder
from processing.transcribe import AudioTranscriber
from processing.synchronize import Synchronizer
from reporting.generator import ReportGenerator

async def main():
    print("Initializing AutoDocs...")
    
    # Store events here
    recorded_events = []

    async def event_callback(event):
        print(f"Captured event: {event['type']}")
        recorded_events.append(event)

    # Initialize components
    browser_recorder = BrowserRecorder(event_callback)
    audio_recorder = AudioRecorder("recording.wav")
    
    try:
        # Start recording
        print("\n--- Starting Recording ---")
        print("Press Ctrl+C to stop recording.")
        
        # Start Audio first to establish timeline baseline
        audio_recorder.start()
        audio_start_time = audio_recorder.start_time
        
        # Start Browser
        await browser_recorder.start()

        print("Recording... Close the browser window to stop.")

        # Keep running until browser is closed
        while browser_recorder.is_open:
            await asyncio.sleep(0.5)

    except KeyboardInterrupt:
        print("\n--- Stopping Recording (KeyboardInterrupt) ---")
    finally:
        try:
            await browser_recorder.stop()
        except Exception as e:
            print(f"Warning during browser shutdown: {e}")
            
        try:
            audio_recorder.stop()
        except Exception as e:
            print(f"Warning during audio shutdown: {e}")

    print(f"Captured {len(recorded_events)} browser events.")
    
    if not os.path.exists("recording.wav"):
        print("No audio recorded. Exiting.")
        return

    # Processing Phase
    print("\n--- Processing ---")
    
    # 1. Transcribe
    transcriber = AudioTranscriber(model_size="base")
    segments = transcriber.transcribe("recording.wav")
    print(f"Transcribed {len(segments)} audio segments.")

    # 2. Normalize timestamps
    # Make event timestamps relative to audio recording start
    normalized_events = []
    for event in recorded_events:
        event_time_relative = event['timestamp'] - audio_start_time
        if event_time_relative < 0:
            event_time_relative = 0
        event['timestamp'] = event_time_relative
        normalized_events.append(event)

    # 3. Synchronize
    synchronizer = Synchronizer(normalized_events, segments)
    steps = synchronizer.sync()
    
    # 4. Generate Report
    print("\n--- Generating Report ---")
    generator = ReportGenerator()
    html_path, pdf_path = generator.generate(steps)
    
    print("\n--- Done ---")
    print(f"Open {html_path} to view the process.")

if __name__ == "__main__":
    asyncio.run(main())
