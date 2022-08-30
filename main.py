from tkinter import Tk
from gui_tkinter import MainScreen


def main():
    root = Tk()

    main_screen = MainScreen(root)
    main_screen.add_logo()
    main_screen.add_image()
    main_screen.information_label()
    main_screen.inputs_user()
    main_screen.separator_line()
    main_screen.start_camera()

    root.mainloop()


if __name__ == "__main__":
    main()
