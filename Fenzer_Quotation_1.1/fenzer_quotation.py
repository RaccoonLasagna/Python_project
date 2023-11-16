from tkinter import *
from util.frames import *

class Quotation_Main(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)    
        self.geometry("%dx%d" % (1000, 700))

        # attempt to load config data from pickle file
        self.config = []
        self.reload_pickle()

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
    
    def reload_pickle(self):
        try:
            for file in os.listdir("config"):
                read_file = open(f"config\\{file}", "rb")
                self.config.append(pickle.load(read_file))
                read_file.close()
        except Exception as err:
            print(err)

testwin = Quotation_Main()
testwin.mainloop()