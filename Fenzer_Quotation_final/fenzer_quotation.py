from tkinter import *
from util.frames import *
from PIL import Image, ImageTk

class Quotation_Main(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)    
        self.geometry("%dx%d" % (1000, 700))
        self.title("Fenzer Quotation")
        if not os.path.exists("util\\fenzerpro.png"):
            import urllib.request
            image_url = 'https://fenzerpro.com/wp-content/uploads/2020/08/Fenzer-pro-Favicon.png'
            urllib.request.urlretrieve(image_url, "util\\fenzerpro.png") 
        icon = Image.open('util\\fenzerpro.png')
        photo = ImageTk.PhotoImage(icon)
        self.wm_iconphoto(False, photo)

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

        # make frames fill the screenar
        container.grid_columnconfigure(0, weight = 1)
        container.grid_rowconfigure(0, weight = 1)

        mainmenu.tkraise()

    def change_frame(self, frame):
        self.frame[frame].tkraise()
    
    def reload_pickle(self):
        # if it's not the initial pickle load
        if self.config != []:
            self.frame["qe"].combobox_category.current(0)
            self.frame["qe"].combobox_items.set('')
            self.frame["qe"].combobox_items['values'] = "รอการเลือกหมวดหมู่"
        self.config = []
        try:
            for file in os.listdir("config"):
                read_file = open(f"config\\{file}", "rb")
                self.config.append(pickle.load(read_file))
                read_file.close()
        except Exception as err:
            showerror("Error", "โหลดข้อมูลไม่สำเร็จ\nกรุณารีสตาร์ทโปรแกรม")
            print("From reload_pickle:", err)

Quotation_Main().mainloop()