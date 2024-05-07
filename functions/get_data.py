import os

from mecheye.area_scan_3d_camera_utils import *
import cv2
import tkinter as tk

class Get_Data:

    def __init__(self):

        self.image_to_capture = ''
        self.initialized = False

    def get_image_Picture(self,mode):

        """
        This function retrieves an image file for processing.
        :return: the image that was captured or loaded based on the condition of whether the program has been initialized or
        not.
        """

        image_to_capture = self.image_to_capture
        initialized = self.initialized

        if not initialized:

            filetype = (("Image files (*.png, *.jpg, *.bmp)", "*.png *.jpg *.bmp"), ("All Files", "*.*"))
            path_filename = tk.askopenfilenames(title="Select files...", initialdir=r".\\", filetypes=filetype)

            self.initialized = True
            self.image_to_capture = cv2.imread(path_filename[0], cv2.IMREAD_COLOR)

        image = image_to_capture
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

        image_to_capture = self.image_to_capture
        initialized = self.initialized

        if not initialized:
            image_to_capture = cv2.VideoCapture(0)
            self.initialized = True
            self.image_to_capture = image_to_capture

        _, image = image_to_capture.read()
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

        image_to_capture = self.image_to_capture
        initialized = self.initialized

        if not initialized:
            camera = Camera()
            find_and_connect(Camera())
            frame_2d = Frame2D()
            show_error(camera.capture_2d(frame_2d))
            if frame_2d.color_type() == ColorTypeOf2DCamera_Monochrome:
                image2d = frame_2d.get_gray_scale_image()
            elif frame_2d.color_type() == ColorTypeOf2DCamera_Color:
                image2d = frame_2d.get_color_image()

            self.initialized = True
            self.image_to_capture = image2d

        _, image = image_to_capture.data()
        if mode == 'HSV':
            image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        return image