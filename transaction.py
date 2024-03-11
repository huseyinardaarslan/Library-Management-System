import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
import sqlite3
from PIL import Image, ImageTk
from datetime import datetime
from lang import I18N

class Transaction(tk.Toplevel):
    def __init__(self, parent, language):
        super().__init__()
        self.i18n = I18N(language)
        self.title(self.i18n.transaction_management)
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
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            borrower_id INTEGER,
            borrow_date DATE,
            return_date DATE,
            FOREIGN KEY (book_id) REFERENCES books (id),
            FOREIGN KEY (borrower_id) REFERENCES borrowers (id)
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

        header_label = ttk.Label(self, text=self.i18n.transaction_management, font=("Helvetica", 16, "bold"), foreground=text_color)
        header_label.pack(pady=10)

        borrow_button = ttk.Button(self, text=self.i18n.borrow_book, command=self.borrow_book_window, style="DarkGold.TButton")
        return_button = ttk.Button(self, text=self.i18n.return_book, command=self.return_book_window, style="DarkGold.TButton")

        borrow_button.pack(pady=10)
        return_button.pack(pady=10)

        self.tree = ttk.Treeview(self, columns=("ID", self.i18n.book_title, self.i18n.borrower_name, self.i18n.borrow_date, self.i18n.return_date), show="headings", height=10)
        self.tree.heading("ID", text="ID")
        self.tree.heading(self.i18n.book_title, text=self.i18n.book_title)
        self.tree.heading(self.i18n.borrower_name, text=self.i18n.borrower_name)
        self.tree.heading(self.i18n.borrow_date, text=self.i18n.borrow_date)
        self.tree.heading(self.i18n.return_date, text=self.i18n.return_date)
        self.tree.pack(pady=10)

    def borrow_book_window(self):
        borrow_window = tk.Toplevel(self)
        borrow_window.title(self.i18n.borrow_book)
        borrow_window.geometry("400x200+480+250")

        title_label = ttk.Label(borrow_window, text=self.i18n.book_title + ":", foreground="black")
        title_entry = ttk.Entry(borrow_window)

        borrower_label = ttk.Label(borrow_window, text=self.i18n.borrower_name + ":", foreground="black")
        borrower_entry = ttk.Entry(borrow_window)

        borrow_date_label = ttk.Label(borrow_window, text=self.i18n.borrow_date + ":", foreground="black")
        borrow_date_entry = ttk.Entry(borrow_window)

        borrow_button = ttk.Button(borrow_window, text=self.i18n.borrow_book, command=lambda: self.borrow_book(title_entry.get(), borrower_entry.get(), borrow_date_entry.get(), borrow_window))

        title_label.grid(row=0, column=0, padx=10, pady=10)
        title_entry.grid(row=0, column=1, padx=10, pady=10)
        borrower_label.grid(row=1, column=0, padx=10, pady=10)
        borrower_entry.grid(row=1, column=1, padx=10, pady=10)
        borrow_date_label.grid(row=2, column=0, padx=10, pady=10)
        borrow_date_entry.grid(row=2, column=1, padx=10, pady=10)
        borrow_button.grid(row=3, column=0, columnspan=2, pady=10)

    def return_book_window(self):
        return_window = tk.Toplevel(self)
        return_window.title(self.i18n.return_book)
        return_window.geometry("320x130+550+250")

        title_label = ttk.Label(return_window, text=self.i18n.book_title + ":", foreground="black")
        title_entry = ttk.Entry(return_window)

        return_button = ttk.Button(return_window, text=self.i18n.return_book, command=lambda: self.return_book(title_entry.get(), return_window))

        title_label.grid(row=0, column=0, padx=10, pady=10)
        title_entry.grid(row=0, column=1, padx=10, pady=10)
        return_button.grid(row=1, column=0, columnspan=2, pady=10)

    def borrow_book(self, title, borrower, borrow_date, borrow_window):
        if not all((title, borrower, borrow_date)):
            msg.showerror(self.i18n.error, self.i18n.fill_all_fields)
            return

        book_id = self.get_book_id(title)
        if not book_id:
            msg.showerror(self.i18n.error, self.i18n.book_not_found)
            return

        if self.is_book_borrowed(book_id):
            msg.showerror(self.i18n.error, self.i18n.book_already_borrowed)
            return

        borrower_id = self.get_borrower_id(borrower)
        if not borrower_id:
            msg.showerror(self.i18n.error, self.i18n.borrower_not_found)
            return

        borrow_date_obj = self.convert_to_date(borrow_date)
        if not borrow_date_obj:
            msg.showerror(self.i18n.error, self.i18n.invalid_date_format)
            return

        query_update_book = "UPDATE books SET is_borrowed = 1 WHERE id = ?;"
        self.execute_query(query_update_book, (book_id,))

        query_insert_transaction = "INSERT INTO transactions (book_id, borrower_id, borrow_date) VALUES (?, ?, ?);"
        self.execute_query(query_insert_transaction, (book_id, borrower_id, borrow_date))

        msg.showinfo(self.i18n.success, self.i18n.book_borrowed)
        borrow_window.destroy()
        self.populate_treeview()

    def return_book(self, title, return_window):
        if not title:
            msg.showerror(self.i18n.error, self.i18n.enter_book_title)
            return

        book_id = self.get_book_id(title)
        if not book_id:
            msg.showerror(self.i18n.error, self.i18n.book_not_found)
            return

        if not self.is_book_borrowed(book_id):
            msg.showerror(self.i18n.error, self.i18n.book_not_borrowed)
            return

        query_update_book = "UPDATE books SET is_borrowed = 0 WHERE id = ?;"
        self.execute_query(query_update_book, (book_id,))

        query_update_transaction = "UPDATE transactions SET return_date = ? WHERE book_id = ? AND return_date IS NULL;"
        self.execute_query(query_update_transaction, (datetime.now().strftime("%Y-%m-%d"), book_id))

        msg.showinfo(self.i18n.success, self.i18n.book_returned)
        return_window.destroy()
        self.populate_treeview()

    def get_book_id(self, title):
        query = "SELECT id FROM books WHERE title = ?;"
        self.execute_query(query, (title,))
        result = self.cur.fetchone()
        return result[0] if result else None

    def is_book_borrowed(self, book_id):
        query = "SELECT is_borrowed FROM books WHERE id = ?;"
        self.execute_query(query, (book_id,))
        result = self.cur.fetchone()
        return result[0] if result else None

    def get_borrower_id(self, name):
        query = "SELECT id FROM borrowers WHERE name = ?;"
        self.execute_query(query, (name,))
        result = self.cur.fetchone()
        return result[0] if result else None

    def convert_to_date(self, date_str):
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return None

    def populate_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        query = '''
        SELECT transactions.id, books.title, borrowers.name, transactions.borrow_date, transactions.return_date
        FROM transactions
        JOIN books ON transactions.book_id = books.id
        JOIN borrowers ON transactions.borrower_id = borrowers.id;
        '''
        self.execute_query(query)
        transactions_data = self.cur.fetchall()

        for transaction in transactions_data:
            self.tree.insert("", "end", values=transaction)

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
