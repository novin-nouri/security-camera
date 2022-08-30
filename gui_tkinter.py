from tkinter import *
from tkinter import ttk
import cv2 as cv
from PIL import ImageTk, Image
from detect import Detect


class MainScreen:
    """Class to create GUI(graphical user interface) for our program"""

    def __init__(self, master):
        self.master = master
        self.master.title("Security Camera")
        self.master.geometry("870x641")
        self.master.resizable(False, False)
        self.master.config(bg="#22272D")
        self.address_display = False
        self.turn_on_camera = False
        """Initializes a MainScreen

        Arg:
            master: In order to create a tkinter application, we generally 
                create an instance of tkinter frame,It helps to display the 
                root window and manages all the other components of the 
                tkinter application.
        """