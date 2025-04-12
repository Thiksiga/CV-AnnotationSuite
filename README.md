# CV-AnnotationSuite
Custom image annotation tool implemented from scratch using OpenCV library functions.

This Python script provides a graphical interface to annotate an image using the mouse and crop regions of interest. It allows users to draw rectangles on the image, save the coordinates, and automatically crop and save the selected regions.

## Features
- Draw rectangles on an image using the mouse.
- Toggle between rectangle and circle drawing modes.
- Save the annotated regions as cropped images.
- Logs all significant events (e.g., cropping success, invalid coordinates) to a timestamped log file.

## Requirements
- Python 3.11
- OpenCV (`cv2`)
- Logging
- `datetime`
- `os`

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/image-annotation-tool.git
   cd image-annotation-tool
