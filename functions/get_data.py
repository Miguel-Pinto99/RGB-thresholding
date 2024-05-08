import os

from mecheye.shared import *
from mecheye.area_scan_3d_camera import *
from mecheye.area_scan_3d_camera_utils import find_and_connect

import cv2
import tkinter as tk

class Get_Data:

    def __init__(self):

        self.image2d = None
        self.initialized = False
        self.frame_2d = None
        self.camera = None


    def get_image_Picture(self,mode):

        """
        This function retrieves an image file for processing.
        :return: the image that was captured or loaded based on the condition of whether the program has been initialized or
        not.
        """

        image2d = self.image2d
        initialized = self.initialized

        if not initialized:

            filetype = (("Image files (*.png, *.jpg, *.bmp)", "*.png *.jpg *.bmp"), ("All Files", "*.*"))
            path_filename = tk.askopenfilenames(title="Select files...", initialdir=r".\\", filetypes=filetype)

            self.initialized = True
            self.image2d = cv2.imread(path_filename[0], cv2.IMREAD_COLOR)

        image = image2d
        if mode == 'HSV':
            image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        return image

    def get_image_WebCam(self, mode):
        """
        This function captures images from a webcam, converts them to HSV color space if specified, processes the images,
        displays them, and allows for keyboard interactions.

        :param mode: The `mode` parameter in the `get_image_WebCam` function is used to specify the color space conversion
        mode for the captured image. It can take on the value of 'HSV' to convert the image from BGR to HSV color space
        """

        image2d = self.image2d
        initialized = self.initialized

        if not initialized:
            image2d = cv2.VideoCapture(0)
            self.initialized = True
            self.image2d = image2d

        _, image = image2d.read()
        if mode == 'HSV':
            image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        return image


    def get_image_MM(self, mode):
        """
        This Python function captures images from a camera, processes them based on a specified mode (e.g., HSV), and
        displays the processed images with trackbars for parameter adjustment.

        :param mode: The `mode` parameter in the `get_image_MM` method is used to specify the color space conversion mode
        for the captured image. It can take on two possible values: 'HSV' or another value that is not specified in the
        provided code snippet
        """

        initialized = self.initialized
        camera = self.camera

        if not initialized:
            camera = Camera()
            find_and_connect(camera)

            self.initialized = True
            self.camera = camera

        frame2d = Frame2D()
        camera.capture_2d(frame2d)

        if frame2d.color_type() == ColorTypeOf2DCamera_Monochrome:
            image2d = frame2d.get_gray_scale_image()
        elif frame2d.color_type() == ColorTypeOf2DCamera_Color:
            image2d = frame2d.get_color_image()

        image = image2d.data()

        if mode == 'HSV' and frame2d.color_type() == ColorTypeOf2DCamera_Color:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        elif mode == 'HSV' and frame2d.color_type() == ColorTypeOf2DCamera_Monochrome:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        return image