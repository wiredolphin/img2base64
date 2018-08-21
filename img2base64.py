#!/usr/bin/env python3

import tkinter as tk
from tkinter import filedialog, scrolledtext
from tkinter import INSERT, END, W, E, N, S
import base64


class Button(tk.Button):
    def __init__(self, parent, *args, **kwargs):
        tk.Button.__init__(self, parent, *args, **kwargs)

class MainFrame(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.create_gui(parent)

    def create_gui(self, parent):
        self.grid()
        self.parent = parent
        self.data = ''

        self.file_name_label = tk.Label(parent, text="File choosen:")
        self.file_name_label.grid(column=0, row=0, columnspan=4,sticky=W)

        self.file_input_text = tk.Entry(parent,width=50)
        self.file_input_text.grid(column=0, row=1, columnspan=4)

        self.output_text = scrolledtext.ScrolledText(
            parent, 
            height=30,
            width=65,
            wrap='none')
        self.output_text.grid(column=0,row=2, columnspan=4)

        self.choose_file_button = Button(parent, text="open file", command=self.choose_file)
        self.choose_file_button.grid(column=0, row=3)

        self.add_to_clipboard_button = Button(parent, text="to clipboard", command=self.add_to_clipboard)
        self.add_to_clipboard_button.grid(column=1, row=3)

        self.reset_button = Button(parent, text="reset", command=self.reset)
        self.reset_button.grid(column=2, row=3)

        self.quit_button = Button(parent, text="quit", command=parent.destroy)
        self.quit_button.grid(column=3, row=3)

    def reset(self):
        self.output_text.delete('1.0', END)
        self.file_input_text.delete(0, END)

    def encode(self, file_name):
        encoded_string = ''
        try:
            with open(file_name, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
            image_file.close()
        except FileNotFoundError:
            print("Sorry, file not found!")
        return encoded_string

    def add_to_clipboard(self):
        # the following adds to the clipboard data containing new line chars
        # self.output = self.output_text.get(1.0, END)

        # better to add raw data to clipboard
        if self.data:
            #self.parent.withdraw()
            self.parent.clipboard_clear()
            self.parent.clipboard_append(self.data)
            # now it stays on the clipboard after the window is closed
            self.parent.update()

    def choose_file(self):
        file_name = filedialog.askopenfilename(
            #initialdir = "/",
            title = "Select file",
            filetypes = (("jpeg files","*.jpg"),
                        ("png files", "*.png"),
                        ("all files","*.*"))
        )
        
        if file_name:
            print(file_name)
            self.file_input_text.insert(0, file_name)
            
            self.data = self.encode(file_name).decode("utf-8")
            data_str = self.data

            # get output text scrolledText widget's current width
            width_opt = self.output_text.configure('width')
            width = int(width_opt[len(width_opt) - 1])

            # splits the whole string to multiple-lines, avoiding the bad 
            # one-line data management of the scrollableText widget
            data_str = '\n'.join([data_str[i:i + width] for i in range(0, len(data_str), width)])

            self.output_text.insert(INSERT, data_str)


def platform_specific_setup():
    try:
        from Cocoa import NSRunningApplication, NSApplicationActivateIgnoringOtherApps
        import os

        app = NSRunningApplication.runningApplicationWithProcessIdentifier_(os.getpid())
        app.activateWithOptions_(NSApplicationActivateIgnoringOtherApps)

    except ModuleNotFoundError:
        print("cocoa framework not found!")


def main():

    args = {}

    root = tk.Tk()
    root.title("Image to base64 encoder")
    MainFrame(root, args)

    platform_specific_setup()

    root.mainloop()


if __name__ == "__main__":
    main()

