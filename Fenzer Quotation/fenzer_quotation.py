from tkinter import *
from util.frames import *

class Quotation_Main(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)    
        self.geometry("%dx%d" % (1000, 700))

        # load config data
        

        # store all frames in a dict
        self.frame =  {}    
        mainmenu = MainMenu(container, self)
        self.frame["mm"] = mainmenu
        quotation_edit = Quotation_Edit(container, self)
        self.frame["qe"] = quotation_edit
        config = Config(container, self)
        self.frame["c"] = config
        
        # pack
        mainmenu.grid(row = 0, column = 0, sticky=NSEW)
        quotation_edit.grid(row = 0, column = 0, sticky=NSEW)
        config.grid(row = 0, column = 0, sticky=NSEW)

        # make frames fill the screen
        container.grid_columnconfigure(0, weight = 1)
        container.grid_rowconfigure(0, weight = 1)

        mainmenu.tkraise()

    def change_frame(self, frame):
        self.frame[frame].tkraise()

testwin = Quotation_Main()
testwin.mainloop()