import os
from PIL import ImageTk
from PIL import Image as Imag
import tkinter as tk
from tkinter import filedialog
from tkinter import *
import requests
from datetime import datetime
import pandas as pd
from tqdm.notebook import tqdm

import utils as U

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        

        ###  App settings
        self.title('Page Status Web Crawler')
        self.geometry("675x500")
        self.config(background = "white")
        self.resizable(True, True)
        
        ### Set Icon
        ico = Imag.open('PageStatusChecker/JerrinLogo__256.png')
        photo = ImageTk.PhotoImage(ico)
        self.iconphoto(False,photo)
        
        ## Create Container
        container = tk.Frame(self,bg="#8aa7a9")
        container.pack(side = "top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        ## Initialize Frames
        self.frames = {}
        self.HomePage = HomePage
        self.Validation = Validation

        ## Defining Frames and Packing it
        for F in {HomePage, Validation}:
            frame = F(self, container)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)

    def show_frame(self, cont):
            frame = self.frames[cont]
            menubar = frame.create_menubar(self)
            self.configure(menu=menubar)
            frame.tkraise()


#------------------------------------------------------ HOME PAGE FRAME / CONTAINER -------------------------------------------------------

class HomePage(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)

        label = tk.Label(self, text="Instructions", font=('Tahoma', '20'))
        label.pack(pady=0,padx=0)
        T = Text(self, font="Tahoma", padx=10, pady=10, height=10, width=50, wrap="word")
        textblock = """This program was created to take a list of URLs in XLSX or CSV format and individually ping each URL to determine the response code of the url and, if redirected, the final redirected URL and its respective response code.\n\nTo begin, select "New Project" from the file menu.\n\nYour column headers must be in the top row. A blank first row will cause errors"""

        T.pack()
        T.insert(tk.END, textblock)

    
    def create_menubar(self, parent):
        menubar = Menu(parent, bd=3, relief=RAISED, activebackground="#80B9DC")

        ## Filemenu
        filemenu = Menu(menubar, tearoff=0, relief=RAISED, activebackground="#0226A9")
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="New Project", command=lambda: parent.show_frame(parent.Validation))
        filemenu.add_command(label="Close", command=lambda: parent.show_frame(parent.HomePage))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=parent.quit)

        # ## processing menu
        # processing_menu = Menu(menubar, tearoff=0)
        # menubar.add_cascade(label="Validation", menu=processing_menu)
        # processing_menu.add_command(label="validate")
        # processing_menu.add_separator()

        ## help menu
        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=U.about)
        help_menu.add_separator()

        return menubar

#------------------------------------------------------ VALIDATION PAGE FRAME / CONTAINER -------------------------------------------------------

class Validation(tk.Frame):
    
    def __init__(self, parent, container):
        filename = "Unknown"
        super().__init__(container)

        label = tk.Label(self, text="URL Validator", font=('Tahoma', '20'))
        label.pack(pady=0,padx=0)

        # Validator Function
        def validator(sheetDir, valButtonState):
            urls_raw = pd.read_excel(sheetDir)
            try:
                colNames = urls_raw.columns
                for col in colNames:
                    print(col)
                options = colNames
                clicked = tk.StringVar()
                clicked.set(colNames[0])

                drop = OptionMenu(self, clicked, *options)
                if valButtonState.get() == False:
                    drop.pack()
                    valButtonState.set(True)
                column_button = Button(self, text = "Check row count", command = show).pack

                def show():
                    label.config(text = clicked.get())
            except:
                print("Error")
            return

        # Function for opening the file explorer window
        def browseFiles(label_file_explorer, buttonCheckState, sheetFileDir, valButtonState):
            filename = filedialog.askopenfilename(initialdir = "/",
                                                title = "Select a File",
                                                filetypes = (("XLSX files",
                                                                "*.xlsx*"),
                                                                ("CSV files",
                                                                "*.CSV*"),
                                                            ("all files",
                                                                "*.*")))
            filename_brief = os.path.basename(filename)
            sheetFileDir.set(filename)

            # Change label contents
            label_file_explorer.configure(text="File Selected: "+filename_brief)
            file_labels = (filename_brief, label_file_explorer)

            # Change button states
            explore_button_text.set("Choose Different File")
            if buttonCheckState.get()==False:
                button_Check = tk.Button(self,
                            text = "Check File Contents",
                            command= lambda: validator(sheetFileDir.get(),valButtonState))
                button_Check.pack(pady=10)
                buttonCheckState.set(True)

            return
        
    # Create a File Explorer label
        label_file_explorer = tk.Label(self,
                                       text = "Select file with URL list",
                                       width = 100, height = 4,
                                       fg = "blue") 
        
        # Set variables
        sheetFileDir = tk.StringVar()
        explore_button_text = tk.StringVar()
        buttonCheckState = tk.BooleanVar()
        buttonCheckState.set(False)
        valButtonState = tk.BooleanVar()
        valButtonState.set(False)

        button_explore = tk.Button(self,
                                   textvariable = explore_button_text,
                                   command = lambda: browseFiles(label_file_explorer, buttonCheckState, sheetFileDir, valButtonState))
        explore_button_text.set("Browse Files")
        

        label_file_explorer.pack()
        button_explore.pack()


    def create_menubar(self, parent):
        menubar = Menu(parent, bd=3, relief=RAISED, activebackground="#80B9DC")

        ## Filemenu
        filemenu = Menu(menubar, tearoff=0, relief=RAISED, activebackground="#0226A9")
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="New Project", command=lambda: parent.show_frame(parent.Validation))
        filemenu.add_command(label="Close", command=lambda: parent.show_frame(parent.HomePage))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=parent.quit)

        # ## processing menu
        # processing_menu = Menu(menubar, tearoff=0)
        # menubar.add_cascade(label="Validation", menu=processing_menu)
        # processing_menu.add_command(label="validate")
        # processing_menu.add_separator()

        ## help menu
        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=U.about)
        help_menu.add_separator()

        return menubar        
      
if __name__ == "__main__":
    app = App()
    app.mainloop()