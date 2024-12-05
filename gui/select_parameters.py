from tkinter import ttk
import tkinter.filedialog as tk
from screeninfo import get_monitors
from tkinter import Label, W


class Window_Select_Parameters:
    def __init__(self):
        pass

    def define_size(self, window):
        width = 400
        height = 200

        info_pc = get_monitors()
        height_monitor = info_pc[0].width
        width_monitor = info_pc[0].height

        x = (width_monitor / 2) - (width / 2)
        y = (height_monitor / 2) - (height / 2)
        window.geometry("%dx%d+%d+%d" % (width, height, x, y))
        return window

    def define_name_and_icon(self, window):
        window.title("Image thresholding")
        return window

    def define_labels(self, window):
        label = Label(window, text="Select setings", font=("Helvetica 15 bold"))
        label.grid(row=0, column=1, sticky=W, pady=10)
        l1 = Label(window, text="Represention:")
        l2 = Label(window, text="Source:")
        l1.grid(row=1, column=0, sticky=W, pady=2)
        l2.grid(row=2, column=0, sticky=W, pady=2)

        return window

    def define_combo_boxes(self, window):
        valid_boxes_mode = ["RGB", "HSV"]
        valid_boxes_source = ["Picture", "WebCam"]

        option_select_mode = ttk.Combobox(window, values=valid_boxes_mode)
        option_select_mode.grid(row=1, column=1, sticky=W, pady=2)
        option_select_source = ttk.Combobox(window, values=valid_boxes_source)
        option_select_source.grid(row=2, column=1, sticky=W, pady=2)

        return window, option_select_mode, option_select_source

    def define_buttons(self, window):
        option_button = ttk.Button(window, text="Select the box", command=window.quit)
        option_button.grid(row=3, column=1, sticky=W, pady=10)

        return window

    def initialize(self):
        """
        The function `set_init_parameters` creates a Tkinter window with combo boxes for selecting image representation mode
        and source, and returns the selected values.
        :return: The `set_init_parameters` function returns the selected mode and source values from the Tkinter combo boxes
        after the user has made their selections.
        """

        # Creating buttons, setting size and title
        window = tk.Tk()

        window = self.define_name_and_icon(window)
        window = self.define_size(window)
        window = self.define_labels(window)
        window, option_select_mode, option_select_source = self.define_combo_boxes(
            window
        )
        window = self.define_buttons(window)

        window.mainloop()
        mode = option_select_mode.get()
        source = option_select_source.get()

        if mode != "" and source != "":
            window.destroy()
            return mode, source
