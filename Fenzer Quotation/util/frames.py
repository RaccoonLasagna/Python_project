from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
import pickle
import os

class MainMenu(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        # new quotation
        new_q_button = Button(self, text="ใบเสนอราคาใหม่", command=lambda: controller.change_frame("qe"), font = ("TH SarabunPSK", 30), bg = 'light green')
        # load quotation
        load_q_button = Button(self, text="เปิดใบเสนอราคา", command=self.load_quotation, font = ("TH SarabunPSK", 30), bg = 'light blue')
        # config button
        config_button = Button(self, text="เพิ่มสินค้า/\nเปลี่ยนราคาสินค้า", command=lambda: controller.change_frame("c"), font = ("TH SarabunPSK", 30), bg = 'light gray')
        
        # grid
        load_q_button.grid(row=0, column=0, sticky="nsew")
        new_q_button.grid(row=0, column=1, sticky="nsew")
        config_button.grid(row=0, column=2, sticky="nsew")

        # arrangement
        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 1)
        self.grid_columnconfigure(2, weight = 1)

    def load_quotation(self):
        loaded_file = askopenfile()
        self.controller.change_frame("qe")

class Quotation_Edit(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        # fence post dropdown
        # fenceposts = ["I18 m * 18 m * 3.45 m", "I18 m * 18 m * 3.70 m", "I15 m * 15 m * 2.28 m", "I15 m * 15 m * 2.78 m", "I15 m * 15 m * 3.28 m", "With plating I15- I18"]
        # self.fenceposts_var = StringVar()
        # self.fenceposts_var.set("Fence Post Type")
        # self.fencepost_drop = OptionMenu(self.frame2, self.fenceposts_var, *fenceposts)

        # back button
        button = Button(self, text="ย้อนกลับ", command=lambda: controller.change_frame("mm"))
        
        # grid
        button.grid(row = 1, column = 3)

class Config(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        # labels
        label_size = 14
        label_index = 0
        labels = ("เสารั้ว", "ฟุตติ้ง", "แผ่นกันดิน", "บัวหัวเสา", "แผ่นรั้ว", "ทับหลัง", "เสาเข็ม", "ค่าแรง")
        for y in (0,5):
            for x in (0,2,4,6):
                Label(self, text=labels[label_index], font = ("TH SarabunPSK", label_size), bg="light gray").grid(row=y, column=x, columnspan=2, sticky=NSEW)
                label_index += 1

        # item & price entering field
        fencepost_name = Entry(self)
        fencepost_price = Entry(self)
        footing_name = Entry(self)
        footing_price = Entry(self)
        retainwall_name = Entry(self)
        retainwall_price = Entry(self)
        frieze_name = Entry(self)
        frieze_price = Entry(self)
        fencepanel_name = Entry(self)
        fencepanel_price = Entry(self)
        lintel_name = Entry(self)
        lintel_price = Entry(self)
        pile_name = Entry(self)
        pile_price = Entry(self)
        labor_name = Entry(self)
        labor_price = Entry(self)
        name_entry = (fencepost_name, footing_name, retainwall_name, frieze_name, fencepanel_name, lintel_name, pile_name, labor_name)
        price_entry = (fencepost_price, footing_price, retainwall_price, frieze_price, fencepanel_price, lintel_price, pile_price, labor_price)

        # add button
        fencepost_add = Button(self, text="เพิ่ม", bg='light green', command=lambda: self.list_add(fencepost_name, fencepost_price, self.fencepost_list))
        footing_add = Button(self, text="เพิ่ม", bg='light green', command=lambda: self.list_add(footing_name, footing_price, self.footing_list))
        retainwall_add = Button(self, text="เพิ่ม", bg='light green', command=lambda: self.list_add(retainwall_name, retainwall_price, self.retainwall_list))
        frieze_add = Button(self, text="เพิ่ม", bg='light green', command=lambda: self.list_add(frieze_name, frieze_price, self.frieze_list))
        fencepanel_add = Button(self, text="เพิ่ม", bg='light green', command=lambda: self.list_add(fencepanel_name, fencepanel_price, self.fencepanel_list))
        lintel_add = Button(self, text="เพิ่ม", bg='light green', command=lambda: self.list_add(lintel_name, lintel_price, self.lintel_list))
        pile_add = Button(self, text="เพิ่ม", bg='light green', command=lambda: self.list_add(pile_name, pile_price, self.pile_list))
        labor_add = Button(self, text="เพิ่ม", bg='light green', command=lambda: self.list_add(labor_name, labor_price, self.labor_list))
        add_button = (fencepost_add, footing_add, retainwall_add, frieze_add, fencepanel_add, lintel_add, pile_add, labor_add)

        # list box
        self.fencepost_list = Listbox(self, selectmode=SINGLE)
        self.footing_list = Listbox(self, selectmode=SINGLE)
        self.retainwall_list = Listbox(self, selectmode=SINGLE)
        self.frieze_list = Listbox(self, selectmode=SINGLE)
        self.fencepanel_list = Listbox(self, selectmode=SINGLE)
        self.lintel_list = Listbox(self, selectmode=SINGLE)
        self.pile_list = Listbox(self, selectmode=SINGLE)
        self.labor_list = Listbox(self, selectmode=SINGLE)
        list_box = (self.fencepost_list, self.footing_list, self.retainwall_list, self.frieze_list, self.fencepanel_list, self.lintel_list, self.pile_list, self.labor_list)

        # load listbox items
        try:
            load_index = 0
            for file in os.listdir("config"):
                read_file = open(f"config\\{file}", "rb")
                loaded_items = pickle.load(read_file)
                for item in sorted(loaded_items):
                    list_box[load_index].insert(END, item)
                read_file.close()
                load_index += 1
        except Exception as err:
            print(err)

        # delete button
        fencepost_del = Button(self, text="ลบ", bg='pink', command=lambda: self.list_del(self.fencepost_list))
        footing_del = Button(self, text="ลบ", bg='pink', command=lambda: self.list_del(self.footing_list))
        retainwall_del = Button(self, text="ลบ", bg='pink', command=lambda: self.list_del(self.retainwall_list))
        frieze_del = Button(self, text="ลบ", bg='pink', command=lambda: self.list_del(self.frieze_list))
        fencepanel_del = Button(self, text="ลบ", bg='pink', command=lambda: self.list_del(self.fencepanel_list))
        lintel_del = Button(self, text="ลบ", bg='pink', command=lambda: self.list_del(self.lintel_list))
        pile_del = Button(self, text="ลบ", bg='pink', command=lambda: self.list_del(self.pile_list))
        labor_del = Button(self, text="ลบ", bg='pink', command=lambda: self.list_del(self.labor_list))
        del_button = (fencepost_del, footing_del, retainwall_del, frieze_del, fencepanel_del, lintel_del, pile_del, labor_del)

        # button
        return_button = Button(self, text="บันทึกและย้อนกลับ", command=lambda: [self.save(), controller.change_frame("mm")], font = ("TH SarabunPSK", label_size))

        # ===== grid =====
        # name entry
        name_index = 0
        for y in (1, 6):
            for x in (0, 2, 4, 6):
                name_entry[name_index].grid(row=y, column=x, sticky=NSEW)
                name_index += 1
        
        # price entry
        price_index = 0
        for y in (1, 6):
            for x in (1, 3, 5, 7):
                price_entry[price_index].grid(row=y, column=x, sticky=NSEW)
                price_index += 1

        # add button
        add_index = 0
        for y in (2, 7):
            for x in (0, 2, 4, 6):
                add_button[add_index].grid(row=y, column=x, columnspan=2, sticky=NSEW)
                add_index += 1
        
        # del button
        del_index = 0
        for y in (4, 9):
            for x in (0, 2, 4, 6):
                del_button[del_index].grid(row=y, column=x, columnspan=2, sticky=NSEW)
                del_index += 1
        
        # listbox
        list_index = 0
        for y in (3, 8):
            for x in (0, 2, 4, 6):
                list_box[list_index].grid(row=y, column=x, columnspan=2, sticky=NSEW)
                list_index += 1

        return_button.grid(row=10,column=2, columnspan=4, sticky=NSEW)

        # ===== arrangement =====
        # alternating column weight
        for column in range(8):
            if column % 2 == 0:
                self.grid_columnconfigure(0, weight=4)
            else:
                self.grid_columnconfigure(0, weight=1)
        
        # bigger row 3 and 8 for the entry box
        for row in range(11):
            if row != 3 and row != 8:
                self.grid_rowconfigure(row, weight=1)
            else:
                self.grid_rowconfigure(row, weight=10)

    def list_add(self, entry_name, entry_price, checklist):
        item = entry_name.get()
        price = entry_price.get()
        if not price:
            return
        try:
            float(price)
        except:
            showinfo("Error", "ราคาต้องเป็นตัวเลขเท่านั้น")
            return
        checklist_item_p = checklist.get(0, END)
        checklist_item = [i.split(", ")[0] for i in checklist_item_p]
        # if item is already in the checklist, delete the previous one
        if item in checklist_item and price:
            index = 0
            for i in checklist_item:
                if i != item:
                    index +=1
                else:
                    checklist.delete(index)
        # if there's an entry in item and price:
        if item and price:
            added_item = f"{item.strip()}, ฿{round(float(price), 2)}"
            checklist.insert(END, added_item)
            entry_name.delete(0, END)
            entry_price.delete(0, END)
    
    def list_del(self, checklist):
        selected_item = checklist.curselection()
        if selected_item:
            checklist.delete(selected_item[0])

    def save(self):
        listbox_values = self.fencepost_list.get(0, END), self.footing_list.get(0, END), self.retainwall_list.get(0, END), self.frieze_list.get(0, END), self.fencepanel_list.get(0, END), self.lintel_list.get(0, END), self.pile_list.get(0, END), self.labor_list.get(0, END)
        filenames = ("_1_fpst_config", "_2_ft_config", "_3_rw_config", "_4_fz_config", "_5_fpnl_config", "_6_lt_config", "_7_p_config", "_8_l_config")
        index = 0
        # if the folder config doesn't exist, create one
        if not os.path.exists("config") and not os.path.isdir("config"):
            os.mkdir("config")
        # pickle and put listbox values into config folder
        for value in listbox_values:
            filename = f"config\\{filenames[index]}.pickle"
            file = open(filename, "wb")
            pickle.dump(value, file)
            file.close()
            index += 1

if __name__ == "__main__":
    test = Tk()
    config = Config(test, test)
    config.pack()
    test.mainloop()