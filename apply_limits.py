#!/usr/bin/env python3

import cv2
import numpy as np
import json
import os

window_name = "Color Segmenter"


def main(image):
    """
    The main function reads parameters from a JSON file, applies thresholding and masking to an input image based on the
    mode specified in the JSON file, and returns the mask and masked image.

    :param image: The `main` function you provided seems to be processing an image based on parameters loaded from a JSON
    file. However, the code snippet you shared is incomplete as it ends abruptly after defining the function
    :return: The function `main(image)` is returning two variables: `mask` and `masked_image`.
    """

    # Build path to json folder and file
    root_dir = os.path.dirname(os.path.abspath(__file__))
    name_directory = "resources"
    name_subdirectory_json = "json"
    name_json_file = "limits.json"
    path_json_file = (
        f"{root_dir}\{name_directory}\{name_subdirectory_json}\{name_json_file}"
    )

    # Open Json file
    with open(path_json_file) as json_file:
        parameters = json.load(json_file)

    # Getting values from Json file
    mode = parameters["mode"]
    if mode == "HSV":
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mins = np.array(
            [
                parameters["limits"]["H"]["min"],
                parameters["limits"]["S"]["min"],
                parameters["limits"]["V"]["min"],
            ]
        )
        maxs = np.array(
            [
                parameters["limits"]["H"]["max"],
                parameters["limits"]["S"]["max"],
                parameters["limits"]["V"]["max"],
            ]
        )
    else:
        mins = np.array(
            [
                parameters["limits"]["B"]["min"],
                parameters["limits"]["G"]["min"],
                parameters["limits"]["R"]["min"],
            ]
        )
        maxs = np.array(
            [
                parameters["limits"]["B"]["max"],
                parameters["limits"]["G"]["max"],
                parameters["limits"]["R"]["max"],
            ]
        )

    # Thresholding and masks
    mask_thresh = cv2.inRange(image, mins, maxs)
    kernel = np.ones((2, 2), np.uint8)
    mask_open = cv2.morphologyEx(mask_thresh, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask_open, cv2.MORPH_CLOSE, kernel)
    masked_image = cv2.bitwise_and(image, image, mask=mask)
    if mode == "HSV":
        masked_image = cv2.cvtColor(masked_image, cv2.COLOR_HSV2BGR)
    return mask, masked_image


if __name__ == "__main__":
    root_dir = os.path.dirname(os.path.abspath(__file__))
    name_directory = "resources"
    name_subdirectory_images = "images"
    name_image_file = "colors.png"
    path_image_file = (
        f"{root_dir}\{name_directory}\{name_subdirectory_images}\{name_image_file}"
    )

    image = cv2.imread(path_image_file)
    mask, image = main(image)
    hori = np.concatenate((image, cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)), axis=1)
    cv2.imshow("Image", hori)
    cv2.waitKey(0)
