import cv2
from functions.image_processing import Image_Processing
from gui.adjust_threshold import Window_Adjust_Threshold
from gui.select_parameters import Window_Select_Parameters
from functions.get_data import Get_Data


def main():
    window_select_parameters = Window_Select_Parameters()
    window_adjust_threshold = Window_Adjust_Threshold()
    get_data = Get_Data()

    mode, source = window_select_parameters.initialize()
    window_adjust_threshold.create_trackBars()

    while True:
        if source == "Picture":
            image = get_data.get_image_Picture(mode)
        elif source == "WebCam":
            image = get_data.get_image_WebCam(mode)
        else:
            raise Exception("No valid source")

        image = Image_Processing.prepare_image(image)
        parameters = window_adjust_threshold.get_trackbar_parameters(image, mode)
        cv2.imshow(r"Output image", image)
        key = cv2.waitKey(1)
        mode = window_adjust_threshold.keyboard_functions(key, mode, parameters)


if __name__ == "__main__":
    main()
