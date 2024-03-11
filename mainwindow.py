import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from bookmanagement import BookManagement
from borrowermanagement import BorrowerManagement
from transaction import Transaction
from lang import I18N

class MainWindow(tk.Toplevel):
    def __init__(self, parent, language):
        super().__init__()
        self.win = parent
        self.i18n = I18N(language)
        self.title(self.i18n.main_window_title)
        self.geometry("800x800+310+0")

        background_image = Image.open("libsys1.gif")
        background_photo = ImageTk.PhotoImage(background_image)

        background_label = tk.Label(self, image=background_photo)
        background_label.place(relwidth=1, relheight=1)
        background_label.image = background_photo

        button_frame = ttk.Frame(self, style="Menu.TFrame")
        button_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.style = ttk.Style()
        self.style.configure("Menu.TFrame", background="#2E4053")

        menu_font = ("Helvetica", 20, "bold")
        button_font = ("Helvetica", 14, "bold")

        menu_label = tk.Label(button_frame, text=self.i18n.menu_label, font=menu_font, foreground="#FAEBD7", background="#2E4053")
        menu_label.grid(row=0, column=0, pady=10, padx=20, columnspan=2)

        self.book_management_button = ttk.Button(button_frame, text=self.i18n.book_management, command=self.open_book_management, style="Button.TButton")
        self.borrower_management_button = ttk.Button(button_frame, text=self.i18n.borrower_management, command=self.open_borrower_management, style="Button.TButton")
        self.transaction_button = ttk.Button(button_frame, text=self.i18n.transaction, command=self.open_transaction, style="Button.TButton")
        self.exit_button = ttk.Button(button_frame, text=self.i18n.exit, command=self.close_window, style="Button.TButton")

        self.style.configure("Button.TButton", font=button_font, padding=(15, 10), background="#3498DB", foreground="#FAEBD7")

        self.book_management_button.grid(row=1, column=0, pady=10, padx=20, sticky="ew")
        self.borrower_management_button.grid(row=2, column=0, pady=10, padx=20, sticky="ew")
        self.transaction_button.grid(row=3, column=0, pady=10, padx=20, sticky="ew")
        self.exit_button.grid(row=4, column=0, pady=10, padx=20, sticky="ew")

        self.mainloop()

    def open_book_management(self):
        book_management_window = BookManagement(self.win, language=self.i18n.language)

    def open_borrower_management(self):
        borrower_management_window = BorrowerManagement(self.win, language=self.i18n.language)

    def open_transaction(self):
        transaction = Transaction(self, language=self.i18n.language)

    def close_window(self):
        self.destroy()
