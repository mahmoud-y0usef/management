from tkinter import Menu

class CreateMenu:
    def __init__(self, root):
        self.root = root
        self.menu = Menu(root)
        root.config(menu=self.menu)


    def add_menu(self, name, items):
        new_menu = Menu(self.menu  , tearoff=0 , font=('Arial', 12) , bg='white' , fg='black' , activebackground='black' , activeforeground='white')
        self.menu.add_cascade(label=name, menu=new_menu)
        for item in items:
            new_menu.add_command(label=item[0], command=item[1])

    def add_title(self, title):
        self.root.title(title)

    def geometry(self, geometry):
        self.root.geometry(geometry)

    def add_separator(self):
        self.menu.add_separator()

    def add_command(self, label, command):
        self.menu.add_command(label=label, command=command)

    def add_checkbutton(self, label, command):
        self.menu.add_checkbutton(label=label, command=command)
        
    def add_radiobutton(self, label, command):
        self.menu.add_radiobutton(label=label, command=command)





    