# AutoDocs

AutoDocs is a smart documentation assistant for macOS. It monitors your browser interactions and records your voice to automatically generate step-by-step process guides in HTML and PDF formats.

## Features
- **Project Organization**: Automatically organizes recordings into named project folders.
- **Browser Orchestration**: Launches a dedicated Chromium instance to capture your actions.
- **Visual Capture**: Takes high-resolution screenshots on every click, input, and navigation event.
- **Audio Transcription**: Records your voice in real-time and uses OpenAI Whisper to generate accurate transcripts.
- **Smart Synthesis**: Intelligent alignment of your spoken instructions with the corresponding visual steps.
- **Dual Output**: Generates both web-ready HTML and professional PDF reports.

## Installation

### 1. Prerequisites
Ensure you have Python 3.9+ and the following system libraries installed (required for audio processing and PDF generation):

**macOS (via Homebrew):**
```bash
brew install ffmpeg pango libffi cairo gdk-pixbuf
```

### 2. Setup
Clone the repository and install the Python dependencies:

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install browser binaries
playwright install chromium
```

## Usage

1. **Activate Environment**:
   ```bash
   source venv/bin/activate
   ```

2. **Run AutoDocs**:
   ```bash
   python main.py
   ```

3. **Start Session**:
   - You will be prompted to enter a **Project Name** (e.g., "expense-report-howto").
   - A Chromium browser window will open automatically.

4. **Record**:
   - Navigate to the website you want to document.
   - Perform your tasks (click, type, navigate) normally.
   - **Explain your steps aloud** as you perform them. The audio will be transcribed and matched to the actions.

5. **Finish**:
   - simply **close the browser window** to stop recording.
   - Alternatively, press `Ctrl+C` in the terminal.

6. **View Results**:
   - Your documentation is saved in: `output/<project_name>/`
   - Open `report.html` or `report.pdf` to view your guide.

## Directory Structure

```
AutoDocs/
├── main.py                 # Application entry point
├── output/                 # Generated documentation (GitIgnored)
│   └── <project_name>/     # Your specific project folder
│       ├── report.html     # Final HTML guide
│       ├── report.pdf      # Final PDF guide
│       ├── recording.wav   # Raw audio recording
│       └── screenshot_*.png # Raw screenshots
├── recorder/               # Browser & Audio recording logic
├── processing/             # Transcription & Synchronization logic
├── reporting/              # HTML/PDF generation logic
└── requirements.txt        # Python dependencies
```

## Configuration
- **Whisper Model**: You can adjust the transcription accuracy/speed by changing `model_size` in `main.py` (default: `base`). Options: `tiny`, `base`, `small`, `medium`, `large`.
- **Templates**: HTML templates are located in `reporting/templates/`. You can modify `report.html` to customize the branding or layout.

## Troubleshooting
- **Permission Errors**: If audio recording fails, ensure your terminal application (e.g., Terminal, iTerm2, VS Code) has permission to access the Microphone in macOS System Settings > Privacy & Security.
- **Browser Errors**: If the browser fails to launch, try running `playwright install chromium` again.
