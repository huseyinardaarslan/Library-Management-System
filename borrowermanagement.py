import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
import sqlite3
from PIL import Image, ImageTk
from lang import I18N

class BorrowerManagement(tk.Toplevel):
    def __init__(self, parent, language):
        super().__init__()
        self.i18n = I18N(language)
        self.title(self.i18n.borrower_management)
        self.geometry("1000x500+210+180")
        self.parent = parent
        self.protocol("WM_DELETE_WINDOW", self.close_window)

        self.conn = None
        self.cur = None

        background_image = Image.open("libsys1.gif")
        background_photo = ImageTk.PhotoImage(background_image)

        background_label = tk.Label(self, image=background_photo)
        background_label.place(relwidth=1, relheight=1)
        background_label.image = background_photo

        self.create_table()
        self.create_widgets()
        self.populate_treeview()

    def create_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS borrowers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            surname TEXT,
            contact_number TEXT
        );
        '''
        self.execute_query(query)

    def execute_query(self, query, parameters=()):
        try:
            if not self.conn:
                self.open_connection()

            self.cur.execute(query, parameters)
            self.conn.commit()
        except Exception as e:
            msg.showerror(self.i18n.error, f"{self.i18n.db_error}: {str(e)}")

    def create_widgets(self):
        text_color = "antique white"

        header_label = ttk.Label(self, text=self.i18n.borrower_management, font=("Helvetica", 16, "bold"), foreground=text_color)
        header_label.pack(pady=10)

        add_button = ttk.Button(self, text=self.i18n.add_borrower, command=self.add_borrower_window, style="DarkGold.TButton")
        remove_button = ttk.Button(self, text=self.i18n.remove_borrower, command=self.remove_borrower_window,
                                   style="DarkGold.TButton")

        add_button.pack(pady=10)
        remove_button.pack(pady=10)


        self.tree = ttk.Treeview(self, columns=("ID", self.i18n.name, self.i18n.surname, self.i18n.contact_number), show="headings", height=10)
        self.tree.heading("ID", text="ID")
        self.tree.heading(self.i18n.name, text=self.i18n.name)
        self.tree.heading(self.i18n.surname, text=self.i18n.surname)
        self.tree.heading(self.i18n.contact_number, text=self.i18n.contact_number)

        self.tree.pack(pady=10)

    def add_borrower_window(self):
        add_window = tk.Toplevel(self)
        add_window.title(self.i18n.add_borrower)
        add_window.geometry("350x200+550+250")

        name_label = ttk.Label(add_window, text=self.i18n.name + ":", foreground="black")
        name_entry = ttk.Entry(add_window)

        surname_label = ttk.Label(add_window, text=self.i18n.surname + ":", foreground="black")
        surname_entry = ttk.Entry(add_window)

        contact_label = ttk.Label(add_window, text=self.i18n.contact_number + ":", foreground="black")
        contact_entry = ttk.Entry(add_window)

        add_button = ttk.Button(add_window, text=self.i18n.add_borrower, command=lambda: self.add_borrower(name_entry.get(), surname_entry.get(), contact_entry.get(), add_window))

        name_label.grid(row=0, column=0, padx=10, pady=10)
        name_entry.grid(row=0, column=1, padx=10, pady=10)
        surname_label.grid(row=1, column=0, padx=10, pady=10)
        surname_entry.grid(row=1, column=1, padx=10, pady=10)
        contact_label.grid(row=2, column=0, padx=10, pady=10)
        contact_entry.grid(row=2, column=1, padx=10, pady=10)
        add_button.grid(row=3, column=0, columnspan=2, pady=10)

    def remove_borrower_window(self):
        remove_window = tk.Toplevel(self)
        remove_window.title(self.i18n.remove_borrower)
        remove_window.geometry("300x150+550+250")

        name_label = ttk.Label(remove_window, text=self.i18n.name + ":", foreground="black")
        name_entry = ttk.Entry(remove_window)

        surname_label = ttk.Label(remove_window, text=self.i18n.surname + ":", foreground="black")
        surname_entry = ttk.Entry(remove_window)

        remove_button = ttk.Button(remove_window, text=self.i18n.remove_borrower, command=lambda: self.remove_borrower(name_entry.get(), surname_entry.get(), remove_window))

        name_label.grid(row=0, column=0, padx=10, pady=10)
        name_entry.grid(row=0, column=1, padx=10, pady=10)
        surname_label.grid(row=1, column=0, padx=10, pady=10)
        surname_entry.grid(row=1, column=1, padx=10, pady=10)
        remove_button.grid(row=2, column=0, columnspan=2, pady=10)

    def add_borrower(self, name, surname, contact, add_window):
        if not all((name, surname, contact)):
            msg.showerror(self.i18n.error, self.i18n.fill_all_fields)
            return

        query = "INSERT INTO borrowers (name, surname, contact_number) VALUES (?, ?, ?);"
        self.execute_query(query, (name, surname, contact))

        msg.showinfo(self.i18n.success, self.i18n.borrower_added)
        add_window.destroy()
        self.populate_treeview()

    def remove_borrower(self, name, surname, remove_window):
        if not name or not surname:
            msg.showerror(self.i18n.error, self.i18n.enter_name_surname)
            return

        query = "DELETE FROM borrowers WHERE name = ? AND surname = ?;"
        self.execute_query(query, (name, surname))

        msg.showinfo(self.i18n.success, self.i18n.borrower_removed)
        remove_window.destroy()
        self.populate_treeview()

    def populate_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        query = "SELECT * FROM borrowers;"
        self.execute_query(query)
        borrowers_data = self.cur.fetchall()

        for borrower in borrowers_data:
            self.tree.insert("", "end", values=borrower)

    def open_connection(self):
        self.conn = sqlite3.connect("library.db")
        self.cur = self.conn.cursor()

    def close_connection(self):
        if self.conn:
            self.conn.close()
            self.cur = None
            self.conn = None

    def close_window(self):
        self.close_connection()
        self.destroy()
