import tkinter as tk
from tkinter import messagebox

class BillingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Billing System")
        self.root.geometry("500x500")
        
        # Title Label
        tk.Label(root, text="Billing System", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Entry Fields
        tk.Label(root, text="Item Name").pack()
        self.item_name = tk.Entry(root)
        self.item_name.pack()
        
        tk.Label(root, text="Quantity").pack()
        self.quantity = tk.Entry(root)
        self.quantity.pack()
        
        tk.Label(root, text="Price").pack()
        self.price = tk.Entry(root)
        self.price.pack()
        
        # Add Item Button
        tk.Button(root, text="Add Item", command=self.add_item).pack(pady=5)
        
        # Bill Area
        self.bill_area = tk.Text(root, height=10, width=40)
        self.bill_area.pack()
        
        # Total Bill Button
        tk.Button(root, text="Calculate Total", command=self.calculate_total).pack(pady=5)
        
        # Clear Bill Button
        tk.Button(root, text="Clear Bill", command=self.clear_bill).pack(pady=5)
        
        self.items = []
    
    def add_item(self):
        try:
            name = self.item_name.get()
            qty = int(self.quantity.get())
            price = float(self.price.get())
            total = qty * price
            self.items.append((name, qty, price, total))
            self.bill_area.insert(tk.END, f"{name}\t{qty}\t${price}\t${total}\n")
            self.item_name.delete(0, tk.END)
            self.quantity.delete(0, tk.END)
            self.price.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid quantity and price")
    
    def calculate_total(self):
        total_amount = sum(item[3] for item in self.items)
        self.bill_area.insert(tk.END, f"\nTotal Bill: ${total_amount}\n")
    
    def clear_bill(self):
        self.bill_area.delete("1.0", tk.END)
        self.items.clear()

# Run Application
root = tk.Tk()
app = BillingApp(root)
root.mainloop()
