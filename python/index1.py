from tkinter import *
from tkinter import ttk
import tkinter.messagebox as tmsg
from datetime import datetime
import subprocess
import tkinter as tk
import os
import time

menu_category = ["perfume", "Eau De Perfume", "Baby Perfume", "Perfume oil"]
menu_category_dict = {
    "perfume": "2 perfume.txt",
    "Eau De Perfume": "4 Eau De Perfume.txt",
    "Baby perfumes": "5 Baby perfumes.txt",
    "Perfume oil": "6 Perfume oil.txt"
}

order_dict = {}
stock_dict = {}  # Dictionary to store the stock for each item

for category in menu_category:
    order_dict[category] = {}
    stock_dict[category] = {}  # Initialize stock for each category

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def load_menu():
    menuCategory.set("")
    menu_tabel.delete(*menu_tabel.get_children())
    menu_file_list = os.listdir("Menu")
    for file in menu_file_list:
        f = open("Menu\\" + file, "r")
        category = ""
        while True:
            line = f.readline()
            if(line == ""):
                menu_tabel.insert('', END, values=["", "", "", ""])
                break
            elif (line == "\n"):
                continue
            elif(line[0] == '#'):
                category = line[1:-1]
                name = "\t\t" + line[:-1]
                price = ""
                stock = 0  # Default stock for new items
            elif(line[0] == '*'):
                name = line[:-1]
                price = ""
                stock = 0  # Default stock for new items
            else:
                name = line[:line.rfind(" ")]
                price = line[line.rfind(" ") + 1:-3]
                stock = stock_dict.get(category, {}).get(name, 0)  # Get current stock from the dictionary
            
            menu_tabel.insert('', END, values=[name, price, category, stock])

def add_stock_button_operation():
    name = itemName.get()
    category = itemCategory.get()

    if category == "" or name == "":
        tmsg.showinfo("Error", "Please select an item")
        return

    if name not in stock_dict[category]:
        tmsg.showinfo("Error", "Item not found in the menu")
        return
    
    # Prompt user to enter the stock quantity to add
    stock_to_add = tmsg.askinteger("Add Stock", "Enter quantity to add:")
    if stock_to_add is None or stock_to_add <= 0:
        tmsg.showinfo("Error", "Please enter a valid quantity")
        return
    
    # Update the stock
    stock_dict[category][name] += stock_to_add

    # Save the updated stock into the menu file if necessary
    # (For now, we'll just update the in-memory stock_dict)
    
    load_menu()  # Reload menu to reflect the updated stock

def load_item_from_menu(event):
    cursor_row = menu_tabel.focus()
    contents = menu_tabel.item(cursor_row)
    row = contents["values"]

    itemName.set(row[0])
    itemRate.set(row[1])
    itemCategory.set(row[2])
    itemQuantity.set("1")

# Other existing functions (add_button_operation, remove_button_operation, etc.) remain unchanged

# Modify the menu table to include the stock column
root = Tk()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.title("Perfume Shop")

style_button = ttk.Style()
style_button.configure("TButton", font=("arial", 10, "bold"),
   background="lightgreen")

# Title frame and other frames remain the same

menu_frame = Frame(root, bd=8, bg="pink", relief=GROOVE)
menu_frame.place(x=0, y=125, height=530, width=650)

menu_label = Label(menu_frame, text="Menu", 
                    font=("times new roman", 20, "bold"), bg="pink", fg="White", pady=0)
menu_label.pack(side=TOP, fill="x")

menu_category_frame = Frame(menu_frame, bg="pink", pady=10)
menu_category_frame.pack(fill="x")

combo_lable = Label(menu_category_frame, text="Select Type", 
                    font=("arial", 12, "bold"), bg="pink", fg="white")
combo_lable.grid(row=0, column=0, padx=10)

menuCategory = StringVar()
combo_menu = ttk.Combobox(menu_category_frame, values=menu_category,
                            textvariable=menuCategory)
combo_menu.grid(row=0, column=1, padx=30)

show_button = ttk.Button(menu_category_frame, text="Show", width=7,
                        command=show_button_operation)
show_button.grid(row=0, column=2, padx=60)

show_all_button = ttk.Button(menu_category_frame, text="Show All",
                        width=10, command=load_menu)
show_all_button.grid(row=0, column=3)

# Modify the menu table to include a stock column
menu_tabel_frame = Frame(menu_frame)
menu_tabel_frame.pack(fill=BOTH, expand=1)

scrollbar_menu_x = Scrollbar(menu_tabel_frame, orient=HORIZONTAL)
scrollbar_menu_y = Scrollbar(menu_tabel_frame, orient=VERTICAL)

style = ttk.Style()
style.configure("Treeview.Heading", font=("arial", 13, "bold"))
style.configure("Treeview", font=("arial", 12), rowheight=25)

menu_tabel = ttk.Treeview(menu_tabel_frame, style="Treeview",
            columns=("name", "price", "category", "stock"), xscrollcommand=scrollbar_menu_x.set,
            yscrollcommand=scrollbar_menu_y.set)

menu_tabel.heading("name", text="Name")
menu_tabel.heading("price", text="Price")
menu_tabel.heading("category", text="Category")
menu_tabel.heading("stock", text="Stock")

menu_tabel["displaycolumns"] = ("name", "price", "category", "stock")
menu_tabel["show"] = "headings"
menu_tabel.column("price", width=40, anchor='center')

scrollbar_menu_x.pack(side=BOTTOM, fill=X)
scrollbar_menu_y.pack(side=RIGHT, fill=Y)

scrollbar_menu_x.configure(command=menu_tabel.xview)
scrollbar_menu_y.configure(command=menu_tabel.yview)

menu_tabel.pack(fill=BOTH, expand=1)

load_menu()
menu_tabel.bind("<ButtonRelease-1>", load_item_from_menu)

# Stock management (new button to add stock)
item_frame = Frame(root, bd=8, bg="pink", relief=GROOVE)
item_frame.place(x=650, y=120, height=200, width=650)

item_title_label = Label(item_frame, text="Item", 
                    font=("times new roman", 20, "bold"), bg="pink", fg="white")
item_title_label.pack(side=TOP, fill="x")

item_frame2 = Frame(item_frame, bg="pink")
item_frame2.pack(fill=X)

item_name_label = Label(item_frame2, text="Name", 
                    font=("arial", 12, "bold"), bg="pink", fg="white")
item_name_label.grid(row=0, column=0)

itemCategory = StringVar()
itemCategory.set("")

itemName = StringVar()
itemName.set("")
item_name = Entry(item_frame2, font="arial 12", textvariable=itemName, state=DISABLED, width=25)
item_name.grid(row=0, column=1, padx=10)

item_rate_label = Label(item_frame2, text="Price", 
                    font=("arial", 12, "bold"), bg="pink", fg="white")
item_rate_label.grid(row=0, column=2, padx=40)

itemRate = StringVar()
itemRate.set("")
item_rate = Entry(item_frame2, font="arial 12", textvariable=itemRate, state=DISABLED, width=40)
item_rate.grid(row=0, column=3, padx=10)

item_quantity_label = Label(item_frame2, text="Quantity", 
                    font=("arial", 12, "bold"), bg="pink", fg="white")
item_quantity_label.grid(row=1, column=0, padx=30, pady=15)

itemQuantity = StringVar()
itemQuantity.set("")
item_quantity = Entry(item_frame2, font="arial 12", textvariable=itemQuantity, width=10)
item_quantity.grid(row=1, column=1)

item_frame3 = Frame(item_frame, bg="pink")
item_frame3.pack(fill=X)

add_button = ttk.Button(item_frame3, text="Add Item", command=add_button_operation)
add_button.grid(row=0, column=1, padx=40, pady=30)

remove_button = ttk.Button(item_frame3, text="Remove Item", command=remove_button_operation)
remove_button.grid(row=0, column=2, padx=40, pady=30)

update_button = ttk.Button(item_frame3, text="Update Quantity", command=update_button_operation)
update_button.grid(row=0, column=3, padx=40, pady=30)

clear_button = ttk.Button(item_frame3, text="Clear", width=5, command=clear_button_operation)
clear_button.grid(row=0, column=4, padx=30, pady=30)

# Add the "Add Stock" button
add_stock_button = ttk.Button(item_frame3, text="Add Stock", command=add_stock_button_operation)
add_stock_button.grid(row=1, column=1, padx=40, pady=30)

root.mainloop()
