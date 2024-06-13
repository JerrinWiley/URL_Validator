import os
from PIL import ImageTk
from PIL import Image as Imag
import tkinter as tk
from tkinter import filedialog
from tkinter import *

import utils as U

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Function for opening the file explorer window
        def browseFiles(label_file_explorer):
            filename = filedialog.askopenfilename(initialdir = "/",
                                                title = "Select a File",
                                                filetypes = (("XLSX files",
                                                                "*.xlsx*"),
                                                                ("CSV files",
                                                                "*.CSV*"),
                                                            ("all files",
                                                                "*.*")))
            filename_brief = os.path.basename(filename)
            # Change label contents
            label_file_explorer.configure(text="File Selected: "+filename_brief)
            file_labels = (filename_brief, label_file_explorer)
            return(file_labels)

        ###  App settings
        self.title('Page Status Web Crawler')
        self.geometry("675x500")
        self.config(background = "white")
        self.resizable(True, True)
        
        ### Set Icon
        ico = Imag.open('JerrinLogo__256.jpg')
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

        # # Create a File Explorer label
        # label_file_explorer = tk.Label(self,
        #                                text = "Select file with URL list",
        #                                width = 100, height = 4,
        #                                fg = "blue") 
        
              
        # button_explore = tk.Button(self,
        #                            text = "Browse Files",
        #                            command = lambda:browseFiles(label_file_explorer)[1]) 
        # button_exit = tk.Button(self,
        #                         text = "Exit",
        #                         command = exit)
        # label_file_explorer.grid(column = 1, row = 1)
        # button_explore.grid(column = 1, row = 2)
        # button_exit.grid(column = 1,row = 3)

#------------------------------------------------------ HOME PAGE FRAME / CONTAINER -------------------------------------------------------

class HomePage(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)

        label = tk.Label(self, text="Instructions", font=('Times', '20'))
        label.pack(pady=0,padx=0)
        T = Text(self, height=15, width=50)
        textblock = """This program was created to take a list of URLs in XLSX or CSV format and individually ping each URL to determine the response code of the url and, if redirected, the final redirected URL and its respective response code."""

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

        ## processing menu
        processing_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Validation", menu=processing_menu)
        processing_menu.add_command(label="validate")
        processing_menu.add_separator()

        ## help menu
        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=U.about)
        help_menu.add_separator()

        return menubar

#------------------------------------------------------ VALIDATION PAGE FRAME / CONTAINER -------------------------------------------------------

class Validation(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)

        label = tk.Label(self, text="Validation Page", font=('Times', '20'))
        label.pack(pady=0,padx=0)
    
    def create_menubar(self, parent):
        menubar = Menu(parent, bd=3, relief=RAISED, activebackground="#80B9DC")

        ## Filemenu
        filemenu = Menu(menubar, tearoff=0, relief=RAISED, activebackground="#0226A9")
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="New Project", command=lambda: parent.show_frame(parent.Validation))
        filemenu.add_command(label="Close", command=lambda: parent.show_frame(parent.HomePage))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=parent.quit)

        ## processing menu
        processing_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Validation", menu=processing_menu)
        processing_menu.add_command(label="validate")
        processing_menu.add_separator()

        ## help menu
        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=U.about)
        help_menu.add_separator()

        return menubar        
      
if __name__ == "__main__":
    app = App()
    app.mainloop()