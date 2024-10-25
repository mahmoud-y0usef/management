from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
import sqlite3
from tkcalendar import DateEntry
from datetime import datetime


current_frame = None

def validate_entries(entries):
    for entry in entries.values():
        if entry.get() == "":
            return False
    return True

def clear_entries(entries):
    for entry in entries.values():
        entry.delete(0, tk.END)

def clear_frame():
    """Clears the current frame to prevent overlapping views."""
    global current_frame
    if current_frame is not None:
        current_frame.destroy()
    current_frame = None  # Reset the global variable to None



conn = sqlite3.connect('data.db')
c = conn.cursor()



## select tables
def GetStorage():
    c.execute('SELECT * FROM storage')
    return c.fetchall()


def GetStorageType():
    c.execute('SELECT * FROM type')
    return c.fetchall()


## count of all total price in storage
def GetTotalPrice():
    c.execute('SELECT SUM(count * price) FROM storage')
    return c.fetchone()[0]


def getWalletCars():
    c.execute("SELECT * FROM wallet")
    return c.fetchall()


def GetTotalWalletPrice():
    c.execute('SELECT SUM(count * price) FROM wallet')
    return c.fetchone()[0]

def GetReturns():
    c.execute('SELECT * FROM returns')
    return c.fetchall()

def GetIndebtedness():
    c.execute('SELECT * FROM indebtedness')
    return c.fetchall()

def GetTotalIndebtednessForClients():
    """حساب إجمالي الدين على العملاء."""
    c.execute("SELECT SUM(price) FROM indebtedness WHERE type = 'عميل'")
    result = c.fetchone()
    return result[0] if result[0] is not None else 0

def GetTotalIndebtednessForSuppliers():
    """حساب إجمالي الدين إلى الموردين."""
    c.execute("SELECT SUM(price) FROM indebtedness WHERE type = 'مورد'")
    result = c.fetchone()
    return result[0] if result[0] is not None else 0


## insert tables
def AddStorage(entries):
    """إضافة عنصر إلى المخزن بعد التحقق من عدم وجود نوع مكرر."""
    if not validate_entries(entries):
        messagebox.showerror("خطأ", "جميع الحقول مطلوبة. الرجاء ملء جميع الحقول.")
    else:
        count = entries['count'].get()
        item_type = entries['type'].get()
        price = entries['price'].get()
        date = entries['date'].get()

        # التحقق من وجود عنصر بنفس النوع مسبقًا في المخزن
        c.execute('SELECT * FROM storage WHERE type = ?', (item_type,))
        existing_item = c.fetchone()  # جلب أول عنصر مطابق (إن وجد)

        if existing_item:
            # إذا كان النوع موجودًا بالفعل، عرض رسالة خطأ
            messagebox.showerror("خطأ", f"العنصر من النوع '{item_type}' موجود بالفعل.")
        else:
            # إذا لم يكن موجودًا، قم بإضافة العنصر
            c.execute(
                'INSERT INTO storage (count, type, price, date) VALUES (?, ?, ?, ?)',
                (count, item_type, price, date)
            )
            conn.commit()  # حفظ التغييرات في قاعدة البيانات
            clear_entries(entries)  # مسح الحقول بعد الإضافة
            messagebox.showinfo("نجاح", "تمت إضافة العنصر بنجاح!")


def AddType(name):
    """إضافة نوع جديد بعد التحقق من وجوده."""
    if not validate_entries(name):
        messagebox.showerror("خطأ", "جميع الحقول مطلوبة. الرجاء ملء جميع الحقول.")
        return

    # التحقق مما إذا كان الاسم موجودًا بالفعل في الجدول
    c.execute('SELECT name FROM type WHERE name = ?', (name['name'].get(),))
    existing_type = c.fetchone()

    if existing_type:
        # عرض رسالة خطأ إذا كان الاسم موجودًا
        messagebox.showerror("خطأ", "هذا النوع موجود بالفعل.")
    else:
        # إدراج النوع الجديد إذا لم يكن موجودًا
        c.execute('INSERT INTO type (name) VALUES (?)', (name['name'].get(),))
        clear_entries(name)  # مسح الحقول بعد الإدراج
        conn.commit()  # تأكيد التغييرات
        messagebox.showinfo("نجاح", "تمت إضافة النوع بنجاح!")



## delete tables
def DeleteStorage(id):
    c.execute('DELETE FROM storage WHERE id = ?', (id,))
    conn.commit()

def DeleteType(id):
    c.execute('DELETE FROM type WHERE id = ?', (id,))
    conn.commit()


## update tables
def UpdateStorage(entries, id):
    if not validate_entries(entries):
        messagebox.showerror("خطأ", "جميع الحقول مطلوبة. الرجاء ملء جميع الحقول.")
    else:
        count = entries['count'].get()
        item_type = entries['type'].get()
        price = entries['price'].get()
        date = entries['date'].get()

        c.execute('UPDATE storage SET count = ?, type = ?, price = ?, date = ? WHERE id = ?', (count, item_type, price, date, id))
        conn.commit()
        messagebox.showinfo("نجاح", "تم تعديل العنصر بنجاح!")

def UpdateType(name, id):
    if not validate_entries(name):
        messagebox.showerror("خطأ", "جميع الحقول مطلوبة. الرجاء ملء جميع الحقول.")
    else:
        c.execute('UPDATE type SET name = ? WHERE id = ?', (name['name'].get(), id))
        conn.commit()
        messagebox.showinfo("نجاح", "تم تعديل النوع بنجاح!")


## Add storage view
def addStorageView(root):
    """Show the form for adding a new storage item."""
    clear_frame()  # Ensure no previous view overlaps

    global current_frame
    current_frame = ttk.Frame(root)
    current_frame.grid(row=1, column=0, columnspan=8, padx=20, pady=20)
    root.title("إضافة إلى المخزن")
    entries = {}
    # Form labels and entries
    ttk.Label(current_frame, text="الكمية").grid(row=0, column=0, padx=5, pady=5)
    count_entry = ttk.Entry(current_frame)
    count_entry.grid(row=0, column=1, padx=5, pady=5)
    entries['count'] = count_entry

    ttk.Label(current_frame, text="النوع").grid(row=1, column=0, padx=5, pady=5)
    type_entry = ttk.Combobox(current_frame, values=[item[1] for item in GetStorageType()])
    type_entry.grid(row=1, column=1, padx=5, pady=5)
    entries['type'] = type_entry

    ttk.Label(current_frame, text="السعر").grid(row=2, column=0, padx=5, pady=5)
    price_entry = ttk.Entry(current_frame)
    price_entry.grid(row=2, column=1, padx=5, pady=5)
    entries['price'] = price_entry

    ttk.Label(current_frame, text="التاريخ").grid(row=3, column=0, padx=5, pady=5)
    date_entry = DateEntry(current_frame, width=12, background='darkblue', foreground='white', 
                           borderwidth=2, year=datetime.now().year, month=datetime.now().month, 
                           day=datetime.now().day)
    date_entry.grid(row=3, column=1, padx=5, pady=5)
    entries['date'] = date_entry

    # Submit button
    submit_btn = ttk.Button(current_frame, text="إضافة", command=lambda: AddStorage(entries))
    submit_btn.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    # Clear form button
    clear_btn = ttk.Button(current_frame, text="مسح", command=lambda: clear_entries(entries))
    clear_btn.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    # Back button to return to storage view
    back_btn = ttk.Button(current_frame, text="رجوع", command=lambda: storageDisplay(root))
    back_btn.grid(row=6, column=0, columnspan=2, pady=10)


## edit Storage View
def edit_item(root, item_id):
    clear_frame()
    global current_frame
    current_frame = ttk.Frame(root)
    current_frame.grid(row=1, column=0, columnspan=8, padx=20, pady=20)
    root.title("تعديل العنصر")
    # Fetch the item data using the actual item_id
    c.execute('SELECT * FROM storage WHERE id = ?', (item_id,))
    item = c.fetchone()

    if item is None:
        messagebox.showerror("خطأ", "العنصر غير موجود.")
        return

    entries = {}
    # Create form labels and entries
    ttk.Label(current_frame, text="الكمية").grid(row=0, column=0, padx=5, pady=5)
    count_entry = ttk.Entry(current_frame)
    count_entry.insert(0, item[1])
    count_entry.grid(row=0, column=1, padx=5, pady=5)
    entries['count'] = count_entry

    ttk.Label(current_frame, text="النوع").grid(row=1, column=0, padx=5, pady=5)
    type_entry = ttk.Combobox(current_frame, values=[item[1] for item in GetStorageType()])
    type_entry.set(item[2])
    type_entry.grid(row=1, column=1, padx=5, pady=5)
    entries['type'] = type_entry

    ttk.Label(current_frame, text="السعر").grid(row=2, column=0, padx=5, pady=5)
    price_entry = ttk.Entry(current_frame)
    price_entry.insert(0, item[3])
    price_entry.grid(row=2, column=1, padx=5, pady=5)
    entries['price'] = price_entry

    ttk.Label(current_frame, text="التاريخ").grid(row=3, column=0, padx=5, pady=5)
    date_entry = DateEntry(current_frame, width=12, background='darkblue', foreground='white', 
                           borderwidth=2)
    date_entry.set_date(item[4])
    date_entry.grid(row=3, column=1, padx=5, pady=5)
    entries['date'] = date_entry

    # Create a button to submit the form
    submit_btn = ttk.Button(current_frame, text="تعديل", command=lambda: UpdateStorage(entries, item_id))
    submit_btn.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    # Create a button to clear the form
    clear_btn = ttk.Button(current_frame, text="مسح", command=lambda: clear_entries(entries))
    clear_btn.grid(row=5, column=0, columnspan=2, padx=5, pady=5)


## Delete item
def delete_item(root , item_id):
    DeleteStorage(item_id)
    storageDisplay(root)

## display Storage View
def storageDisplay(root):
    """عرض المخزن مع العناصر الحالية وإمكانية إضافة عناصر جديدة."""
    clear_frame()  # تنظيف الإطار السابق دائمًا

    # إنشاء Canvas و Scrollbar
    canvas = tk.Canvas(root)
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    # إنشاء إطار داخل الـ Canvas لاحتواء المحتويات
    scrollable_frame = ttk.Frame(canvas)

    # تحديث منطقة التمرير عند تغيير حجم الإطار الداخلي
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    # إضافة الإطار داخل الـ Canvas
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    # وضع الـ Canvas و Scrollbar في الشبكة
    canvas.grid(row=1, column=0, columnspan=8, sticky="nsew", padx=20, pady=20)
    scrollbar.grid(row=1, column=8, sticky="ns")

    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)

    global current_frame
    current_frame = scrollable_frame  # تحديث الإطار الحالي

    root.title("عرض المخزن")

    # العناوين المحدثة
    headers = ["المعرف", "الكمية", "النوع", "السعر", "التاريخ", "الإجمالي", "تعديل", "حذف", "إضافة"]

    # عرض العناوين
    for idx, header in enumerate(headers):
        ttk.Label(current_frame, text=header, font=('Arial', 12, 'bold'), padding=10).grid(row=0, column=idx)

    # جلب البيانات من المخزن
    storage = GetStorage()

    for index, item in enumerate(storage):
        item_id, count, item_type, price, date = item  # تفكيك التفاصيل
        total = int(count) * float(price)  # حساب الإجمالي

        values = [item_id, count, item_type, price, date, f"{total:.2f}"]

        for col, value in enumerate(values):
            ttk.Label(current_frame, text=value, padding=10).grid(row=index + 1, column=col)

        # زر التعديل
        edit_btn = ttk.Button(current_frame, text="تعديل", command=lambda id=item_id: edit_item(root, id))
        edit_btn.grid(row=index + 1, column=len(values), padx=5, pady=5)

        # زر الحذف
        del_btn = ttk.Button(current_frame, text="حذف", command=lambda id=item_id: delete_item(root, id))
        del_btn.grid(row=index + 1, column=len(values) + 1, padx=5, pady=5)

        # زر الإضافة إلى المحفظة
        add_to_wallet_btn = ttk.Button(current_frame, text="إضافة إلى السيارة", command=lambda id=item_id: AddToWallet(root, id))
        add_to_wallet_btn.grid(row=index + 1, column=len(values) + 2, padx=5, pady=5)

    # عرض السعر الإجمالي
    total_price = GetTotalPrice()
    ttk.Label(current_frame, text="الإجمالي", font=('Arial', 12, 'bold'), padding=10).grid(row=len(storage) + 1, column=5)
    ttk.Label(current_frame, text=f"{total_price:.2f}", padding=10).grid(row=len(storage) + 1, column=6)

    # زر إضافة إلى المخزن
    add_btn = ttk.Button(current_frame, text="إضافة إلى المخزن", command=lambda: addStorageView(root))
    add_btn.grid(row=len(storage) + 2, column=0, columnspan=2, pady=10)



## Add new type view
def AddNewType(root):
    clear_frame()
    global current_frame
    current_frame = ttk.Frame(root)
    current_frame.grid(row=1, column=0, columnspan=8, padx=20, pady=20)
    root.title("إضافة نوع جديد")
    entries = {}
    # Create form labels and entries
    ttk.Label(current_frame, text="النوع").grid(row=0, column=0, padx=5, pady=5)
    name_entry = ttk.Entry(current_frame)
    name_entry.grid(row=0, column=1, padx=5, pady=5)
    entries['name'] = name_entry

    # Create a button to submit the form
    submit_btn = ttk.Button(current_frame, text="إضافة", 
                            command=lambda: AddType(entries))
    submit_btn.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    # Create a button to clear the form
    clear_btn = ttk.Button(current_frame, text="مسح", 
                           command=lambda: clear_entries(entries))
    clear_btn.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    # Button to go back to types display view
    back_btn = ttk.Button(current_frame, text="رجوع", 
                          command=lambda: typesDisplay(root))
    back_btn.grid(row=3, column=0, columnspan=2, pady=10)

    


## edit type view
def edit_type(root, type_id):
    clear_frame()
    global current_frame
    current_frame = ttk.Frame(root)
    current_frame.grid(row=1, column=0, columnspan=8, padx=20, pady=20)
    root.title("تعديل النوع")
    # Fetch the type data
    c.execute('SELECT * FROM type WHERE id = ?', (type_id,))
    type_data = c.fetchone()

    if type_data is None:
        messagebox.showerror("خطأ", "النوع غير موجود.")
        return

    entries = {}
    # Create form labels and entries
    ttk.Label(current_frame, text="النوع").grid(row=0, column=0, padx=5, pady=5)
    name_entry = ttk.Entry(current_frame)
    name_entry.insert(0, type_data[1])
    name_entry.grid(row=0, column=1, padx=5, pady=5)
    entries['name'] = name_entry

    # Create a button to submit the form
    submit_btn = ttk.Button(current_frame, text="تعديل", 
                            command=lambda: UpdateType(entries, type_id))
    submit_btn.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    # Create a button to clear the form
    clear_btn = ttk.Button(current_frame, text="مسح", 
                           command=lambda: clear_entries(entries))
    clear_btn.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    # Button to go back to types display view
    back_btn = ttk.Button(current_frame, text="رجوع", 
                          command=lambda: typesDisplay(root))
    back_btn.grid(row=3, column=0, columnspan=2, pady=10)





## delete type
def delete_type(root , type_id):
    DeleteType(type_id)
    typesDisplay(root)

## display types View
def typesDisplay(root):
    clear_frame()
    global current_frame

    # Create a canvas and a scrollbar
    canvas = tk.Canvas(root)
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas to hold the content
    scrollable_frame = ttk.Frame(canvas)

    # Configure the canvas to update the scroll region when the frame size changes
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    # Add the frame to the canvas
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    # Place the canvas and scrollbar on the grid
    canvas.grid(row=1, column=0, columnspan=8, sticky="nsew", padx=20, pady=20)
    scrollbar.grid(row=1, column=8, sticky="ns")

    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Update the global frame reference
    current_frame = scrollable_frame

    root.title("عرض الأنواع")

    # Define column headers with equal spacing
    headers = ["المعرف", "النوع", "تعديل", "حذف"]
    for idx, header in enumerate(headers):
        ttk.Label(current_frame, text=header, font=('Arial', 12, 'bold'), padding=10).grid(row=0, column=idx)

    # Fetch and display the storage types
    types = GetStorageType()
    for index, item in enumerate(types):
        for col, value in enumerate(item):
            ttk.Label(current_frame, text=value, padding=10).grid(row=index + 1, column=col)

        # Add Edit button
        edit_btn = ttk.Button(current_frame, text="تعديل", 
                              command=lambda id=item[0]: edit_type(root, id))
        edit_btn.grid(row=index + 1, column=len(item), padx=5, pady=5)

        # Add Delete button
        del_btn = ttk.Button(current_frame, text="حذف", 
                             command=lambda id=item[0]: delete_type(root, id))
        del_btn.grid(row=index + 1, column=len(item) + 1, padx=5, pady=5)

    # Button to open Add New Type view
    add_btn = ttk.Button(current_frame, text="إضافة نوع جديد", 
                         command=lambda: AddNewType(root))
    add_btn.grid(row=len(types) + 2, column=0, columnspan=2, pady=10)


## Add to wallet car view
def AddToWallet(root , item_id):
    clear_frame()
    global current_frame

    current_frame = ttk.Frame(root)
    current_frame.grid(row=1, column=0, columnspan=8, padx=20, pady=20)
    root.title("إضافة إلى السيارة")

    entries = {}    

    c.execute('SELECT * FROM storage WHERE id = ?', (item_id,))
    item = c.fetchone()

    if item is None:
        messagebox.showerror("خطأ", "العنصر غير موجود.")
        return

    
    ttk.Label(current_frame, text="الكمية التي تريد إدخالها إلي السيارة").grid(row=0, column=0, padx=5, pady=5)
    count_entry = ttk.Entry(current_frame)
    count_entry.insert(0, item[1])
    count_entry.grid(row=0, column=1, padx=5, pady=5)
    entries['count'] = count_entry

    ## button add to wallet
    submit_btn = ttk.Button(current_frame, text="إضافة إلى السيارة", command=lambda: AddToWalletCar(root , entries, item_id))
    submit_btn.grid(row=1, column=0, columnspan=2, padx=5, pady=5)


def AddToWalletCar(root, entires, item_id):
    if not validate_entries(entires):
        messagebox.showerror("خطأ", "جميع الحقول مطلوبة. الرجاء ملء جميع الحقول.")
    else:
        count = int(entires['count'].get())  # Ensure count is an integer
        
        # Fetch the item from storage
        c.execute('SELECT * FROM storage WHERE id = ?', (item_id,))
        item = c.fetchone()
        
        if not item:
            messagebox.showerror("خطأ", "العنصر غير موجود في المخزون.")
            return
        
        if count > int(item[1]):
            messagebox.showerror("خطأ", "الكمية المدخلة أكبر من الكمية المتوفرة.")
        else:
            # Check if the item type already exists in the wallet
            c.execute('SELECT * FROM wallet WHERE type = ?', (item[2],))
            wallet_item = c.fetchone()

            if wallet_item:
                # Update the count if the item exists in the wallet
                new_count = int(wallet_item[1]) + count
                c.execute('UPDATE wallet SET count = ? WHERE type = ?', (new_count, item[2]))
            else:
                # Insert the new item into the wallet if it doesn't exist
                c.execute(
                    'INSERT INTO wallet (count, type, price, date) VALUES (?, ?, ?, ?)',
                    (count, item[2], item[3], item[4])
                )
            
            # Update the storage count
            new_storage_count = int(item[1]) - count
            c.execute('UPDATE storage SET count = ? WHERE id = ?', (new_storage_count, item_id))

            conn.commit()
            messagebox.showinfo("نجاح", "تمت إضافة العنصر إلى السيارة بنجاح!")
            
            storageDisplay(root)




def displayWallet(root):
    clear_frame()  # تنظيف الإطار السابق دائمًا

    # إنشاء Canvas و Scrollbar للتمرير
    canvas = tk.Canvas(root)
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    # إنشاء إطار داخلي للـ Canvas لاحتواء المحتويات
    scrollable_frame = ttk.Frame(canvas)

    # تحديث منطقة التمرير عند تغيير حجم الإطار الداخلي
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    # إضافة الإطار داخل الـ Canvas
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    # وضع الـ Canvas و Scrollbar في الشبكة
    canvas.grid(row=1, column=0, columnspan=8, sticky="nsew", padx=20, pady=20)
    scrollbar.grid(row=1, column=8, sticky="ns")

    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)

    global current_frame
    current_frame = scrollable_frame  # تحديث الإطار الحالي

    root.title("عرض رصيد السيارة")

    # العناوين
    headers = ["المعرف", "الكمية", "النوع", "السعر", "التاريخ", "الإجمالي", "إرجاع إلي المخزن"]

    # عرض العناوين
    for idx, header in enumerate(headers):
        ttk.Label(current_frame, text=header, font=('Arial', 12, 'bold'), padding=10).grid(row=0, column=idx)

    wallet = getWalletCars()

    for index, item in enumerate(wallet):
        item_id, count, item_type, price, date = item
        total = int(count) * float(price)

        values = [item_id, count, item_type, price, date, f"{total:.2f}"]

        for col, value in enumerate(values):
            ttk.Label(current_frame, text=value, padding=10).grid(row=index + 1, column=col)

        # زر لإرجاع العنصر إلى المخزن
        return_btn = ttk.Button(current_frame, text="إرجاع إلي المخزن", command=lambda id=item_id: check_count_return(root, id))
        return_btn.grid(row=index + 1, column=len(values), padx=5, pady=5)

        # عرض السعر الإجمالي
        total_price = GetTotalWalletPrice()
        ttk.Label(current_frame, text="الإجمالي", font=('Arial', 12, 'bold'), padding=10).grid(row=len(wallet) + 1, column=5)
        ttk.Label(current_frame, text=f"{total_price:.2f}", padding=10).grid(row=len(wallet) + 1, column=6)


def check_count_return(root, item_id):
    """عرض واجهة إدخال الكمية المراد إرجاعها."""
    clear_frame()
    global current_frame

    current_frame = ttk.Frame(root)
    current_frame.grid(row=1, column=0, columnspan=8, padx=20, pady=20)
    root.title("إرجاع العنصر إلى المخزن")

    entries = {}

    # جلب العنصر من المحفظة
    c.execute('SELECT * FROM wallet WHERE id = ?', (item_id,))
    item = c.fetchone()

    if item is None:
        messagebox.showerror("خطأ", "العنصر غير موجود.")
        return

    # عرض إدخال الكمية
    ttk.Label(current_frame, text="الكمية التي تريد إرجاعها إلى المخزن:").grid(row=0, column=0, padx=5, pady=5)
    count_entry = ttk.Entry(current_frame)
    count_entry.insert(0, item[1])  # إدخال الكمية الحالية في المحفظة
    count_entry.grid(row=0, column=1, padx=5, pady=5)
    entries['count'] = count_entry

    # زر إرجاع إلى المخزن
    submit_btn = ttk.Button(current_frame, text="إرجاع إلى المخزن", 
                            command=lambda: return_to_storage(root, entries, item_id))
    submit_btn.grid(row=1, column=0, columnspan=2, padx=5, pady=5)


def return_to_storage(root, entries, item_id):
    """إرجاع الكمية المطلوبة إلى المخزن."""
    try:
        # جلب العنصر من المحفظة
        c.execute('SELECT type, count FROM wallet WHERE id = ?', (item_id,))
        wallet_item = c.fetchone()

        if not wallet_item:
            messagebox.showerror("خطأ", "العنصر غير موجود في المحفظة.")
            return

        item_type, wallet_count = wallet_item

        # الحصول على الكمية المراد إرجاعها
        return_count = int(entries['count'].get())

        if return_count > wallet_count:
            messagebox.showerror("خطأ", "الكمية المراد إرجاعها أكبر من المتاحة.")
            return

        # جلب الكمية الحالية في المخزن
        c.execute('SELECT count FROM storage WHERE type = ?', (item_type,))
        storage_item = c.fetchone()
        storage_count = storage_item[0] if storage_item else 0

        # تحديث الكمية في المخزن
        new_storage_count = storage_count + return_count
        if storage_item:
            c.execute('UPDATE storage SET count = ? WHERE type = ?', (new_storage_count, item_type))
        else:
            c.execute('INSERT INTO storage (type, count) VALUES (?, ?)', (item_type, return_count))

        # إدخال البيانات في جدول المرتجعات
        c.execute('INSERT INTO returns (count, type, price, date) '
                  'SELECT ?, type, price, date FROM wallet WHERE id = ?', (return_count, item_id))

        # تقليل الكمية في المحفظة أو حذفها إذا أصبحت صفر
        new_wallet_count = wallet_count - return_count
        if new_wallet_count > 0:
            c.execute('UPDATE wallet SET count = ? WHERE id = ?', (new_wallet_count, item_id))
        else:
            c.execute('DELETE FROM wallet WHERE id = ?', (item_id,))

        # تأكيد التغييرات
        conn.commit()

        # تحديث واجهة المستخدم
        displayWallet(root)

        # إظهار رسالة نجاح
        messagebox.showinfo("نجاح", "تمت إعادة العنصر إلى المخزن بنجاح.")
    except Exception as e:
        conn.rollback()  # التراجع عن التغييرات في حالة حدوث خطأ
        messagebox.showerror("خطأ", f"حدث خطأ أثناء إعادة العنصر: {str(e)}")


def ShowReturns(root):
    clear_frame()  # تنظيف الإطار السابق دائمًا

    # إنشاء Canvas و Scrollbar للتمرير
    canvas = tk.Canvas(root)
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    # إنشاء إطار داخلي للـ Canvas لاحتواء المحتويات
    scrollable_frame = ttk.Frame(canvas)

    # تحديث منطقة التمرير عند تغيير حجم الإطار الداخلي
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    # إضافة الإطار داخل الـ Canvas
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    # وضع الـ Canvas و Scrollbar في الشبكة
    canvas.grid(row=1, column=0, columnspan=8, sticky="nsew", padx=20, pady=20)
    scrollbar.grid(row=1, column=8, sticky="ns")

    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)

    global current_frame
    current_frame = scrollable_frame  # تحديث الإطار الحالي

    root.title("عرض المرتجعات")

    # العناوين
    headers = ["المعرف", "الكمية", "النوع", "السعر", "التاريخ", "الإجمالي" , "مسح"]

    # عرض العناوين
    for idx, header in enumerate(headers):
        ttk.Label(current_frame, text=header, font=('Arial', 12, 'bold'), padding=10).grid(row=0, column=idx)

    returns = GetReturns()

    for index, item in enumerate(returns):
        item_id, count, item_type, price, date = item
        total = int(count) * float(price)

        values = [item_id, count, item_type, price, date, f"{total:.2f}"]


        for col, value in enumerate(values):
            ttk.Label(current_frame, text=value, padding=10).grid(row=index + 1, column=col)

        # زر لمسح العنصر

        del_btn = ttk.Button(current_frame, text="مسح", command=lambda id=item_id: delete_return(root, id))
        del_btn.grid(row=index + 1, column=len(values), padx=5, pady=5)

    
def delete_return(root , item_id):
    c.execute('DELETE FROM returns WHERE id = ?', (item_id,))
    conn.commit()
    ShowReturns(root)


def Showindebtedness(root):
    """عرض الديون باستخدام Canvas و Scrollbar."""
    clear_frame()  # تنظيف الإطار السابق

    # إنشاء Canvas و Scrollbar للتمرير
    canvas = tk.Canvas(root)
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    # إنشاء إطار داخلي للـ Canvas لاحتواء المحتويات
    scrollable_frame = ttk.Frame(canvas)

    # تحديث منطقة التمرير عند تغيير حجم الإطار الداخلي
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    # إضافة الإطار داخل الـ Canvas
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    # وضع الـ Canvas و Scrollbar في الشبكة
    canvas.grid(row=1, column=0, columnspan=8, sticky="nsew", padx=20, pady=20)
    scrollbar.grid(row=1, column=8, sticky="ns")

    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)

    global current_frame
    current_frame = scrollable_frame  # تحديث الإطار الحالي

    root.title("عرض الديون")

    # العناوين
    headers = ["المعرف", "الإسم", "النوع", "السعر", "التاريخ", "تعديل", "مسح"]

    # عرض العناوين
    for idx, header in enumerate(headers):
        ttk.Label(current_frame, text=header, font=('Arial', 12, 'bold'), padding=10).grid(row=0, column=idx)

    # جلب الديون
    indebtedness = GetIndebtedness()

    for index, item in enumerate(indebtedness):
        item_id, name, item_type, price, date = item
        values = [item_id, name, item_type, price, date]

        for col, value in enumerate(values):
            ttk.Label(current_frame, text=value, padding=10).grid(row=index + 1, column=col)

        # زر التعديل
        edit_btn = ttk.Button(
            current_frame, text="تعديل", 
            command=lambda id=item_id: edit_indebtedness(root, id)
        )
        edit_btn.grid(row=index + 1, column=len(values), padx=5, pady=5)

        # زر المسح
        del_btn = ttk.Button(
            current_frame, text="مسح", 
            command=lambda id=item_id: delete_indebtedness(root, id)
        )
        del_btn.grid(row=index + 1, column=len(values) + 1, padx=5, pady=5)

    # عرض إجمالي الدين على العملاء
    total_price1 = GetTotalIndebtednessForClients()
    ttk.Label(current_frame, text="إجمالي الدين على العملاء", font=('Arial', 12, 'bold'), padding=10).grid(
        row=len(indebtedness) + 1, column=0, columnspan=3, sticky="w", padx=5, pady=5
    )
    ttk.Label(current_frame, text=f"{total_price1:.2f}", padding=10).grid(
        row=len(indebtedness) + 1, column=3, columnspan=2, sticky="e", padx=5, pady=5
    )

    # عرض إجمالي الدين إلى الموردين
    total_price = GetTotalIndebtednessForSuppliers()
    ttk.Label(current_frame, text="إجمالي الدين إلى الموردين", font=('Arial', 12, 'bold'), padding=10).grid(
        row=len(indebtedness) + 2, column=0, columnspan=3, sticky="w", padx=5, pady=5
    )
    ttk.Label(current_frame, text=f"{total_price:.2f}", padding=10).grid(
        row=len(indebtedness) + 2, column=3, columnspan=2, sticky="e", padx=5, pady=5
    )

    # زر إضافة دين جديد
    add_btn = ttk.Button(current_frame, text="إضافة دين جديد", command=lambda: add_indebtedness(root))
    add_btn.grid(row=len(indebtedness) + 3, column=0, columnspan=2, pady=10)




def add_indebtedness(root):
    clear_frame()
    global current_frame
    current_frame = ttk.Frame(root)
    current_frame.grid(row=1, column=0, columnspan=8, padx=20, pady=20)
    root.title("إضافة دين جديد")
    entries = {}
    # Create form labels and entries
    ttk.Label(current_frame, text="الإسم").grid(row=0, column=0, padx=5, pady=5)
    name_entry = ttk.Entry(current_frame)
    name_entry.grid(row=0, column=1, padx=5, pady=5)
    entries['name'] = name_entry

    ttk.Label(current_frame, text="النوع").grid(row=1, column=0, padx=5, pady=5)
    headers = ["عميل" , "مورد"]
    type_entry = ttk.Combobox(current_frame, values=headers)
    type_entry.grid(row=1, column=1, padx=5, pady=5)
    entries['type'] = type_entry

    ttk.Label(current_frame, text="السعر").grid(row=2, column=0, padx=5, pady=5)
    price_entry = ttk.Entry(current_frame)
    price_entry.grid(row=2, column=1, padx=5, pady=5)
    entries['price'] = price_entry

    ttk.Label(current_frame, text="التاريخ").grid(row=3, column=0, padx=5, pady=5)
    date_entry = DateEntry(current_frame, width=12, background='darkblue', foreground='white', 
                           borderwidth=2)
    date_entry.grid(row=3, column=1, padx=5, pady=5)
    entries['date'] = date_entry

    # Submit button
    submit_btn = ttk.Button(current_frame, text="إضافة", command=lambda: AddIndebtedness(root , entries))
    submit_btn.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    # Clear form button
    clear_btn = ttk.Button(current_frame, text="مسح", command=lambda: clear_entries(entries))
    clear_btn.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    # Back button to return to indebtedness view
    back_btn = ttk.Button(current_frame, text="رجوع", command=lambda: Showindebtedness(root))
    back_btn.grid(row=6, column=0, columnspan=2, pady=10)


def edit_indebtedness(root, item_id):
    clear_frame()
    global current_frame
    current_frame = ttk.Frame(root)
    current_frame.grid(row=1, column=0, columnspan=8, padx=20, pady=20)
    root.title("تعديل الدين")
    # Fetch the item data using the actual item_id
    c.execute('SELECT * FROM indebtedness WHERE id = ?', (item_id,))
    item = c.fetchone()

    if item is None:
        messagebox.showerror("خطأ", "الدين غير موجود.")
        return

    entries = {}
    # Create form labels and entries
    ttk.Label(current_frame, text="الإسم").grid(row=0, column=0, padx=5, pady=5)
    name_entry = ttk.Entry(current_frame)
    name_entry.insert(0, item[1])
    name_entry.grid(row=0, column=1, padx=5, pady=5)
    entries['name'] = name_entry

    ttk.Label(current_frame, text="النوع").grid(row=1, column=0, padx=5, pady=5)
    headers = ["عميل" , "مورد"]
    type_entry = ttk.Combobox(current_frame, values=headers)
    type_entry.set(item[2])
    type_entry.grid(row=1, column=1, padx=5, pady=5)
    entries['type'] = type_entry

    ttk.Label(current_frame, text="السعر").grid(row=2, column=0, padx=5, pady=5)
    price_entry = ttk.Entry(current_frame)
    price_entry.insert(0, item[3])
    price_entry.grid(row=2, column=1, padx=5, pady=5)
    entries['price'] = price_entry

    ttk.Label(current_frame, text="التاريخ").grid(row=3, column=0, padx=5, pady=5)
    date_entry = DateEntry(current_frame, width=12, background='darkblue', foreground='white', 
                           borderwidth=2)
    date_entry.set_date(item[4])
    date_entry.grid(row=3, column=1, padx=5, pady=5)
    entries['date'] = date_entry

    # Create a button to submit the form
    submit_btn = ttk.Button(current_frame, text="تعديل", command=lambda: UpdateIndebtedness(root , entries, item_id))
    submit_btn.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    # Create a button to clear the form
    clear_btn = ttk.Button(current_frame, text="مسح", command=lambda: clear_entries(entries))
    clear_btn.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    # Button to go back to indebtedness display view
    back_btn = ttk.Button(current_frame, text="رجوع", command=lambda: Showindebtedness(root))
    back_btn.grid(row=6, column=0, columnspan=2, pady=10)


def AddIndebtedness(root , entries):
    if not validate_entries(entries):
        messagebox.showerror("خطأ", "جميع الحقول مطلوبة. الرجاء ملء جميع الحقول.")
    else:
        name = entries['name'].get()
        item_type = entries['type'].get()
        price = entries['price'].get()
        date = entries['date'].get()

        c.execute('INSERT INTO indebtedness (name, type, price, date) VALUES (?, ?, ?, ?)',
                  (name, item_type, price, date))
        conn.commit()
        messagebox.showinfo("نجاح", "تمت إضافة الدين بنجاح!")
        Showindebtedness(root)


def UpdateIndebtedness(root ,entries, item_id):
    if not validate_entries(entries):
        messagebox.showerror("خطأ", "جميع الحقول مطلوبة. الرجاء ملء جميع الحقول.")
    else:
        name = entries['name'].get()
        item_type = entries['type'].get()
        price = entries['price'].get()
        date = entries['date'].get()

        c.execute('UPDATE indebtedness SET name = ?, type = ?, price = ?, date = ? WHERE id = ?',
                  (name, item_type, price, date, item_id))
        conn.commit()
        messagebox.showinfo("نجاح", "تم تحديث الدين بنجاح!")
        Showindebtedness(root)

def delete_indebtedness(root , item_id):
    c.execute('DELETE FROM indebtedness WHERE id = ?', (item_id,))
    conn.commit()
    Showindebtedness(root)