import tkinter as tk
from tkinter import ttk, messagebox
from mainwindow import MainWindow
from lang import I18N
import sqlite3

class LoginWindow:
    def __init__(self, language="en"):
        self.i18n = I18N(language)
        self.win = tk.Tk()
        self.window_title = self.i18n.title
        self.win.geometry("800x800+310+0")
        self.win.title(self.window_title)

        self.background_image = tk.PhotoImage(file="libsys1.gif")
        background_label = tk.Label(self.win, image=self.background_image)
        background_label.place(relwidth=1, relheight=1)

        login_frame = ttk.Frame(self.win, borderwidth=3, relief="ridge")
        login_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.open_connection()
        self.create_table()
        self.create_widgets(login_frame)

    def open_connection(self):
        self.conn = sqlite3.connect("library.db")
        self.cur = self.conn.cursor()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            contact TEXT
        )
        """
        self.cur.execute(query)
        self.conn.commit()

    def create_widgets(self, frame):
        text_color = "antique white"

        self.header_label = ttk.Label(frame, text=self.i18n.header, font=("Helvetica", 16, "bold"), foreground=text_color)

        self.username_label = ttk.Label(frame, text=self.i18n.username, foreground=text_color)
        self.username_entry = ttk.Entry(frame)

        self.password_label = ttk.Label(frame, text=self.i18n.password, foreground=text_color)
        self.password_entry = ttk.Entry(frame, show="*")

        self.login_button = ttk.Button(frame, text=self.i18n.login, command=self.login, style="DarkGold.TButton")
        self.register_button = ttk.Button(frame, text=self.i18n.register, command=self.show_register_window, style="DarkGold.TButton")

        self.english_button = ttk.Button(frame, text="English", command=lambda: self.change_language("en"), style="DarkGold.TButton")
        self.turkish_button = ttk.Button(frame, text="Türkçe", command=lambda: self.change_language("tr"), style="DarkGold.TButton")

        self.win.bind("<Return>", self.login)

        self.header_label.grid(row=0, column=0, columnspan=2, pady=10)
        self.username_label.grid(row=1, column=0, padx=10, pady=10)
        self.username_entry.grid(row=1, column=1, padx=10, pady=10)
        self.password_label.grid(row=2, column=0, padx=10, pady=10)
        self.password_entry.grid(row=2, column=1, columnspan=2, padx=10, pady=10)
        self.login_button.grid(row=3, column=0, columnspan=2, pady=10, sticky='ew')
        self.register_button.grid(row=4, column=0, columnspan=2, sticky='ew')
        self.english_button.grid(row=5, column=0, columnspan=2, pady=(10,5))
        self.turkish_button.grid(row=6, column=0, columnspan=2, pady=(0,10))

        self.win.style = ttk.Style()
        self.win.style.configure("DarkGold.TButton", foreground=text_color)

    def login(self, event=None):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.is_registered(username, password):
            self.open_main_window()
            messagebox.showinfo(self.i18n.login_successful, f"{self.i18n.welcome}, {username}!")
            self.win.destroy()
        else:
            messagebox.showerror(self.i18n.login_failed, self.i18n.invalid_credentials)

    def is_registered(self, username, password):
        query = "SELECT * FROM users WHERE username=? AND password=?"
        result = self.conn.execute(query, (username, password)).fetchone()
        return result is not None

    def show_register_window(self):
        register_window = RegisterWindow(self.win, self.conn, self.i18n)
        self.win.wait_window(register_window.top)

    def open_main_window(self):
        self.win.withdraw()
        self.main_window = MainWindow(parent=self, language=self.i18n.language)
        self.main_window.grab_set()
        self.main_window.mainloop()

    def change_language(self, selected_language):
        try:
            self.i18n = I18N(selected_language)
        except NotImplementedError as e:
            messagebox.showerror("Error", str(e))
            return

        self.update_labels()

    def update_labels(self):
        self.window_title = self.i18n.title
        self.win.title(self.window_title)
        self.header_label.config(text=self.i18n.header)
        self.username_label.config(text=self.i18n.username)
        self.password_label.config(text=self.i18n.password)
        self.login_button.config(text=self.i18n.login)
        self.register_button.config(text=self.i18n.register)


class RegisterWindow:
    def __init__(self, parent, conn, i18n):
        self.top = tk.Toplevel(parent)
        self.top.title(i18n.register)
        self.top.geometry("360x305+550+250")

        self.conn = conn
        self.i18n = i18n
        self.create_widgets()

    def create_widgets(self):
        text_color = "antique white"

        header_label = ttk.Label(self.top, text=self.i18n.register, font=("Helvetica", 16, "bold"), foreground=text_color)
        header_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.fullname_label = ttk.Label(self.top, text=self.i18n.fullname, foreground=text_color)
        self.fullname_entry = ttk.Entry(self.top)

        self.new_username_label = ttk.Label(self.top, text=self.i18n.new_username, foreground=text_color)
        self.new_username_entry = ttk.Entry(self.top)

        self.new_password_label = ttk.Label(self.top, text=self.i18n.new_password, foreground=text_color)
        self.new_password_entry = ttk.Entry(self.top, show="*")

        self.contact_label = ttk.Label(self.top, text=self.i18n.contact, foreground=text_color)
        self.contact_entry = ttk.Entry(self.top)

        self.register_button = ttk.Button(self.top, text=self.i18n.register, command=self.register_user, style="DarkGold.TButton")

        self.fullname_label.grid(row=1, column=0, padx=10, pady=10)
        self.fullname_entry.grid(row=1, column=1, padx=10, pady=10)
        self.new_username_label.grid(row=2, column=0, padx=10, pady=10)
        self.new_username_entry.grid(row=2, column=1, padx=10, pady=10)
        self.new_password_label.grid(row=3, column=0, padx=10, pady=10)
        self.new_password_entry.grid(row=3, column=1, padx=10, pady=10)
        self.contact_label.grid(row=4, column=0, padx=10, pady=10)
        self.contact_entry.grid(row=4, column=1, padx=10, pady=10)
        self.register_button.grid(row=5, column=0, columnspan=2, pady=10)

        self.top.style = ttk.Style()
        self.top.style.configure("DarkGold.TButton", foreground=text_color)

    def register_user(self):
        fullname = self.fullname_entry.get()
        new_username = self.new_username_entry.get()
        new_password = self.new_password_entry.get()
        contact_number = self.contact_entry.get()


        if self.is_username_taken(new_username):
            messagebox.showerror(self.i18n.registration_failed, self.i18n.username_taken)
        else:
            query = "INSERT INTO users (fullname, username, password, contact) VALUES (?, ?, ?, ?)"
            self.conn.execute(query, (fullname, new_username, new_password, contact_number))
            self.conn.commit()
            messagebox.showinfo(self.i18n.registration_successful, self.i18n.user_registered)
            self.top.destroy()

    def is_username_taken(self, username):
        query = "SELECT * FROM users WHERE username=?"
        result = self.conn.execute(query, (username,)).fetchone()
        return result is not None

app = LoginWindow()
app.win.mainloop()
