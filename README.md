# RGB-Thresholding

## Description

Repository which holds a simple Python application that allows users to select thresholding values using radio buttons while capturing video from a webcam and then saved them to a json file. This tool is useful for experimenting with different thresholding techniques in real-time, aiding in computer vision projects.

![Screenshot 2024-10-19 180124](https://github.com/user-attachments/assets/5f4915c0-57ad-49ad-afc8-56396e191ad3)

## Features

- Adjustable thresholding values using radio buttons
- Supports input from webcam or local image
- Supports two color models (HSV and RGB)

## Tools and Libraries
This project utilizes the following tools and libraries:

- **Reflex**: A framework for building reactive web applications. [Reflex Documentation](https://reflex.dev/docs)
- **UV**: A Python library for running applications. [UV Documentation](https://docs.astral.sh/uv/getting-started/installation/)
- **pre-commit**: A framework for managing and maintaining multi-language pre-commit hooks. [pre-commit Documentation](https://pre-commit.com)

## Usage
1. Clone the repository:
    ```bash
    git clone https://github.com/Miguel-Pinto99/RGB-thresholding.git
    ```

2. Install UV:
    ```bash
    pip install uv
    ```

3. Navigate to the project directory:
    ```bash
    cd RGB-thresholding
    ```

4. Run the script:
    ```bash
    uv run rgb_thresholding.py
    ```

5. Select the image source and the color representation.

    ![image](https://github.com/user-attachments/assets/02ebef1d-a829-4abb-a22b-ba54b2ea3bb2)

6. A window will open displaying the webcam feed. Use the radio buttons to select your desired thresholding limits and then press 'w'.

7. Apply limits to an image:
    ```bash
    uv run apply_limits.py
    ```

    Don't forget to change the input.

## Instructions

```
w- write limits to json file
q- Load last saved limits
m/n- Change to RGB/HSV representation
e- exit
```
