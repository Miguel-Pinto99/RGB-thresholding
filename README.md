# RGB_Thresholding

## Description

Repository which holds a simple Python application that allows users to select thresholding values using radio buttons while capturing video from a webcam and then saved them to a json file. This tool is useful for experimenting with different thresholding techniques in real-time, aiding in computer vision projects.

![Screenshot 2024-10-19 180124](https://github.com/user-attachments/assets/5f4915c0-57ad-49ad-afc8-56396e191ad3)

## Features

- Adjustable thresholding values using radio buttons
- Supports input from webcam or local image
- Supports two color models (HSV and RGB)

## Tools

- Python 3.x
- OpenCV
- NumPy
- uv
- pre-commit
- Pyside6

## Setup

```
uv pip install -r requirements.txt
```

## Using Pre-Commit Hooks
Install pre-commit:
```
pre-commit install
```

Run all hooks manually:
```
pre-commit run --all-files
```

## Usage

1-Run the script:

```
uv run rgb_thresholding.py
```

2- Select the image source and the color representation.

![image](https://github.com/user-attachments/assets/02ebef1d-a829-4abb-a22b-ba54b2ea3bb2)

3- A window will open displaying the webcam feed. Use the radio buttons to select your desired thresholding limits and then press 'w'

4- Apply limits to an image:

```
uv run apply_limits.py
```

Dont forget to change the input.

## Instructions

```
w- write limits to json file
q- Load last saved limits
m/n- Change to RGB/HSV representation
e- exit
```

