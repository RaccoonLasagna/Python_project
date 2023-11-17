from tkinter import *
try:
    from util.excelwriter import generate_xlsx
except:
    from excelwriter import generate_xlsx
import pickle
import os
# for combobox
from tkinter import ttk
# for popup entry field
from tkinter import simpledialog
# for showing error
from tkinter.messagebox import showerror
# for selecting files
from tkinter.filedialog import askopenfilename
import pandas
import openpyxl

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
        load_file_path = askopenfilename()
        try:
            df = pandas.read_excel(load_file_path, usecols='B:D')
        except:
            return
        # get the address, which is everything from row 3 to 'รายการสินค้า'
        address = ""
        current_row = 3
        while df['Unnamed: 1'].iloc[current_row] != "รายการสินค้า":
            # NaN's type is float, and items are always strings, so use floats to filter out NaN
            if type(df['Unnamed: 1'].iloc[current_row]) != float:
                address = f"{address}{df['Unnamed: 1'].iloc[current_row]}\n"
            current_row += 1
        current_row += 1
        # read until it hits ***ขนส่งด้วย 10ล้อ เท่านั้น*** which will signal the end of the item list
        items = []
        while df['Unnamed: 1'].iloc[current_row] != '***ขนส่งด้วย 10ล้อ เท่านั้น***':
            if type(df['Unnamed: 1'].iloc[current_row]) != float:
                # format and append
                items.append(f"{df['Unnamed: 1'].iloc[current_row]}, ฿{df['Unnamed: 2'].iloc[current_row]} ({df['Unnamed: 3'].iloc[current_row]})")
            current_row += 1
        # clear and write the collected data
        address_box = self.controller.frame["qe"].address_entry
        address_box.delete("1.0", END)
        address_box.insert(END, address)
        list_box = self.controller.frame["qe"].added_items
        list_box.delete(0, END)
        for item in items:
            self.controller.frame["qe"].added_items.insert(END, item)
        self.controller.change_frame("qe")

class Quotation_Edit(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label_size = 14

        # entry for address
        self.address_entry = Text(self, width=0, height=0, font = ("TH SarabunPSK", label_size))

        # dropdown for category and item selection
        self.category = StringVar()
        self.category_values = ["เลือกหมวดหมู่", "เสารั้ว", "ฟุตติ้ง", "แผ่นกันดิน", "บัวหัวเสา", "แผ่นรั้ว", "ทับหลัง", "เสาเข็ม", "ค่าแรง", "อื่นๆ"]
        self.combobox_category = ttk.Combobox(self,values=self.category_values ,state="readonly", textvariable=self.category, font = ("TH SarabunPSK", label_size))
        self.combobox_category.current(0)
        self.combobox_category.bind("<<ComboboxSelected>>", self.load_items)

        self.item = StringVar()
        self.combobox_items = ttk.Combobox(self,values=["รอการเลือกหมวดหมู่"], textvariable=self.item, state='readonly', font = ("TH SarabunPSK", label_size))

        # listbox to store added item
        self.added_items = Listbox(self, font = ("TH SarabunPSK", label_size))

        # buttons
        add_button = Button(self, text="เพื่ม", command=self.add_item, bg = "light yellow", font = ("TH SarabunPSK", label_size))
        delete_button = Button(self, text="ลบ", command = self.delete_item, bg = "pink", font = ("TH SarabunPSK", label_size))
        create_button = Button(self, text="เขียนใบเสนอราคา", command=self.create_quotation, bg="light green", font = ("TH SarabunPSK", label_size))
        back_button = Button(self, text="ย้อนกลับ", command=lambda: controller.change_frame("mm"), font = ("TH SarabunPSK", label_size))
        
        # grid
        Label(self, text="ที่อยู่ลูกค้า", font = ("TH SarabunPSK", label_size)).grid(row=0, column=0, sticky=NSEW, columnspan=2)
        self.address_entry.grid(row=1, column=0, sticky=NSEW, columnspan=2)
        Label(self, text="เลือกรายการ", font = ("TH SarabunPSK", label_size)).grid(row=2, column=0, sticky=NSEW, columnspan=2)
        self.combobox_category.grid(row=3, column=0, sticky=NSEW, columnspan=2)
        self.combobox_items.grid(row=4, column=0, sticky=NSEW, columnspan=2)
        add_button.grid(row=5, column=0, sticky=NSEW)
        delete_button.grid(row=5, column=1, sticky=NSEW)
        self.added_items.grid(row=6, column=0, sticky=NSEW, columnspan=2)
        create_button.grid(row=7, column=0, sticky=NSEW, columnspan=2)
        back_button.grid(row=8, column=0, sticky=NSEW, columnspan=2)

        # ===== arrangement =====
        self.grid_columnconfigure([0,1], weight=1)
        self.grid_rowconfigure(1, weight=5)
        self.grid_rowconfigure(6, weight=10)
        self.grid_rowconfigure([0,2,3,4,5,7,8], weight=1)
    
    def load_items(self, _event):
        # index 1-8 = load file from config
        index = self.category_values.index(self.category.get())
        if index == 0:
            self.combobox_items['state'] = 'readonly'
            self.combobox_items['values'] = "รอการเลือกหมวดหมู่"
        elif  1 <= index and index <= 8:
            self.combobox_items['state'] = 'readonly'
            self.combobox_items['values'] = self.controller.config[index-1]
        elif index == 0:
            self.combobox_items['state'] = 'readonly'
        elif index == 9:
            self.combobox_items['state'] = 'normal'
            self.combobox_items['values'] = "พิมพ์สิ่งที่ต้องการเพิ่ม"
            self.combobox_items.current(0)
        else:
            print("Something went wrong...")

    def add_item(self):
        item = self.item.get()
        added_items_content = [i.split(" (")[0].strip() for i in self.added_items.get(0, END)]
        if item in added_items_content:
            return
        if item == "รอการเลือกหมวดหมู่" or item == "พิมพ์สิ่งที่ต้องการเพิ่ม" or item.strip() == "":
            return
        elif self.category.get() == "อื่นๆ":
            price = simpledialog.askfloat(title="ราคา", prompt="ใส่ราคาของรายการ")
            amount = simpledialog.askinteger(title="จำนวน", prompt="ใส่จำนวนของรายการ")
            insert_string = f"{item}, ฿{price} ({amount})"
            self.added_items.insert(END, insert_string)
        else:
            amount = simpledialog.askinteger(title="จำนวน", prompt="ใส่จำนวนของรายการ")
            insert_string = f"{item} ({amount})"
            self.added_items.insert(END, insert_string)

    def delete_item(self):
        selected_item = self.added_items.curselection()
        if selected_item:
            self.added_items.delete(selected_item[0])

    def create_quotation(self):
        generate_xlsx(self.address_entry.get("1.0", END), self.added_items.get(0, END))

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
        name_entry_key = ('fencepost_name', 'footing_name', 'retainwall_name', 'frieze_name', 'fencepanel_name', 'lintel_name', 'pile_name', 'labor_name')
        price_entry_key = ('fencepost_price', 'footing_price', 'retainwall_price', 'frieze_price', 'fencepanel_price', 'lintel_price', 'pile_price', 'labor_price')
        name_entry = {}
        price_entry = {}
        for namekey in name_entry_key:
            name_entry[namekey] = Entry(self, width=1)
        for pricekey in price_entry_key:
            price_entry[pricekey] = Entry(self, width=1)

        # list box
        self.list_box_key = ('fencepost_list', 'footing_list', 'retainwall_list', 'frieze_list', 'fencepanel_list', 'lintel_list', 'pile_list', 'labor_list')
        self.list_box = {}
        for listkey in self.list_box_key:
            self.list_box[listkey] = Listbox(self, selectmode=SINGLE)

        # load list box items from pickle
        try:
            load_index = 0
            for config in controller.config:
                for item in config:
                    self.list_box[self.list_box_key[load_index]].insert(END, item)
                load_index += 1
        except Exception as err:
            print("From loading list box:", err)

        # add button
        add_button_key = ('fencepost_add', 'footing_add', 'retainwall_add', 'frieze_add', 'fencepanel_add', 'lintel_add', 'pile_add', 'labor_add')
        add_button = {}
        counter = 0
        for addkey in add_button_key:
            current_name = name_entry[name_entry_key[counter]]
            current_price = price_entry[price_entry_key[counter]]
            current_list = self.list_box[self.list_box_key[counter]]
            add_button[addkey] = Button(self, text="เพิ่ม", bg='light green', command=lambda name = current_name, price = current_price, list = current_list: self.list_add(name, price, list))
            counter += 1

        # delete button
        delete_button_key = ('fencepost_del', 'footing_del', 'retainwall_del', 'frieze_del', 'fencepanel_del', 'lintel_del', 'pile_del', 'labor_del')
        delete_button = {}
        counter = 0
        for delkey in delete_button_key:
            listkey = self.list_box[self.list_box_key[counter]]
            delete_button[delkey] = Button(self, text="ลบ", bg='pink', command=lambda list = listkey: self.list_del(list))
            counter += 1

        # return button
        return_button = Button(self, text="บันทึกและย้อนกลับ", command=lambda: [self.save(), controller.reload_pickle(), controller.change_frame("mm")], font = ("TH SarabunPSK", label_size))

        # ===== grid =====
        # name entry
        counter = 0
        for y in (1, 6):
            for x in (0, 2, 4, 6):
                name_entry[name_entry_key[counter]].grid(row=y, column=x, sticky=NSEW)
                counter += 1
        
        # price entry
        counter = 0
        for y in (1, 6):
            for x in (1, 3, 5, 7):
                price_entry[price_entry_key[counter]].grid(row=y, column=x, sticky=NSEW)
                counter += 1

        # add button
        counter = 0
        for y in (2, 7):
            for x in (0, 2, 4, 6):
                add_button[add_button_key[counter]].grid(row=y, column=x, columnspan=2, sticky=NSEW)
                counter += 1
        
        # del button
        counter = 0
        for y in (4, 9):
            for x in (0, 2, 4, 6):
                delete_button[delete_button_key[counter]].grid(row=y, column=x, columnspan=2, sticky=NSEW)
                counter += 1
        
        # listbox
        counter = 0
        for y in (3, 8):
            for x in (0, 2, 4, 6):
                self.list_box[self.list_box_key[counter]].grid(row=y, column=x, columnspan=2, sticky=NSEW)
                counter += 1

        return_button.grid(row=10,column=2, columnspan=4, sticky=NSEW)

        # ===== arrangement =====
        # alternating column weight
        self.grid_columnconfigure([0,2,4,6], weight=4)
        self.grid_columnconfigure([1,3,5,7], weight=1)
        
        # bigger row 3 and 8 for the entry box
        self.grid_rowconfigure([0,1,2,4,5,6,7,9,10], weight=1)
        self.grid_rowconfigure([3,8], weight=10)

    def list_add(self, entry_name, entry_price, checklist):
        print(entry_name, entry_price, checklist)
        item = entry_name.get()
        price = entry_price.get()
        if not price:
            return
        try:
            float(price)
        except:
            showerror("Error", "ราคาต้องเป็นตัวเลขเท่านั้น")
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
        # listbox_values = self.list_box.get(0, END), self.footing_list.get(0, END), self.retainwall_list.get(0, END), self.frieze_list.get(0, END), self.fencepanel_list.get(0, END), self.lintel_list.get(0, END), self.pile_list.get(0, END), self.labor_list.get(0, END)
        listbox_values = [self.list_box[self.list_box_key[i]].get(0, END) for i in range(8)]
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

    def check(self):
        print("ok")