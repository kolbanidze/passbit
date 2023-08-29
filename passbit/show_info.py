import binascii
from CTkMessagebox import CTkMessagebox
from customtkinter import CTkToplevel, CTkLabel, CTkEntry, StringVar, CTkCheckBox, CTkButton
from pyperclip import copy as clipboard_copy
from threading import Thread
from pyotp import TOTP
from datetime import datetime
from time import sleep
from .language import ShowInfoPy
from tkinter import TclError


class ShowInfo(CTkToplevel):
    def __init__(self, entry_content: dict) -> None:
        """Shows ui and entry content"""
        super().__init__()
        self.lang = ShowInfoPy()
        self.entry_content = entry_content
        self.title(self.lang.title)
        self.resizable(False, False)

        uuid_label = CTkLabel(self, text="UUID")
        name_label = CTkLabel(self, text=self.lang.name)
        description_label = CTkLabel(self, text=self.lang.description)
        login_label = CTkLabel(self, text=self.lang.login)
        password_label = CTkLabel(self, text=self.lang.password)

        self.uuid_entry = CTkEntry(self)
        self.uuid_entry.insert(0, self.entry_content['uuid'])
        self.uuid_entry.configure(state="disabled")

        self.name_entry = CTkEntry(self)
        self.name_entry.insert(0, self.entry_content['name'])
        self.name_entry.configure(state='disabled')

        self.description_entry = CTkEntry(self)
        self.description_entry.insert(0, self.entry_content['description'])
        self.description_entry.configure(state='disabled')

        self.login_entry = CTkEntry(self)
        self.login_entry.insert(0, self.entry_content['login'])
        self.login_entry.configure(state='disabled')

        self.password_entry = CTkEntry(self, show='*')
        self.password_entry.insert(0, self.entry_content['password'])
        self.password_entry.configure(state='disabled')

        self.reveal_var = StringVar()
        password_reveal_checkbox = CTkCheckBox(self, text=self.lang.reveal_password,
                                               onvalue=True, offvalue=False,
                                               command=lambda: self.reveal_password(), variable=self.reveal_var)

        copy_uuid_btn = CTkButton(self, text=f"{self.lang.copy} UUID",
                                  command=lambda: self.copy_to_clipboard('uuid'))

        copy_name_btn = CTkButton(self, text=self.lang.copy_name,
                                  command=lambda: self.copy_to_clipboard('name'))
        copy_description_btn = CTkButton(self, text=self.lang.copy_description,
                                         command=lambda: self.copy_to_clipboard('description'))
        copy_login_btn = CTkButton(self, text=self.lang.copy_login,
                                   command=lambda: self.copy_to_clipboard('login'))
        copy_password_btn = CTkButton(self, text=self.lang.copy_password,
                                      command=lambda: self.copy_to_clipboard('password'))

        uuid_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.uuid_entry.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        name_label.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.name_entry.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        description_label.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.description_entry.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

        login_label.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        self.login_entry.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")

        password_label.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")
        self.password_entry.grid(row=4, column=1, padx=10, pady=10, sticky="nsew")

        copy_uuid_btn.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")
        copy_name_btn.grid(row=1, column=3, padx=10, pady=10, sticky="nsew")
        copy_description_btn.grid(row=2, column=3, padx=10, pady=10, sticky="nsew")
        copy_login_btn.grid(row=3, column=3, padx=10, pady=10, sticky="nsew")
        copy_password_btn.grid(row=4, column=3, padx=10, pady=10, sticky="nsew")

        password_reveal_checkbox.grid(row=5, column=1, padx=10, pady=10, sticky="nsew")

        if entry_content['is_totp'] == 'y':
            self.totp = TOTP(self.password_entry.get())

            is_totp_label = CTkLabel(self, text="TOTP")
            self.totp_entry = CTkEntry(self, state="disabled")
            copy_totp_btn = CTkButton(self, text=self.lang.copy_totp,
                                      command=lambda: clipboard_copy(self.totp_entry.get()))

            totp_thread = Thread(target=self.totp_handler)
            totp_thread.daemon = True
            is_totp_label.grid(row=6, column=0, padx=10, pady=10, sticky="nsew")
            self.totp_entry.grid(row=6, column=1, padx=10, pady=10, sticky="nsew")
            copy_totp_btn.grid(row=6, column=3, padx=10, pady=10, sticky="nsew")
            totp_thread.start()

    def reveal_password(self) -> None:
        """Handles 'Reveal password' checkbox"""
        state = self.reveal_var.get()
        if state == "0":
            self.password_entry.configure(show='*')
        else:
            self.password_entry.configure(show='')

    def copy_to_clipboard(self, string_to_copy: str) -> None:
        """Copies string to clipboard"""
        clipboard_copy(self.entry_content[string_to_copy])

    def totp_handler(self):
        while True:
            current_time = datetime.now()
            current_second_time = current_time.second

            # Calculate remaining seconds until the next 30-second interval
            remaining_seconds = 30 - (current_second_time % 30)

            try:
                self.totp_entry.configure(state="normal")
                self.totp_entry.insert(0, self.totp.now())
                self.totp_entry.configure(state="disabled")
            except TclError:
                # Stopping thread when window was closed, but thread is still working
                exit()
            except binascii.Error:
                print(self.lang.totp_error)
                exit()

            # Wait for the remaining seconds
            sleep(remaining_seconds)
            try:
                self.totp_entry.configure(state="normal")
                self.totp_entry.delete(0, 'end')
                self.totp_entry.configure(state="disabled")
            except TclError:
                # Stopping thread when window was closed, but thread is still working
                exit()
