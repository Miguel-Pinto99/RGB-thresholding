
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

