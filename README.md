# Panorama Stitching App

A desktop application for stitching multiple images into a panorama using OpenCV,
with a PySide6 GUI for dataset selection, preview, and export.

## Folder Structure
```
project/
├── dataset/
│   └── [folder_name]/     # put your image sets here
├── output/                # saved panoramas go here
├── stitching/
│   └── stitcher.py        # PanoramaStitcher class
├── gui/
│   ├── main_window.py     # MainWindow UI
│   └── styles.py          # app stylesheet
└── main.py
```

## Installation
```bash
pip install opencv-python numpy PySide6
```

## Usage
```bash
python main.py
```

1. Select a dataset folder from the dropdown
2. Preview the input images in the scroll area
3. Click **Run Stitching** to generate the panorama
4. Click **Save Panorama** to export as `.jpg` or `.png`

## How It Works

| Module | Responsibility |
|---|---|
| `PanoramaStitcher` | Loads images, runs `cv2.Stitcher`, crops black borders |
| `MainWindow` | GUI — dataset selector, image thumbnails, panorama preview |
| `dataset_scanner` | Lists available subfolders inside `dataset/` |

## Image Requirements
- At least 2 images per dataset folder
- Sufficient overlap between consecutive shots (~50–70%)
- Supported formats: `.jpg`, `.jpeg`, `.png`, `.bmp`

## Results
![panorama](https://github.com/user-attachments/assets/744c0a31-f6d6-4ab0-965c-1b798456196a)

## Image 1
![006](https://github.com/user-attachments/assets/fc1c5dfb-54fc-4a6a-b1c8-da402ebd9f09)
## Image 2
![007](https://github.com/user-attachments/assets/f221044c-5f67-4330-baba-56c100455e57)
## Result
![panorama_building](https://github.com/user-attachments/assets/844bd905-d5a9-4016-8054-ece922496c7c)

## GUI
<img width="996" height="630" alt="image" src="https://github.com/user-attachments/assets/63dc2def-e8b5-4ee4-af50-1aea9a4a3200" />

