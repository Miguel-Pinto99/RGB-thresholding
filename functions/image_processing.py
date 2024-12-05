import numpy as np
from screeninfo import get_monitors
import cv2


class Image_Processing:
    def prepare_image(image):
        info_pc = get_monitors()
        height_monitor = info_pc[0].height
        width_monitor = info_pc[0].width

        x = round(width_monitor / 2)
        y = round(height_monitor / 1.65)

        image = cv2.resize(image, (x, y))

        kernel = np.ones((2, 2), np.uint8)
        image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
        image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)

        return image
