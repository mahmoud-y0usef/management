import tkinter as tk
from tkinter import ttk
import sqlite3
from menu import CreateMenu
root = tk.Tk()

current_frame = None
conn = sqlite3.connect('data.db')
c = conn.cursor()

## select tables
def GetStorage():
    c.execute('SELECT * FROM storage')
    return c.fetchall()

def GetStorageType():
    c.execute('SELECT * FROM type')
    return c.fetchall()

## insert tables
def AddStorage(count, type, price, date):
    c.execute('INSERT INTO storage (count, type, price, date) VALUES (?, ?, ?, ?)', (count, type, price, date))
    conn.commit()

def AddType(name):
    c.execute('INSERT INTO type (name) VALUES (?)', (name,))
    conn.commit()


## delete tables
def DeleteStorage(id):
    c.execute('DELETE FROM storage WHERE id = ?', (id,))
    conn.commit()

def DeleteType(id):
    c.execute('DELETE FROM type WHERE id = ?', (id,))
    conn.commit()

## update tables
def UpdateStorage(count, type, price, date, id):
    c.execute('UPDATE storage SET count = ?, type = ?, price = ?, date = ? WHERE id = ?', (count, type, price, date, id))
    conn.commit()

def UpdateType(name, id):
    c.execute('UPDATE type SET name = ? WHERE id = ?', (name, id))
    conn.commit()

def NavBar(title):
    global root
    menu = CreateMenu(root)
    menu.add_menu('المخزن', [('جديد', AddNewStorage), ('عرض', Main)])
    menu.add_menu('رصيد السيارة', [('جديد', AddNewWalletCar), ('عرض', ShowWalletCar)])
    menu.add_menu('المرتجعات', [('جديد', AddNewReturn), ('عرض', ShowReturn)])
    menu.add_menu('المديونية', [('جديد', AddNewIndebtedness), ('عرض', ShowIndebtedness)])
    menu.add_menu('خروج', [('خروج', root.quit)])
    menu.add_title(title)
    menu.geometry('800x600+300+100')


def ShowIndebtedness():
    NavBar('عرض المديونية')

def AddNewIndebtedness():
    NavBar('إضافة مديونية جديد')

def AddNewReturn():
    NavBar('إضافة مرتجع جديد')

def ShowReturn():
    NavBar('عرض المرتجعات')

def AddNewWalletCar():
    NavBar('إضافة رصيد سيارة جديد')

def ShowWalletCar():
    NavBar('عرض رصيد السيارة')

def clear_frame():
    global current_frame
    if current_frame:
        current_frame.destroy()

def Main():
    NavBar('المخزن')
    clear_frame()
    
    global current_frame
    current_frame = ttk.Frame(root)
    current_frame.grid(row=1, column=0, columnspan=8, padx=20, pady=20)

    # Define column headers with equal spacing
    headers = ["المعرف", "الكمية", "النوع", "السعر", "التاريخ", "تعديل", "حذف"]
    for idx, header in enumerate(headers):
        ttk.Label(current_frame, text=header, font=('Arial', 12, 'bold'), padding=10).grid(row=0, column=idx)

    # Fetch and display the storage data
    storage = GetStorage()
    for index, item in enumerate(storage):
        # Display each column in a separate grid cell
        for col, value in enumerate(item):
            ttk.Label(current_frame, text=value, padding=10).grid(row=index+1, column=col)
        
        # Add Edit button
        edit_btn = ttk.Button(current_frame, text="تعديل", command=lambda id=item[0]: edit_item(id))
        edit_btn.grid(row=index+1, column=len(item), padx=5, pady=5)

        # Add Delete button
        del_btn = ttk.Button(current_frame, text="حذف", command=lambda id=item[0]: delete_item(id))
        del_btn.grid(row=index+1, column=len(item) + 1, padx=5, pady=5)

    # Add a button for adding new item
    add_btn = ttk.Button(current_frame, text="إضافة إلى المخزن", command=AddNewStorage)
    add_btn.grid(row=len(storage) + 2, column=0, columnspan=2, pady=10)

def AddNewStorage():
    NavBar('إضافة مخزن جديد')
    clear_frame()

    global current_frame
    current_frame = ttk.Frame(root)
    current_frame.grid(row=1, column=0, columnspan=8, padx=20, pady=20)

    # Create form labels and entries
    ttk.Label(current_frame, text="الكمية").grid(row=0, column=0, padx=5, pady=5)
    count_entry = ttk.Entry(current_frame)
    count_entry.grid(row=0, column=1, padx=5, pady=5)
    
    ttk.Label(current_frame, text="النوع").grid(row=1, column=0, padx=5, pady=5)
    type_entry = ttk.Combobox(current_frame)
    type_entry['values'] = [item[1] for item in GetStorageType()]
    type_entry.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(current_frame, text="السعر").grid(row=2, column=0, padx=5, pady=5)
    price_entry = ttk.Entry(current_frame)
    price_entry.grid(row=2, column=1, padx=5, pady=5)
    
    ttk.Label(current_frame, text="التاريخ").grid(row=3, column=0, padx=5, pady=5)
    date_entry = ttk.Entry(current_frame)
    date_entry.grid(row=3, column=1, padx=5, pady=5)

    # Create a button to submit the form
    submit_btn = ttk.Button(current_frame, text="إضافة", command=lambda: AddStorage(count_entry.get(), type_entry.get(), price_entry.get(), date_entry.get()))
    submit_btn.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

def show_types():
    NavBar('إدارة الأنواع')
    clear_frame()

    global current_frame
    current_frame = ttk.Frame(root)
    current_frame.grid(row=1, column=0, columnspan=8, padx=20, pady=20)

    # Define column headers with equal spacing
    headers = ["المعرف", "النوع", "تعديل", "حذف"]
    for idx, header in enumerate(headers):
        ttk.Label(current_frame, text=header, font=('Arial', 12, 'bold'), padding=10).grid(row=0, column=idx)

    # Fetch and display the storage types
    types = GetStorageType()
    for index, item in enumerate(types):
        for col, value in enumerate(item):
            ttk.Label(current_frame, text=value, padding=10).grid(row=index+1, column=col)
        
        # Add Edit button
        edit_btn = ttk.Button(current_frame, text="تعديل", command=lambda id=item[0]: edit_type(id))
        edit_btn.grid(row=index+1, column=len(item), padx=5, pady=5)

        # Add Delete button
        del_btn = ttk.Button(current_frame, text="حذف", command=lambda id=item[0]: delete_type(id))
        del_btn.grid(row=index+1, column=len(item) + 1, padx=5, pady=5)

    # Add a button for adding new type
    add_btn = ttk.Button(current_frame, text="إضافة نوع", command=AddNewType)
    add_btn.grid(row=len(types) + 2, column=0, columnspan=2, pady=10)

def AddNewType():
    NavBar('إضافة نوع جديد')
    clear_frame()

    global current_frame
    current_frame = ttk.Frame(root)
    current_frame.grid(row=1, column=0, columnspan=8, padx=20, pady=20)

    # Create form labels and entries
    ttk.Label(current_frame, text="النوع").grid(row=0, column=0, padx=5, pady=5)
    name_entry = ttk.Entry(current_frame)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    # Create a button to submit the form
    submit_btn = ttk.Button(current_frame, text="إضافة", command=lambda: AddType(name_entry.get()))
    submit_btn.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
    
    

def edit_item(item_id):
    NavBar('تعديل بيانات المخزن')
    clear_frame()

    global current_frame
    current_frame = ttk.Frame(root)
    current_frame.grid(row=1, column=0, columnspan=8, padx=20, pady=20)

    # Fetch the item data
    item = GetStorage()[item_id - 1]

    # Create form labels and entries
    ttk.Label(current_frame, text="الكمية").grid(row=0, column=0, padx=5, pady=5)
    count_entry = ttk.Entry(current_frame)
    count_entry.insert(0, item[1])
    count_entry.grid(row=0, column=1, padx=5, pady=5)
    
    ttk.Label(current_frame, text="النوع").grid(row=1, column=0, padx=5, pady=5)
    type_entry = ttk.Combobox(current_frame)
    type_entry['values'] = [item[1] for item in GetStorageType()]
    type_entry.insert(0, item[2])
    type_entry.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(current_frame, text="السعر").grid(row=2, column=0, padx=5, pady=5)
    price_entry = ttk.Entry(current_frame)
    price_entry.insert(0, item[3])
    price_entry.grid(row=2, column=1, padx=5, pady=5)
    
    ttk.Label(current_frame, text="التاريخ").grid(row=3, column=0, padx=5, pady=5)
    date_entry = ttk.Entry(current_frame)
    date_entry.insert(0, item[4])
    date_entry.grid(row=3, column=1, padx=5, pady=5)

    # Create a button to submit the form
    submit_btn = ttk.Button(current_frame, text="تعديل", command=lambda: UpdateStorage(count_entry.get(), type_entry.get(), price_entry.get(), date_entry.get(), item_id))
    submit_btn.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

def edit_type(type_id):
    NavBar('تعديل نوع المخزن')
    clear_frame()

    global current_frame
    current_frame = ttk.Frame(root)
    current_frame.grid(row=1, column=0, columnspan=8, padx=20, pady=20)

    # Fetch the type data
    type = GetStorageType()[type_id - 1]

    # Create form labels and entries
    ttk.Label(current_frame, text="النوع").grid(row=0, column=0, padx=5, pady=5)
    name_entry = ttk.Entry(current_frame)
    name_entry.insert(0, type[1])
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    # Create a button to submit the form
    submit_btn = ttk.Button(current_frame, text="تعديل", command=lambda: UpdateType(name_entry.get(), type_id))
    submit_btn.grid(row=1, column=0, columnspan=2, padx=5, pady=5)


def delete_item(item_id):
    DeleteStorage(item_id)
    Main()

def edit_type(type_id):
    NavBar('تعديل نوع المخزن')
    clear_frame()

    global current_frame
    current_frame = ttk.Frame(root)
    current_frame.grid(row=1, column=0, columnspan=8, padx=20, pady=20)

    # Fetch the type data
    type = GetStorageType()[type_id - 1]

    # Create form labels and entries
    ttk.Label(current_frame, text="النوع").grid(row=0, column=0, padx=5, pady=5)
    name_entry = ttk.Entry(current_frame)
    name_entry.insert(0, type[1])
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    # Create a button to submit the form
    submit_btn = ttk.Button(current_frame, text="تعديل", command=lambda: UpdateType(name_entry.get(), type_id))
    submit_btn.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

def delete_type(type_id):
    DeleteType(type_id)
    show_types()



if __name__ == '__main__':
    Main()
    # Create the main menu buttons
    main_btn = ttk.Button(root, text="عرض المخزن", command=Main)
    main_btn.grid(row=0, column=0, padx=20, pady=10)

    types_btn = ttk.Button(root, text="إدارة الأنواع", command=show_types)
    types_btn.grid(row=0, column=1, padx=20, pady=10)

    cars_btn = ttk.Button(root, text="عرض رصيد السيارة", command=ShowWalletCar)
    cars_btn.grid(row=0, column=2, padx=20, pady=10)

    

    root.mainloop()



