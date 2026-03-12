# YouTube Downloader Application

## Setup Instructions
1. **Clone the repository**:
   ```bash
   git clone https://github.com/fishcake-coder/ytd.git
   cd ytd
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Features
- Download videos from YouTube in various formats.
- Support for playlists and channels.
- Option to download audio only.
- User-friendly command-line interface.

## Usage
1. **Basic video download**:
   ```bash
   python ytd.py <YouTube_URL>
   ```
2. **Download audio only**:
   ```bash
   python ytd.py <YouTube_URL> --audio
   ```
3. **Download playlist**:
   ```bash
   python ytd.py <Playlist_URL> --playlist
   ```

## Troubleshooting
- **Q: Video download failed**?  
   A: Ensure the URL is correct and the video is available.

- **Q: Permissions error**?  
   A: Check your write permissions to the download directory.

- **Q: Missing dependencies**?  
   A: Run `pip install -r requirements.txt` to install the necessary packages.

For further issues, please refer to the [GitHub Issues](https://github.com/fishcake-coder/ytd/issues) page.