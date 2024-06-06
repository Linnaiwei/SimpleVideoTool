## Introduction
SimpleVideoTool is a tool for handling simple, repetitive but troublesome video processing tasks. The current version provides two versions: a standard version and a GPU-accelerated version.

## Completed functionality
- Splitting video files
- Merging video files

## Dependencies
- Python 3.7+
- Required Libraries:
  - `moviepy`
  - `tkinter`

## Installing Dependencies
Use pip to install the required libraries:
```bash
pip install moviepy tk
```
## GPU Driver and CUDA Version (for GPU-accelerated version only)
- NVIDIA Driver: 551.76 or newer
- CUDA Version: 11.1 or newer
- Hardware-accelerated ffmpeg
## How to Run
### Standard Version
1. Download and unzip the project.
2. Install dependencies:
```bash
pip install moviepy tk
```
3. Run the main program:
```bash
python video_tool.py
```
### GPU-accelerated Version
1. Ensure your system has the supported NVIDIA driver and CUDA toolkit installed.
2. Install hardware-accelerated ffmpeg:
- Download and install the ffmpeg with CUDA/NVENC support from: https://www.ffmpeg.org/download.html
3. Download and unzip the project.
4. Install dependencies:
```bash
pip install moviepy tk
```
5. Run the main program:
```bash
python video_tool_gpu.py
```
## Usage
### Split Video
1. Select the "Split Video" tab.
2. Click the "Browse" button to choose a video file.
3. Click the "Browse" button to choose the output folder.
4. Enter the clip length in seconds.
5. Click the "Split Video" button.
### Merge Videos
1. Select the "Merge Videos" tab.
2. Click the "Add Videos" button to add video files.
3. Use the "Move Up" or "Move Down" buttons to adjust the video order, or click "Default Sort" to sort by file name.
4. Click the "Browse" button to choose the output folder.
5. Click the "Merge Videos" button.

## Contribution
Feel free to submit issues and pull requests to contribute code and improve documentation.

## License
This project is licensed under the MIT License.