# AutoDocs

AutoDocs is a Python-based desktop application that generates automated process documentation by monitoring your browser interactions and recording your voice. It outputs a step-by-step guide in HTML and PDF formats.

## Features
- **Browser Orchestration**: Automatically launches a Chromium instance to capture your actions.
- **Visual Capture**: Takes high-resolution screenshots on every click, input, and navigation.
- **Audio Transcription**: Records your voice and uses OpenAI Whisper to transcribe your explanations.
- **Smart Synthesis**: Aligns your spoken instructions with the corresponding visual steps.
- **Reports**: Generates clean, formatted HTML and PDF reports.

## Installation

1. **Prerequisites**:
   - Python 3.9+
   - `ffmpeg` (Required for Whisper)
   - `pango` (Required for PDF generation)

   On macOS:
   ```bash
   brew install ffmpeg pango libffi cairo gdk-pixbuf
   ```

2. **Install Dependencies**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   playwright install chromium
   ```

## Usage

1. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

2. Run the application:
   ```bash
   python main.py
   ```

3. **Interact**:
   - The browser will open. Navigate to the website you want to document.
   - Perform actions (click, type) while describing them aloud.

4. **Stop**:
   - Simply **close the browser window** to finish the session.
   - Alternatively, press `Ctrl+C` in the terminal.

5. **View Report**:
   - Open `report.html` or `report.pdf` in the project directory.

## Configuration
- **Model**: You can change the Whisper model size in `main.py` (default: `base`).
- **Reporting**: Templates are located in `reporting/templates/`.
