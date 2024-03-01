
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as tk
import cv2
import numpy as np
from colorama import Fore, Style
import json
import os
from screeninfo import get_monitors
from tkinter import *

from mecheye.shared import *
from mecheye.area_scan_3d_camera import *
from mecheye.area_scan_3d_camera_utils import *


## Follow tutorial on teams

class ClassConnectAndCaptureImage(object):
    def __init__(self):
        # This class initializes various attributes related to capturing images and working with directories and monitor
        # information.
        self.camera = Camera()

        self.abspath = os.path.abspath(__file__)
        self.windowDir = os.path.normpath(os.getcwd())

        self.name_directory = 'resources'
        self.name_subdirectory_json = 'json'
        self.name_json_file = 'limits.json'
        self.path_json_file = fr'{self.windowDir}\{self.name_directory}\{self.name_subdirectory_json}\{self.name_json_file}'
        self.path_json_file_exists = os.path.exists(self.path_json_file)

        self.info_pc = get_monitors()
        self.height_monitor = self.info_pc[0].height
        self.width_monitor = self.info_pc[0].width

        self.window_name = 'Color Segmenter'

    def onTrackbar(self, image, mode):

        """
        The function `onTrackbar` reads trackbar values for color thresholds, sets limits based on mode (RGB or HSV),
        creates a mask, applies the mask to the image, and displays the result.

        :param image: The `image` parameter in the `onTrackbar` function is the input image that you want to apply
        thresholding on based on the trackbar values set by the user. The function reads trackbar values for different color
        channels (B/H, G/S, R/V) and then creates a
        :param mode: The `mode` parameter in the `onTrackbar` function is used to specify whether the thresholding should be
        done in RGB color space or HSV color space. It determines how the trackbar values for each channel (B/G/R or H/S/V)
        should be interpreted and applied to create the
        :return: The function `onTrackbar` returns the `parameters` dictionary, which contains the limits for the color
        channels (either RGB or HSV) based on the trackbar values set by the user.
        """


        # Reading Trackbars (High is equal or bigger than Low)
        Threshold_LOW_B_H = cv2.getTrackbarPos('LOW B/H', self.window_name)
        Threshold_HIGH_B_H = cv2.getTrackbarPos('HIGH B/H', self.window_name)

        # Condition that prevents a minimal input higher than the maximum input
        if Threshold_HIGH_B_H < Threshold_LOW_B_H:
            cv2.setTrackbarPos('HIGH B/H', self.window_name, Threshold_LOW_B_H)

        Threshold_LOW_G_S = cv2.getTrackbarPos('LOW G/S', self.window_name)
        Threshold_HIGH_G_S = cv2.getTrackbarPos('HIGH G/S', self.window_name)
        if Threshold_HIGH_G_S < Threshold_LOW_G_S:
            cv2.setTrackbarPos('HIGH G/S', self.window_name, Threshold_LOW_G_S)

        Threshold_LOW_R_V = cv2.getTrackbarPos('LOW R/V', self.window_name)
        Threshold_HIGH_R_V = cv2.getTrackbarPos('HIGH R/V', self.window_name)
        if Threshold_HIGH_R_V < Threshold_LOW_R_V:
            cv2.setTrackbarPos('HIGH R/V', self.window_name, Threshold_LOW_R_V)

        # Defining limits by mode (HSV or RGB)
        if mode == 'RGB':

            print('\n\nNew threshold defined by:\n')
            print(Fore.BLUE + 'TH_B_min = ' + Style.RESET_ALL + str(
                Threshold_LOW_B_H) + Fore.BLUE + ', TH_B_max = ' + Style.RESET_ALL + str(Threshold_HIGH_B_H))
            print(Fore.GREEN + 'TH_G_min = ' + Style.RESET_ALL + str(
                Threshold_LOW_G_S) + Fore.GREEN + ', TH_G_max = ' + Style.RESET_ALL + str(Threshold_HIGH_G_S))
            print(Fore.RED + 'TH_R_min = ' + Style.RESET_ALL + str(
                Threshold_LOW_R_V) + Fore.RED + ', TH_R_max = ' + Style.RESET_ALL + str(Threshold_HIGH_R_V))

            parameters = {'limits': {'B': {'min': Threshold_LOW_B_H, 'max': Threshold_HIGH_B_H},
                                          'G': {'min': Threshold_LOW_G_S, 'max': Threshold_HIGH_G_S},
                                          'R': {'min': Threshold_LOW_R_V, 'max': Threshold_HIGH_R_V}}
                          ,
                          'mode': mode
                          }

            mins = np.array([parameters['limits']['B']['min'], parameters['limits']['G']['min'],
                             parameters['limits']['R']['min']])
            maxs = np.array([parameters['limits']['B']['max'], parameters['limits']['G']['max'],
                             parameters['limits']['R']['max']])

        else:

            print('\n\nNew threshold defined by:\n')
            print(Fore.CYAN + 'TH_H_min = ' + Style.RESET_ALL + str(
                Threshold_LOW_B_H) + Fore.CYAN + ', TH_H_max = ' + Style.RESET_ALL + str(Threshold_HIGH_B_H))
            print(Fore.MAGENTA + 'TH_S_min = ' + Style.RESET_ALL + str(
                Threshold_LOW_G_S) + Fore.MAGENTA + ', TH_S_max = ' + Style.RESET_ALL + str(Threshold_HIGH_G_S))
            print(Fore.LIGHTBLUE_EX + 'TH_V_min = ' + Style.RESET_ALL + str(
                Threshold_LOW_R_V) + Fore.LIGHTBLUE_EX + ', TH_V_max = ' + Style.RESET_ALL + str(Threshold_HIGH_R_V))

            parameters = {'limits': {'H': {'min': Threshold_LOW_B_H, 'max': Threshold_HIGH_B_H},
                                          'S': {'min': Threshold_LOW_G_S, 'max': Threshold_HIGH_G_S},
                                          'V': {'min': Threshold_LOW_R_V, 'max': Threshold_HIGH_R_V}}
                               ,
                               'mode': mode
                               }

            mins = np.array([parameters['limits']['H']['min'], parameters['limits']['S']['min'],
                             parameters['limits']['V']['min']])
            maxs = np.array([parameters['limits']['H']['max'], parameters['limits']['S']['max'],
                             parameters['limits']['V']['max']])

        # Creating Mask with limits defined
        mask = cv2.inRange(image, mins, maxs)
        image_masked = cv2.bitwise_and(image,image,mask= mask)

        rgb_mask = cv2.cvtColor(mask,cv2.COLOR_GRAY2RGB)

        all = np.concatenate((rgb_mask,image_masked), axis=1)
        cv2.imshow(self.window_name, all)

        return parameters

    def set_old_values(self):

        """
        The function `set_old_values` reads values from a JSON file and sets trackbar positions in a window based on the
        retrieved values.
        """
        # Open Json file
        with open(self.path_json_file, 'r') as json_file:
            parameters = json.load(json_file)

        # Getting values from Json file
        mode = parameters['mode']
        if mode == 'HSV':

            mins = np.array([parameters['limits']['H']['min'], parameters['limits']['S']['min'],
                             parameters['limits']['V']['min']])
            maxs = np.array([parameters['limits']['H']['max'], parameters['limits']['S']['max'],
                             parameters['limits']['V']['max']])
        else:
            mins = np.array([parameters['limits']['B']['min'], parameters['limits']['G']['min'],
                             parameters['limits']['R']['min']])
            maxs = np.array([parameters['limits']['B']['max'], parameters['limits']['G']['max'],
                             parameters['limits']['R']['max']])

        cv2.setTrackbarPos('LOW B/H', self.window_name, mins[0])
        cv2.setTrackbarPos('HIGH B/H', self.window_name, maxs[0])
        cv2.setTrackbarPos('LOW G/S', self.window_name, mins[1])
        cv2.setTrackbarPos('HIGH G/S', self.window_name, maxs[1])
        cv2.setTrackbarPos('LOW R/V', self.window_name, mins[2])
        cv2.setTrackbarPos('HIGH R/V', self.window_name, maxs[2])

    def set_init_parameters(self):

        """
        The function `set_init_parameters` creates a Tkinter window with combo boxes for selecting image representation mode
        and source, and returns the selected values.
        :return: The `set_init_parameters` function returns the selected mode and source values from the Tkinter combo boxes
        after the user has made their selections.
        """

        #Creating Tkinter combo box for user input type of photo
        mode = ''
        source = ''
        valid_boxes_mode = ['RGB', 'HSV']
        valid_boxes_source = ['Picture','WebCam','MM']

        # Creating buttons, setting size and title
        window = tk.Tk()
        window.title('Image thresholding')
        window.iconbitmap(fr'resources\icons\affix_logo.ico')

        width = 400
        height = 200

        height_monitor = self.height_monitor
        width_monitor = self.width_monitor

        x = (width_monitor / 2) - (width / 2)
        y = (height_monitor / 2) - (height / 2)
        window.geometry('%dx%d+%d+%d' % (width, height, x, y))

        label = Label(window, text="Select setings",font= ('Helvetica 15 bold'))
        label.grid(row = 0, column = 1, sticky = W, pady = 10)
        l1 = Label(window, text="Represention:")
        l2 = Label(window, text="Source:")
        l1.grid(row=1, column=0, sticky=W, pady=2)
        l2.grid(row=2, column=0, sticky=W, pady=2)

        option_select_mode = ttk.Combobox(window, values=valid_boxes_mode)
        option_select_mode.grid(row=1, column=1, sticky=W, pady=2)
        option_select_source = ttk.Combobox(window, values=valid_boxes_source)
        option_select_source.grid(row=2, column=1, sticky=W, pady=2)
        option_button = ttk.Button(window, text="Select the box", command=window.quit)
        option_button.grid(row=3, column=1, sticky=W, pady=10)

        # option_select_mode.pack(anchor="n")
        # option_select_source.pack(anchor="n")
        # option_button.pack(anchor="n")

        window.mainloop()
        mode = option_select_mode.get()
        source = option_select_source.get()

        if mode != "" and source != "":
            window.destroy()
            return mode,source

    def createTrackBars(self):

        """
        The function `createTrackBars` creates track bars for adjusting color thresholds in an OpenCV window.
        """
        # Create Track bars
        min_threshold = 0
        max_threshold = 255
        cv2.namedWindow(self.window_name)
        cv2.moveWindow(self.window_name, 0, 0)

        cv2.createTrackbar('LOW B/H', self.window_name, min_threshold, max_threshold, self.onTrackbar)
        cv2.createTrackbar('HIGH B/H', self.window_name, min_threshold, max_threshold, self.onTrackbar)
        cv2.createTrackbar('LOW G/S', self.window_name, min_threshold, max_threshold, self.onTrackbar)
        cv2.createTrackbar('HIGH G/S', self.window_name, min_threshold, max_threshold, self.onTrackbar)
        cv2.createTrackbar('LOW R/V', self.window_name, min_threshold, max_threshold, self.onTrackbar)
        cv2.createTrackbar('HIGH R/V', self.window_name, min_threshold, max_threshold, self.onTrackbar)

    def keyboard_functions(self,key,parameters):

        """
        The function `keyboard_functions` handles key presses for writing data to a text file, exiting the program, and
        setting old values if a file exists.

        :param key: The `key` parameter in the `keyboard_functions` method seems to represent the key that was pressed by
        the user. It is checked against certain conditions using the `ord` function to determine the action to be taken
        based on the key pressed. In this case, the `ord` function converts the
        :param parameters: It seems like you forgot to provide the details of the `parameters` variable. Could you please
        share the content or structure of the `parameters` variable so that I can assist you further with the
        `keyboard_functions` method?
        """

        # Writing limits data in text file
        if key == ord('w'):
            with open(self.path_json_file, 'w') as file_handle:
                print('You pressed "w" (write). Writing limits to file ' + self.path_json_file)
                json.dump(parameters, file_handle)

        if key == ord('e'):
            print('You pressed "e" (exit). Program Finished!')
            exit()

        if key == ord('q'):
            if self.path_json_file_exists:
                self.set_old_values()


    def process_image(self,image):

        """
        The function processes an image by resizing it, applying morphological opening and closing operations using a
        kernel, and then returning the processed image.

        :param image: The code you provided seems to be a method for processing an image. It resizes the image to a specific
        width and height, applies morphological operations (opening and closing) using a kernel of size (2, 2), and then
        returns the processed image
        :return: the processed image after resizing and applying morphological operations (opening and closing) using the
        given kernel.
        """

        width_monitor = self.width_monitor
        height_monitor = self.height_monitor

        x = round(width_monitor / 2)
        y = round(height_monitor/1.65)

        image = cv2.resize(image, (x, y))

        kernel = np.ones((2, 2), np.uint8)
        image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
        image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)

        return image

    def get_image_Picture(self,mode):

        """
        This function allows the user to select an image file, convert it to HSV mode if specified, process the image,
        display it, and interact with trackbars and keyboard functions.

        :param mode: The `mode` parameter in the `get_image_Picture` function is used to specify the color space conversion
        mode for the image processing. It can take on the values 'HSV' or any other mode supported by OpenCV
        """

        filetype = (("Image files (*.png, *.jpg, *.bmp)", "*.png *.jpg *.bmp"), ("All Files", "*.*"))
        path_filename = tk.askopenfilenames(title="Select files...", initialdir=r".\\", filetypes=filetype)

        # Only if the user did not select any DXF files
        if path_filename:

            self.createTrackBars()

            while True:
                image = cv2.imread(path_filename[0], cv2.IMREAD_COLOR)
                if mode == 'HSV':
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

                # Dilate and Close
                image = self.process_image(image)

                # Grab the parameters on the Trackbars
                parameters = self.onTrackbar(image, mode)
                cv2.imshow(fr'{mode} image', image)
                key = cv2.waitKey(20)

                self.keyboard_functions(key, parameters)

    def get_image_WebCam(self, mode):
        """
        This function captures images from a webcam, converts them to HSV color space if specified, processes the images,
        displays them, and allows for keyboard interactions.

        :param mode: The `mode` parameter in the `get_image_WebCam` function is used to specify the color space conversion
        mode for the captured image. It can take on the value of 'HSV' to convert the image from BGR to HSV color space
        """

        self.createTrackBars()
        capture = cv2.VideoCapture(0)

        while True:

            _, image = capture.read()  # get an image from the camera

            if mode == 'HSV':
                image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

            # Dilate and Close
            image = self.process_image(image)

            # Grab the parameters on the Trackbars
            parameters = self.onTrackbar(image, mode)
            cv2.imshow(fr'{mode} images',image)
            key = cv2.waitKey(20)

            self.keyboard_functions(key, parameters)

    def get_image_MM(self, mode):
        """
        This Python function captures images from a camera, processes them based on a specified mode (e.g., HSV), and
        displays the processed images with trackbars for parameter adjustment.

        :param mode: The `mode` parameter in the `get_image_MM` method is used to specify the color space conversion mode
        for the captured image. It can take on two possible values: 'HSV' or another value that is not specified in the
        provided code snippet
        """
        # Find existing Cameras
        if find_and_connect(self.camera):

            self.createTrackBars()

            while True:

                frame_2d = Frame2D()
                show_error(self.camera.capture_2d(frame_2d))
                if frame_2d.color_type() == ColorTypeOf2DCamera_Monochrome:
                    image2d = frame_2d.get_gray_scale_image()
                elif frame_2d.color_type() == ColorTypeOf2DCamera_Color:
                    image2d = frame_2d.get_color_image()

                image = image2d.data()

                if mode == 'HSV':
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

                # Dilate and Close
                image = self.process_image(image)

                # Grab the parameters on the Trackbars
                parameters = self.onTrackbar(image, mode)
                cv2.imshow(fr'{mode} image',image)
                key = cv2.waitKey(20)

                self.keyboard_functions(key, parameters)

    def check_file(self,mode):

        """
        This function checks if a JSON file exists, and if not, creates it with specific parameters based on the mode
        provided.

        :param mode: The `mode` parameter in the `check_file` method is used to determine whether the color space mode is
        'HSV' or 'RGB'. Depending on the value of `mode`, different parameters are set for the color space limits. If `mode`
        is 'HSV', the parameters include limits for
        """

        if self.path_json_file_exists is False:
            with open(self.path_json_file, "w+") as file:
                if mode == 'HSV':
                    parameters = {'limits': {'H': {'min': 0, 'max': 0},
                                             'S': {'min': 0, 'max': 0},
                                             'V': {'min': 0, 'max': 0}}
                        ,
                                  'mode': mode
                                  }
                elif mode == 'RGB':
                    parameters = {'limits': {'R': {'min': 0, 'max': 0},
                                             'G': {'min': 0, 'max': 0},
                                             'B': {'min': 0, 'max': 0}}
                        ,
                                  'mode': mode
                                  }
                file.write(str(parameters))
        else:
            pass

    def main(self):

        """
        The main function determines the mode and source of input, then calls different functions based on the source
        selected (Picture, WebCam, or MM).
        """

        # Get mode from combobox: HSV and RGB
        mode,source = self.set_init_parameters()
        self.check_file(mode)

        if source == 'Picture':
            self.get_image_Picture(mode)
        elif source == 'WebCam':
            self.get_image_WebCam(mode)
        elif source == 'MM':
            self.get_image_MM(mode)

if __name__ == '__main__':
    get_threshold_limits = ClassConnectAndCaptureImage()
    get_threshold_limits.main()

