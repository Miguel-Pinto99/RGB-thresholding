import cv2
import numpy as np
from colorama import Fore, Style
import json
import os
from typing import Any


class Window_Adjust_Threshold:
    def __init__(self):
        self.window_dir = os.path.normpath(os.getcwd())
        self.name_directory = "resources"
        self.name_subdirectory_json = "json"
        self.name_json_file = "limits.json"
        self.path_json_file = rf"{self.window_dir}\{self.name_directory}\{self.name_subdirectory_json}\{self.name_json_file}"
        self.path_json_file_exists = os.path.exists(self.path_json_file)

        self.window_name = "Color Segmenter"

    def get_trackbar_parameters(self, image: np.ndarray, mode: str) -> dict[str, Any]:
        Threshold_LOW_B_H = cv2.getTrackbarPos("LOW B/H", self.window_name)
        Threshold_HIGH_B_H = cv2.getTrackbarPos("HIGH B/H", self.window_name)

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

        mask = cv2.inRange(image, mins, maxs)
        image_masked = cv2.bitwise_and(image, image, mask=mask)

        rgb_mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)

        all = np.concatenate((rgb_mask, image_masked), axis=1)
        cv2.imshow(self.window_name, all)

        return parameters

    def set_old_values(self) -> None:
        with open(self.path_json_file) as json_file:
            parameters = json.load(json_file)

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

    def create_trackBars(self) -> None:
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

    def check_file(self, mode: str) -> None:
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

    def keyboard_functions(
        self, key: int, mode: str, parameters: dict[str, Any]
    ) -> str:
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
