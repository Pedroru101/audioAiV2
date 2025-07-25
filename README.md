# Audio Capture Widget

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![PySide6](https://img.shields.io/badge/PySide6-6.0+-green.svg)](https://pypi.org/project/PySide6/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://github.com/yourusername/audio-capture-widget)

Professional audio recording application with simultaneous microphone and system audio capture, featuring a minimalist floating interface and advanced functionality.

## Key Features

- **Simultaneous Recording**: Capture microphone and system audio in real-time
- **Source Selection**: Choose to record microphone only, system only, or both
- **Device Testing**: 3-second recording tests with instant playback
- **Configurable Chunks**: Automatic segments from 2-300 seconds
- **Webhook Integration**: Compatible with n8n and other webhook services
- **Floating Interface**: Minimalist, draggable, always-visible interface
- **Configuration Panel**: Animated panel with advanced options
- **Intelligent Mixing**: Real-time audio mixing with automatic normalization
- **Standalone Executable**: No Python installation required

## Installation

### Option 1: Executable (Recommended)
1. Download the [latest release](https://github.com/yourusername/audio-capture-widget/releases)
2. Run `AudioCaptureWidget.exe`
3. Ready to use!

### Option 2: From Source Code

#### 1. Clone the repository
```bash
git clone https://github.com/yourusername/audio-capture-widget.git
cd audio-capture-widget
```

#### 2. Create virtual environment
```bash
python -m venv venv
```

#### 3. Activate virtual environment
```bash
# Windows
.\venv\Scripts\activate

# Linux/Mac (experimental)
source venv/bin/activate
```

#### 4. Install dependencies
```bash
pip install -r requirements.txt
```

#### 5. Run the application
```bash
python main.py
```

## Usage Guide

### Quick Start
1. **Run**: Double-click `AudioCaptureWidget.exe` or run `python main.py`
2. **Configure**: Press the settings button to open configuration
3. **Select sources**: Check the boxes according to your needs:
   - **Microphone Only**: Voice/ambient recording
   - **System Only**: Capture application audio
   - **Both**: Complete recording (recommended)
4. **Test devices**: Use "Test" and "Play" buttons to verify functionality
5. **Record**: Press record button to start, stop button to end

### Advanced Configuration

#### Audio Devices
1. **Microphone**: Select your preferred input device
2. **System**: For system capture, we recommend VB-Audio Cable
3. **Testing**: Each device can be tested independently

#### Recording Options
- **Webhook URL**: Automatic sending to n8n or other services
- **Chunk Duration**: Segments from 2-300 seconds
- **Flexible Sources**: Combine or separate microphone and system

#### System Configuration
For system audio capture:
1. Install [VB-Audio Cable](https://vb-audio.com/Cable/)
2. Configure applications to use "CABLE Input"
3. Select "CABLE Output" in the application

## Project Structure

```
audio-capture-widget/
├── main.py                 # Main application
├── audio_handler.py        # Recording engine
├── audio_device_tester.py  # Device testing utilities
├── utils.py               # Utility functions
├── build.py               # Build script for executable
├── create_distribution.py # Distribution package creator
├── config.json            # Configuration file
├── requirements.txt       # Dependencies
├── assets/               # Resources
│   ├── icons/           # SVG icons
│   └── styles/          # CSS styles
├── temp_audio/          # Temporary audio files
└── grabaciones/         # Final recordings
```

## Configuration

The `config.json` file contains:

```json
{
  "input_device": 2,           // Microphone device ID
  "output_device": 1,          // System audio device ID
  "webhook_url": "http://...", // Webhook URL
  "chunk_duration": 4,         // Duration in seconds
  "record_microphone": true,   // Enable microphone recording
  "record_system": true        // Enable system audio recording
}
```

## Recommended Devices

### For Microphone:
- Any standard input device
- Prefer WASAPI or MME devices

### For System Audio:
- Devices with "loopback" in the name
- VB-Audio Cable (recommended)
- "Stereo Mix" or "What U Hear" (if enabled)

## Troubleshooting

### System audio not detected:
1. Install VB-Audio Cable
2. Configure applications to use "CABLE Input"
3. Select "CABLE Output" in the application

### "Input Overflow" errors:
1. Use MME devices instead of WASAPI
2. Increase chunk_duration to 8-10 seconds
3. Close other audio applications

### Stop button doesn't appear:
- Verify configuration is saved correctly
- Restart the application

## Dependencies

- **PySide6**: GUI framework
- **sounddevice**: Audio recording
- **numpy**: Numerical processing
- **scipy**: Audio analysis
- **pydub**: Audio manipulation (optional)
- **lameenc**: MP3 encoding (optional)
- **requests**: Webhook communication

## Supported Formats

- **Output**: WAV, MP3 (if pydub available)
- **Quality**: 44100Hz, 16-bit, mono/stereo
- **Compression**: MP3 128kbps (configurable)

## Workflow

1. **Configuration** → Device testing
2. **Recording** → Automatic chunks every X seconds
3. **Processing** → Mix microphone + system audio
4. **Sending** → Automatic webhook (optional)
5. **Storage** → Local files in temp_audio/

## Building Executable

To create your own executable:

```bash
# Install PyInstaller
pip install PyInstaller

# Build executable
python build.py

# Executable will be in dist/AudioCaptureWidget.exe
```

## Contributing

Contributions are welcome! Please:

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Changelog

### v1.0.0 (2024-07-22)
- Flexible recording source selection
- Independent device testing
- Improved VB-Audio Cable support
- Standalone executable packaging
- Clean and optimized project
- Complete documentation

## Known Issues

- **Windows Defender**: May flag executable as suspicious (false positive)
- **Microphone Permissions**: Windows may request permissions on first run
- **VB-Audio**: Requires separate installation for system capture

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [PySide6](https://pypi.org/project/PySide6/) - GUI framework
- [sounddevice](https://pypi.org/project/sounddevice/) - Audio capture
- [VB-Audio](https://vb-audio.com/) - Virtual audio solutions
- [PyInstaller](https://pyinstaller.org/) - Application packaging

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/audio-capture-widget/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/audio-capture-widget/discussions)
- **Contact**: Through GitHub

---

**Developed for professional audio recording**