import json
from menu import CreateMenu
from tkinter import *
from tkinter import font
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image 
import time
from storage import *
current_theme = 'light'
updatemenuisopen = False
class LoginPage:
    def __init__(self, window):
        self.window = window
        # center the window on the screen with any screen responsive
        width_of_window = 400
        height_of_window = 500
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x_coordinate = (screen_width/2)-(width_of_window/2)
        y_coordinate = (screen_height/2)-(height_of_window/2)
        self.window.geometry("%dx%d+%d+%d" %(width_of_window,height_of_window,x_coordinate,y_coordinate))
        self.window.configure(bg='#040405')

        self.window.resizable(0, 0)
        self.window.title('تسجيل الدخول')
        self.window.iconbitmap("images\\egypt_studio_logo.ico")

        # ====== Login Frame =========================
        self.lgn_frame = Frame(self.window, bg='#040405', width=400, height=500)
        self.lgn_frame.pack()
        with open('credentials.json', 'r') as f:
            credentials = json.load(f)
        # ======= عنوان الترحيب =======================
        self.txt = "مرحبا" + " "+ credentials['username']
        self.heading = Label(self.lgn_frame, text=self.txt, font=('yu gothic ui', 20, "bold"), bg="#040405", fg='white')
        self.heading.place(x=120, y=30)

        # ========== حقل اسم المستخدم =================
        self.username_label = Label(self.lgn_frame, text="المستخدم إسم ", bg="#040405", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.username_label.place(x=50, y=150)

        self.username_entry = Entry(self.lgn_frame, bg="#333333", fg="white", font=("yu gothic ui", 12, "bold"))
        self.username_entry.place(x=50, y=180, width=300)

        # ========== حقل كلمة المرور ===================
        self.password_label = Label(self.lgn_frame, text="المرور كلمة", bg="#040405", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.password_label.place(x=50, y=230)

        self.password_entry = Entry(self.lgn_frame, bg="#333333", fg="white", font=("yu gothic ui", 12, "bold"), show="*")
        self.password_entry.place(x=50, y=260, width=300)

        # ========== زر تسجيل الدخول ===================
        self.login_button = Button(self.lgn_frame, text='دخول', font=("yu gothic ui", 13, "bold"), bg='#3047ff',
                                   fg='white', command=self.validate_login)
        self.login_button.place(x=140, y=320, width=120)

    def validate_login(self):
        # تحميل بيانات تسجيل الدخول من ملف JSON
        with open('credentials.json', 'r') as f:
            credentials = json.load(f)

        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == credentials['username'] and password == credentials['password']:
            self.window.destroy()  # إغلاق نافذة تسجيل الدخول
            mainpage()  # فتح الصفحة الرئيسية
        else:
            self.show_error()

    def show_error(self):
        # عرض رسالة خطأ إذا كانت بيانات الدخول غير صحيحة
        error_label = Label(self.lgn_frame, text="خطأ في بيانات الدخول", bg="#040405", fg="red",
                            font=("yu gothic ui", 10, "bold"))
        error_label.place(x=100, y=360)

class UpdateCredentials:
    def __init__(self, window):
        self.window = window
        self.window.geometry('400x300+500+200')
        self.window.title('الصفحة الشخصيه')
        self.window.iconbitmap("images\\egypt_studio_logo.ico")
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        # ====== Frame =========================
        self.frame = Frame(self.window, bg='#040405', width=400, height=300)
        self.frame.pack()

        # ======= عنوان النافذة =======================
        self.heading = Label(self.frame, text="المعلومات تحديث", font=('yu gothic ui', 15, "bold"),
                             bg="#040405", fg='white')
        self.heading.place(x=80, y=20)

        # ======= حقل اسم المستخدم الجديد =============
        self.username_label = Label(self.frame, text=" الإسم", bg="#040405", fg="#4f4e4d",
                                    font=("yu gothic ui", 12, "bold"))
        self.username_label.place(x=50, y=80)

        self.username_entry = Entry(self.frame, bg="#333333", fg="white", font=("yu gothic ui", 12, "bold"))
        self.username_entry.place(x=50, y=110, width=300)

        # ======= حقل كلمة المرور الجديدة =============
        self.password_label = Label(self.frame, text="المرور كلمة ", bg="#040405", fg="#4f4e4d",
                                    font=("yu gothic ui", 12, "bold"))
        self.password_label.place(x=50, y=150)

        self.password_entry = Entry(self.frame, bg="#333333", fg="white", font=("yu gothic ui", 12, "bold"), show="*")
        self.password_entry.place(x=50, y=180, width=300)

        # ======= زر التحديث ===========================
        self.update_button = Button(self.frame, text='تحديث', font=("yu gothic ui", 13, "bold"), bg='#3047ff',
                                    fg='white', command=self.update_credentials)
        self.update_button.place(x=140, y=230, width=120)

    def on_close(self):
        """إجراء عند إغلاق النافذة يدويًا."""
        global updatemenuisopen
        updatemenuisopen = False  # تغيير الحالة إلى False
        self.window.destroy()  # إغلاق النافذة
    def update_credentials(self):
        # قراءة البيانات الجديدة
        new_username = self.username_entry.get()
        new_password = self.password_entry.get()

        if new_username and new_password:
            # تحديث ملف JSON بالمعلومات الجديدة
            credentials = {
                "username": new_username,
                "password": new_password
            }

            with open('credentials.json', 'w') as f:
                json.dump(credentials, f, indent=4)

            messagebox.showinfo("Success", "تم تحديث المعلومات بنجاح")
            global updatemenuisopen
            updatemenuisopen = False
            self.window.destroy()  # إغلاق نافذة التحديث
        else:
            messagebox.showerror("Error", "يجب ملئ جميع الحقول")


def open_update_page():
    global updatemenuisopen
    if updatemenuisopen == False:
        updatemenuisopen = True
        update_window = Tk()
        UpdateCredentials(update_window)
        update_window.mainloop()
    else:
     messagebox.showerror("Error", "انت بالفعل في صفحة الصفحة الشخصيه")

def page():
    window = Tk()
    LoginPage(window)
    window.mainloop()



def mainpage():
    root = tk.Tk()
    menu = CreateMenu(root)
    # open full size window
    root.state('zoomed')
    menu.add_title('القائمة الرئيسية')

    # تشغيل عرض المخزن تلقائيًا عند فتح الصفحة
    storageDisplay(root)

    # إضافة القوائم بدون الأزرار
    menu.add_menu('المخزن', [('جديد', lambda: addStorageView(root)), ('عرض', lambda: storageDisplay(root)), ('الأنواع', lambda: typesDisplay(root))])
    menu.add_menucommand('رصيد السيارة', lambda: displayWallet(root))
    menu.add_menucommand('المرتجعات', lambda: ShowReturns(root))
    menu.add_menucommand('تغيير معلومات الدخول', lambda: open_update_page())
    menu.add_menu('المديونية', [('جديد', lambda: add_indebtedness(root)), ('عرض', lambda: Showindebtedness(root))])
    menu.add_menucommand('خروج',  root.quit)

    # إعداد الأيقونة والخصائص الأساسية
    root.iconbitmap("images\\egypt_studio_logo.ico")

    # تشغيل الحلقة الرئيسية للواجهة
    root.mainloop()


if __name__ == '__main__':
    w=Tk()

width_of_window = 427
height_of_window = 250
screen_width = w.winfo_screenwidth()
screen_height = w.winfo_screenheight()
x_coordinate = (screen_width/2)-(width_of_window/2)
y_coordinate = (screen_height/2)-(height_of_window/2)
w.geometry("%dx%d+%d+%d" %(width_of_window,height_of_window,x_coordinate,y_coordinate))

w.overrideredirect(1) 


Frame(w, width=427, height=250, bg='#272727').place(x=0,y=0)
label1=Label(w, text='تمت برمجة المشروع بواسطه محمود يوسف \n \n تم تصميم المشروع بواسطه أحمد يوسف \n \n https://egypt-studio.com', fg='white', bg='#272727') #decorate it 
label1.configure(font=("Egypt Studio", 11, "bold"))   #You need to install this font in your PC or try another one
label1.place(x=80,y=60)

label2=Label(w, text='جاري التحميل...', fg='white', bg='#272727') #decorate it 
label2.configure(font=("Calibri", 11))
label2.place(x=10,y=215)


image_a=ImageTk.PhotoImage(Image.open('c2.png'))
image_b=ImageTk.PhotoImage(Image.open('c1.png'))




for i in range(5):
    topplace = 190
    l1=Label(w, image=image_a, border=0, relief=SUNKEN).place(x=180, y=topplace)
    l2=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=200, y=topplace)
    l3=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=220, y=topplace)
    l4=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=240, y=topplace)
    w.update_idletasks()
    time.sleep(0.2)

    l1=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=180, y=topplace)
    l2=Label(w, image=image_a, border=0, relief=SUNKEN).place(x=200, y=topplace)
    l3=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=220, y=topplace)
    l4=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=240, y=topplace)
    w.update_idletasks()
    time.sleep(0.2)

    l1=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=180, y=topplace)
    l2=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=200, y=topplace)
    l3=Label(w, image=image_a, border=0, relief=SUNKEN).place(x=220, y=topplace)
    l4=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=240, y=topplace)
    w.update_idletasks()
    time.sleep(0.2)

    l1=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=180, y=topplace)
    l2=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=200, y=topplace)
    l3=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=220, y=topplace)
    l4=Label(w, image=image_a, border=0, relief=SUNKEN).place(x=240, y=topplace)
    w.update_idletasks()
    time.sleep(0.2)


w.destroy()
page()


   
