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

    def __repr__(self):
        return f"{self.__class__.__name__!r}({self.__dict__!r})"

    def add_logo(self):
        """Add logo for app"""
        logo = PhotoImage(file=r"files\images\security_camera_icon.png")
        self.master.iconphoto(False, logo)

    @staticmethod
    def add_image():
        """Add image in main screen"""
        image = Image.open(r"files\images\security_camera_image.png")
        img = ImageTk.PhotoImage(image)
        lmain2 = Label(image=img, borderwidth=0, border=0)
        lmain2.image = img
        lmain2.place(x=264, y=20)
