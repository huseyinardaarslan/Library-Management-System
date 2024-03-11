import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
import sqlite3
from PIL import Image, ImageTk
from lang import I18N

class BookManagement(tk.Toplevel):
    def __init__(self, parent, language):
        super().__init__()
        self.i18n = I18N(language)
        self.title(self.i18n.book_management)
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
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            publication_year INTEGER,
            is_borrowed INTEGER DEFAULT 0
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
            msg.showerror(self.i18n.error, f"{self.i18n.database_error}: {str(e)}")

    def create_widgets(self):
        text_color = "antique white"

        header_label = ttk.Label(self, text=self.i18n.book_management, font=("Helvetica", 16, "bold"), foreground=text_color)
        header_label.pack(pady=10)

        add_button = ttk.Button(self, text=self.i18n.add_book, command=self.add_book_window, style="DarkGold.TButton")
        remove_button = ttk.Button(self, text=self.i18n.remove_book, command=self.remove_book_window, style="DarkGold.TButton")

        add_button.pack(pady=10)
        remove_button.pack(pady=10)

        self.tree = ttk.Treeview(self, columns=("ID", "Title", "Author", "Publication Year", "Borrowed"), show="headings", height=10)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Title", text=self.i18n.book_title)
        self.tree.heading("Author", text=self.i18n.author)
        self.tree.heading("Publication Year", text=self.i18n.publication_year)
        self.tree.heading("Borrowed", text=self.i18n.borrowed)

        self.tree.pack(pady=10)


    def add_book_window(self):
        add_window = tk.Toplevel(self)
        add_window.title(self.i18n.add_book)
        add_window.geometry("370x200+500+250")

        title_label = ttk.Label(add_window, text=self.i18n.book_title, foreground="black")
        title_entry = ttk.Entry(add_window)

        author_label = ttk.Label(add_window, text=self.i18n.author, foreground="black")
        author_entry = ttk.Entry(add_window)

        year_label = ttk.Label(add_window, text=self.i18n.publication_year, foreground="black")
        year_entry = ttk.Entry(add_window)

        add_button = ttk.Button(add_window, text=self.i18n.add_book, command=lambda: self.add_book(title_entry.get(), author_entry.get(), year_entry.get(), add_window))

        title_label.grid(row=0, column=0, padx=10, pady=10)
        title_entry.grid(row=0, column=1, padx=10, pady=10)
        author_label.grid(row=1, column=0, padx=10, pady=10)
        author_entry.grid(row=1, column=1, padx=10, pady=10)
        year_label.grid(row=2, column=0, padx=10, pady=10)
        year_entry.grid(row=2, column=1, padx=10, pady=10)
        add_button.grid(row=3, column=0, columnspan=2, pady=10)

    def remove_book_window(self):
        remove_window = tk.Toplevel(self)
        remove_window.title(self.i18n.remove_book)
        remove_window.geometry("300x110+550+250")

        title_label = ttk.Label(remove_window, text=self.i18n.book_title, foreground="black")
        title_entry = ttk.Entry(remove_window)

        remove_button = ttk.Button(remove_window, text=self.i18n.remove_book, command=lambda: self.remove_book(title_entry.get(), remove_window))

        title_label.grid(row=0, column=0, padx=10, pady=10)
        title_entry.grid(row=0, column=1, padx=10, pady=10)
        remove_button.grid(row=1, column=0, columnspan=2, pady=10)

    def add_book(self, title, author, year, add_window):
        if not all((title, author, year.isdigit())):
            msg.showerror(self.i18n.error, self.i18n.fill_all_fields)
            return

        query = "INSERT INTO books (title, author, publication_year) VALUES (?, ?, ?);"
        self.execute_query(query, (title, author, year))

        msg.showinfo(self.i18n.success, self.i18n.book_added)
        self.populate_treeview()
        add_window.destroy()

    def remove_book(self, title, remove_window):
        if not title:
            msg.showerror(self.i18n.error, self.i18n.enter_title_to_remove)
            return

        query = "DELETE FROM books WHERE title = ?;"
        self.execute_query(query, (title,))

        msg.showinfo(self.i18n.success, self.i18n.book_removed)
        self.populate_treeview()
        remove_window.destroy()

    def populate_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        query = "SELECT * FROM books;"
        self.execute_query(query)
        books_data = self.cur.fetchall()

        for book in books_data:
            book_with_is_borrowed = book + (self.i18n.borrowed if book[4] else "",)
            self.tree.insert("", "end", values=book_with_is_borrowed)

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
