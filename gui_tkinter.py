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

    def information_label(self):
        """Add user information label"""
        label_target_name = ttk.Label(self.master,
                                      text="Target object:",
                                      background="#22272D",
                                      foreground="White")
        label_target_name.place(x=10, y=20)
        label_phone_number = ttk.Label(self.master,
                                       text="Phone number:",
                                       background="#22272D",
                                       foreground="White")
        label_phone_number.place(x=10, y=100)
        label_api_key = ttk.Label(self.master,
                                  text="API key:",
                                  background="#22272D",
                                  foreground="White")
        label_api_key.place(x=10, y=180)
        label_cuda = ttk.Label(self.master,
                               text="Run with:",
                               background="#22272D",
                               foreground="White")
        label_cuda.place(x=10, y=260)
        label_camera = ttk.Label(self.master,
                                 text="Camera:",
                                 background="#22272D",
                                 foreground="White")
        label_camera.place(x=10, y=340)

    def inputs_user(self):
        """Add user information inputs"""
        self._object_optionmenu()
        self._information_entry()
        self._camera_optionmenu()
        self._cuda_optionmenu()

    def separator_line(self):
        """Add vertical line in main screen to separat between
        user information and video frame
        """
        separator = ttk.Separator(self.master, orient="vertical")
        separator.place(relx=0.218,
                        rely=0.02,
                        relwidth=0.001,
                        relheight=0.958)

    def _object_optionmenu(self):
        """Add option menu for (Target object) label
        and its options include: (dog, car, cat, bicycle, ...)
        """
        classes_names = self._read_file("target_object.names")
        self.object_variable = StringVar()
        # Set fifth of list for show on option menu
        self.object_variable.set(classes_names[5])
        self.object_optionmenu = OptionMenu(self.master,
                                            self.object_variable,
                                            *classes_names)
        self.object_optionmenu.config(bg="#464F5E",
                                      fg="White",
                                      width=15)
        self.object_optionmenu["menu"].config(bg="#464F5E",
                                              fg="White")
        self.object_optionmenu.place(x=11, y=50)

    def _information_entry(self):
        """Add entry box for (Phone number:) label and (Api key:) label"""
        self.entry_phone_number = ttk.Entry(self.master, width=20)
        self.entry_phone_number.place(x=11, y=130, height=30)
        self.entry_api_key = ttk.Entry(self.master, width=20)
        self.entry_api_key.place(x=11, y=210, height=30)

    def _cuda_optionmenu(self):
        """Add option menu for (Run with:) label
        and its options include: (CPU, GPU)
        """
        classes_names = ["CPU", "GPU"]
        self.cuda_variable = StringVar()
        self.cuda_variable.set(classes_names[0])
        self.cuda_optionmenu = OptionMenu(self.master,
                                          self.cuda_variable,
                                          *classes_names)
        self.cuda_optionmenu.config(bg="#464F5E",
                                    fg="White",
                                    width=15)
        self.cuda_optionmenu["menu"].config(bg="#464F5E", fg="White")
        self.cuda_optionmenu.place(x=11, y=290)

    def _camera_optionmenu(self):
        """Add option menu for (Camera) label
        and its options include: (first screen, Second screen, IP, Video))
        """
        classes_names = self._read_file("camera.names")
        self.camera_variable = StringVar()
        self.camera_variable.set(classes_names[0])
        self.camera_optionmenu = OptionMenu(self.master,
                                            self.camera_variable,
                                            *classes_names,
                                            command=self._camera_command)
        self.camera_optionmenu.config(bg="#464F5E",
                                      fg="White",
                                      width=15)
        self.camera_optionmenu["menu"].config(bg="#464F5E", fg="White")
        # Change color for (Video (for test))
        self.camera_optionmenu['menu'].entryconfig(3, foreground='Gray')
        self.camera_optionmenu.place(x=11, y=370)

    @staticmethod
    def _read_file(file_name):
        """Read .txt or .names file

        Args:
            file_name: name of .txt or .names file

        Returns:
            A list of words in each line of .txt or .names file
        """
        files_dir = f"files/yolov3_files/{file_name}"
        with open(files_dir, "r") as f:
            classes_names = f.read().rstrip("\n").split("\n")
        return classes_names

    def _camera_command(self, get_camera_type):
        """If you click on (IP) or (Video (for test)) in Camera option menu
        this function execute it
        """
        get_camera_type = self.camera_variable.get()
        # Add (Adress:) label and entry box for it
        if (get_camera_type == "IP") or (get_camera_type == "video (for test)"):
            self.label_address = ttk.Label(self.master,
                                           text="Address:",
                                           background="#22272D",
                                           foreground="White")
            self.label_address.place(x=10, y=420)

            self.entry_address = ttk.Entry(self.master, width=20)
            self.entry_address.place(x=11, y=450, height=30)
            self.address_display = True
        else:
            # if click on other (Camera:) option menu, remove (address)
            if self.address_display:
                self.entry_address.delete(0, END)
                self.entry_address.insert(0, "")
                self.label_address.place_forget()
                self.entry_address.place_forget()
                self.address_display = False

    def start_camera(self):
        """create (Start) button"""
        self._activate_widget("normal")
        start_button = ttk.Button(self.master,
                                  text="Start",
                                  width=20,
                                  command=self._stop_camera)
        start_button.place(x=11, y=590)

        if self.turn_on_camera:
            self.detector.capture.release()

    def _stop_camera(self):
        """create (Stop) button"""
        self._activate_widget("disabled")
        start_button = ttk.Button(self.master,
                                  text="Stop",
                                  width=20,
                                  command=self.start_camera)
        start_button.place(x=11, y=590)
        self.turn_on_camera = True
        self._create_frame()

    def _activate_widget(self, activate):
        """Disabled/enabled entry box and optinmenu

        Arg:
            activate:
                activate="disabled" => disabled entry box and option menu if
                    you click in Start button
                activate="normal" => enable entry box and option menu if
                    you click in Stop button
        """
        self.object_optionmenu.config(state=activate)
        self.entry_phone_number.config(state=activate)
        self.entry_api_key.config(state=activate)
        self.camera_optionmenu.config(state=activate)
        self.cuda_optionmenu.config(state=activate)
        if self.address_display:
            self.entry_address.config(state=activate)

    def _create_frame(self):
        """Create tkinter frame in right side of app
        this frame later use for camera
        """
        main_frame = ttk.Frame(self.master)
        main_frame.place(x=200, y=142)
        self.label = ttk.Label(self.master)
        self.label.place(x=200, y=142)
        self._send_information()

    def _send_information(self):
        """Get information user inputs and putting in Sms class, QrCode class
        and Detect class
        """
        get_list = self._get_information()
        url = f"https://console.melipayamak.com/api/send/simple/{str(get_list[2])}"
        information = {"phone_number": str(get_list[1]),
                       "api": url}
        self.detector = Detect(main_target="person",
                               target_object=str(get_list[0]),
                               camera=get_list[3],
                               sms_information=information,
                               cuda=get_list[4])
        self.net = self.detector.processing()
        # If (Video (for test)) Selected, we change the resolution of video
        # to 480 p
        if self.detector.camera == "video (for test)":
            self.detector.make_480p()
        self.show_frame()

    def _get_information(self):
        """Get all user inputs and putting in list

        Return:
            A list of all user inputs
        """
        get_target_object = self.object_variable.get()
        get_phone_number = self.entry_phone_number.get()
        get_api_key = self.entry_api_key.get()
        get_camera = self.camera_variable.get()
        get_run_processor = self.cuda_variable.get()
        if (get_camera == "IP") or (get_camera == "video (for test)"):
            video_folder = r"files\videos"
            get_camera_ = self.entry_address.get()
            get_camera = f"{video_folder}\{get_camera_}"
        elif get_camera == "first camera":
            get_camera = 0
        elif get_camera == "second camera":
            get_camera = 1
        get_list = [get_target_object,
                    get_phone_number,
                    get_api_key,
                    get_camera,
                    get_run_processor, ]
        return get_list

    def show_frame(self):
        """"Show video frame of opencv in tkinter"""
        frame = self.detector.show_frame(self.net)
        cv2image = cv.cvtColor(frame, cv.COLOR_BGR2RGBA)
        # change resolution to (640, 480)
        image = Image.fromarray(cv2image).resize((640, 480))
        imgtk = ImageTk.PhotoImage(image=image)
        self.label.imgtk = imgtk
        self.label.configure(image=imgtk)
        self.label.after(1, self.show_frame)
