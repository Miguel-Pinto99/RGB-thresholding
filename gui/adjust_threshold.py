import cv2
import numpy as np
from colorama import Fore, Style
import json
import os


class Window_Adjust_Threshold:
    def __init__(self):
        # This class initializes various attributes related to capturing images and working with directories and monitor
        # information.

        self.window_dir = os.path.normpath(os.getcwd())
        self.name_directory = "resources"
        self.name_subdirectory_json = "json"
        self.name_json_file = "limits.json"
        self.path_json_file = rf"{self.window_dir}\{self.name_directory}\{self.name_subdirectory_json}\{self.name_json_file}"
        self.path_json_file_exists = os.path.exists(self.path_json_file)

        self.window_name = "Color Segmenter"

    def get_trackbar_parameters(self, image, mode):
        """
        The function `get_trackbar_parameters` reads trackbar values for color thresholds, sets limits based on mode (RGB or HSV),
        creates a mask, applies the mask to the image, and displays the result.

        :param image: The `image` parameter in the `get_trackbar_parameters` function is the input image that you want to apply
        thresholding on based on the trackbar values set by the user. The function reads trackbar values for different color
        channels (B/H, G/S, R/V) and then creates a
        :param mode: The `mode` parameter in the `get_trackbar_parameters` function is used to specify whether the thresholding should be
        done in RGB color space or HSV color space. It determines how the trackbar values for each channel (B/G/R or H/S/V)
        should be interpreted and applied to create the
        :return: The function `get_trackbar_parameters` returns the `parameters` dictionary, which contains the limits for the color
        channels (either RGB or HSV) based on the trackbar values set by the user.
        """

        # Reading Trackbars (High is equal or bigger than Low)
        Threshold_LOW_B_H = cv2.getTrackbarPos("LOW B/H", self.window_name)
        Threshold_HIGH_B_H = cv2.getTrackbarPos("HIGH B/H", self.window_name)

        # Condition that prevents a minimal input higher than the maximum input
        if Threshold_HIGH_B_H < Threshold_LOW_B_H:
            cv2.setTrackbarPos("HIGH B/H", self.window_name, Threshold_LOW_B_H)

        Threshold_LOW_G_S = cv2.getTrackbarPos("LOW G/S", self.window_name)
        Threshold_HIGH_G_S = cv2.getTrackbarPos("HIGH G/S", self.window_name)
        if Threshold_HIGH_G_S < Threshold_LOW_G_S:
            cv2.setTrackbarPos("HIGH G/S", self.window_name, Threshold_LOW_G_S)

        Threshold_LOW_R_V = cv2.getTrackbarPos("LOW R/V", self.window_name)
        Threshold_HIGH_R_V = cv2.getTrackbarPos("HIGH R/V", self.window_name)
        if Threshold_HIGH_R_V < Threshold_LOW_R_V:
            cv2.setTrackbarPos("HIGH R/V", self.window_name, Threshold_LOW_R_V)

        # Defining limits by mode (HSV or RGB)
        if mode == "RGB":
            print("\n\nNew threshold defined by:\n")
            print(
                Fore.BLUE
                + "TH_B_min = "
                + Style.RESET_ALL
                + str(Threshold_LOW_B_H)
                + Fore.BLUE
                + ", TH_B_max = "
                + Style.RESET_ALL
                + str(Threshold_HIGH_B_H)
            )
            print(
                Fore.GREEN
                + "TH_G_min = "
                + Style.RESET_ALL
                + str(Threshold_LOW_G_S)
                + Fore.GREEN
                + ", TH_G_max = "
                + Style.RESET_ALL
                + str(Threshold_HIGH_G_S)
            )
            print(
                Fore.RED
                + "TH_R_min = "
                + Style.RESET_ALL
                + str(Threshold_LOW_R_V)
                + Fore.RED
                + ", TH_R_max = "
                + Style.RESET_ALL
                + str(Threshold_HIGH_R_V)
            )

            parameters = {
                "limits": {
                    "B": {"min": Threshold_LOW_B_H, "max": Threshold_HIGH_B_H},
                    "G": {"min": Threshold_LOW_G_S, "max": Threshold_HIGH_G_S},
                    "R": {"min": Threshold_LOW_R_V, "max": Threshold_HIGH_R_V},
                },
                "mode": mode,
            }

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

        else:
            print("\n\nNew threshold defined by:\n")
            print(
                Fore.CYAN
                + "TH_H_min = "
                + Style.RESET_ALL
                + str(Threshold_LOW_B_H)
                + Fore.CYAN
                + ", TH_H_max = "
                + Style.RESET_ALL
                + str(Threshold_HIGH_B_H)
            )
            print(
                Fore.MAGENTA
                + "TH_S_min = "
                + Style.RESET_ALL
                + str(Threshold_LOW_G_S)
                + Fore.MAGENTA
                + ", TH_S_max = "
                + Style.RESET_ALL
                + str(Threshold_HIGH_G_S)
            )
            print(
                Fore.LIGHTBLUE_EX
                + "TH_V_min = "
                + Style.RESET_ALL
                + str(Threshold_LOW_R_V)
                + Fore.LIGHTBLUE_EX
                + ", TH_V_max = "
                + Style.RESET_ALL
                + str(Threshold_HIGH_R_V)
            )

            parameters = {
                "limits": {
                    "H": {"min": Threshold_LOW_B_H, "max": Threshold_HIGH_B_H},
                    "S": {"min": Threshold_LOW_G_S, "max": Threshold_HIGH_G_S},
                    "V": {"min": Threshold_LOW_R_V, "max": Threshold_HIGH_R_V},
                },
                "mode": mode,
            }

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

        # Creating Mask with limits defined
        mask = cv2.inRange(image, mins, maxs)
        image_masked = cv2.bitwise_and(image, image, mask=mask)

        rgb_mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)

        all = np.concatenate((rgb_mask, image_masked), axis=1)
        cv2.imshow(self.window_name, all)

        return parameters

    def set_old_values(self):
        """
        The function `set_old_values` reads values from a JSON file and sets trackbar positions in a window based on the
        retrieved values.
        """
        # Open Json file
        with open(self.path_json_file) as json_file:
            parameters = json.load(json_file)

        # Getting values from Json file
        mode = parameters["mode"]
        if mode == "HSV":
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

        cv2.setTrackbarPos("LOW B/H", self.window_name, mins[0])
        cv2.setTrackbarPos("HIGH B/H", self.window_name, maxs[0])
        cv2.setTrackbarPos("LOW G/S", self.window_name, mins[1])
        cv2.setTrackbarPos("HIGH G/S", self.window_name, maxs[1])
        cv2.setTrackbarPos("LOW R/V", self.window_name, mins[2])
        cv2.setTrackbarPos("HIGH R/V", self.window_name, maxs[2])

    def create_trackBars(self):
        """
        The function `createTrackBars` creates track bars for adjusting color thresholds in an OpenCV window.
        """
        # Create Track bars
        min_threshold = 0
        max_threshold = 255
        cv2.namedWindow(self.window_name)
        cv2.moveWindow(self.window_name, 0, 0)

        cv2.createTrackbar(
            "LOW B/H",
            self.window_name,
            min_threshold,
            max_threshold,
            self.get_trackbar_parameters,
        )
        cv2.createTrackbar(
            "HIGH B/H",
            self.window_name,
            min_threshold,
            max_threshold,
            self.get_trackbar_parameters,
        )
        cv2.createTrackbar(
            "LOW G/S",
            self.window_name,
            min_threshold,
            max_threshold,
            self.get_trackbar_parameters,
        )
        cv2.createTrackbar(
            "HIGH G/S",
            self.window_name,
            min_threshold,
            max_threshold,
            self.get_trackbar_parameters,
        )
        cv2.createTrackbar(
            "LOW R/V",
            self.window_name,
            min_threshold,
            max_threshold,
            self.get_trackbar_parameters,
        )
        cv2.createTrackbar(
            "HIGH R/V",
            self.window_name,
            min_threshold,
            max_threshold,
            self.get_trackbar_parameters,
        )

    def check_file(self, mode):
        """
        This function checks if a JSON file exists, and if not, creates it with specific parameters based on the mode
        provided.

        :param mode: The `mode` parameter in the `check_file` method is used to determine whether the color space mode is
        'HSV' or 'RGB'. Depending on the value of `mode`, different parameters are set for the color space limits. If `mode`
        is 'HSV', the parameters include limits for
        """

        if self.path_json_file_exists is False:
            with open(self.path_json_file, "w+") as file:
                if mode == "HSV":
                    parameters = {
                        "limits": {
                            "H": {"min": 0, "max": 0},
                            "S": {"min": 0, "max": 0},
                            "V": {"min": 0, "max": 0},
                        },
                        "mode": mode,
                    }
                elif mode == "RGB":
                    parameters = {
                        "limits": {
                            "R": {"min": 0, "max": 0},
                            "G": {"min": 0, "max": 0},
                            "B": {"min": 0, "max": 0},
                        },
                        "mode": mode,
                    }
                file.write(str(parameters))
        else:
            pass

    def keyboard_functions(self, key, mode, parameters):
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
        if key == ord("w"):
            with open(self.path_json_file, "w") as file_handle:
                print(
                    'You pressed "w" (write). Writing limits to file '
                    + self.path_json_file
                )
                json.dump(parameters, file_handle)

        elif key == ord("e"):
            print('You pressed "e" (exit). Program Finished!')
            exit()

        elif key == ord("q"):
            print('You pressed "q". Loaded old limits!')
            if self.path_json_file_exists:
                self.set_old_values()

        elif key == ord("m"):
            print('You pressed "m". HSV mode ON')
            mode = "HSV"

        elif key == ord("n"):
            print('You pressed "n". RGB mode ON')
            mode = "RGB"

        return mode
