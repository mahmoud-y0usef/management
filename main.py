from menu import CreateMenu
from storage import *
if __name__ == '__main__':
    root = tk.Tk()
    menu = CreateMenu(root)
    menu.geometry('800x600+300+200')
    menu.add_title('القائمة الرئيسية')
    menu.add_menu('المخزن', [('جديد',lambda : addStorageView(root)), ('عرض',lambda : storageDisplay(root))])
  
    main_btn = ttk.Button(root, text="عرض المخزن", command= lambda: storageDisplay(root))
    main_btn.grid(row=0, column=0, padx=20, pady=10)

    view_types_button = ttk.Button(root, text="عرض الأنواع", command=lambda: typesDisplay(root))
    view_types_button.grid(row=0, column=1, padx=20, pady=10)

    cars_btn = ttk.Button(root, text="عرض رصيد السيارة", command= lambda: displayWallet(root))
    cars_btn.grid(row=0, column=2, padx=20, pady=10)

    menu.add_menu('رصيد السيارة', [('عرض', lambda : displayWallet(root))])
    menu.add_menu('المرتجعات', [('عرض', lambda: ShowReturns(root))])
    menu.add_menu('المديونية', [('جديد', lambda: add_indebtedness(root)), ('عرض', lambda: Showindebtedness(root))])
    menu.add_menu('خروج', [('خروج', root.quit)])
    

    root.mainloop()