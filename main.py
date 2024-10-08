import tkinter as tk
from menu import CreateMenu
root = tk.Tk()

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
    root.mainloop()

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

def AddNewStorage():
    NavBar('إضافة مخزن جديد')

def Main():
    NavBar('المخزن')

if __name__ == '__main__':
    Main()



