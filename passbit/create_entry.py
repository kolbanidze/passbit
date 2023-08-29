from customtkinter import *
from uuid import uuid4
from .pb_crypto import PBCrypto
from .language import CreateEntryPy
from binascii import Error as TOTP_Base32_Error
from pyotp import TOTP
from CTkMessagebox import CTkMessagebox


class CreateEntry(CTkToplevel):
    def __init__(self, master_key, db, c, self_update_entries) -> None:
        super().__init__()
        self.lang = CreateEntryPy()
        self.master_key = master_key
        self.db = db
        self.c = c
        self.self_update_entries = self_update_entries

        self.title(self.lang.title)
        self.columnconfigure(0, weight=2)

        name_label = CTkLabel(self, text=self.lang.name_label)
        self.name_entry = CTkEntry(self)
        name_label.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        self.name_entry.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        description_label = CTkLabel(self, text=self.lang.description_label)
        self.description_entry = CTkEntry(self)
        description_label.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")
        self.description_entry.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")

        login_label = CTkLabel(self, text=self.lang.login_label)
        self.login_entry = CTkEntry(self)
        login_label.grid(row=4, column=0, padx=10, pady=5, sticky="nsew")
        self.login_entry.grid(row=5, column=0, padx=10, pady=5, sticky="nsew")

        password_label = CTkLabel(self, text=self.lang.password_label)
        self.password_entry = CTkEntry(self, show='*')
        password_label.grid(row=6, column=0, padx=10, pady=5, sticky="nsew")
        self.password_entry.grid(row=7, column=0, padx=10, pady=5, sticky="nsew")

        self.reveal_var = StringVar()
        password_reveal_checkbox = CTkCheckBox(self, text=self.lang.reveal_password, onvalue=True,
                                               offvalue=False,
                                               variable=self.reveal_var,
                                               command=lambda: self.reveal_password())
        password_reveal_checkbox.grid(row=8, column=0, sticky="nsew", padx=15, pady=10)

        self.is_totp_status = StringVar(value='n')
        self.is_totp_switch = CTkSwitch(self, text="TOTP", variable=self.is_totp_status,
                                        onvalue='y', offvalue='n')
        self.is_totp_switch.grid(row=9, column=0, padx=10, pady=5, sticky="nsew")

        self.create_entry_btn = CTkButton(self, text=self.lang.create_entry,
                                          command=lambda: self.create_entry())
        self.create_entry_btn.grid(row=10, column=0, padx=10, pady=5, sticky="nsew")

    def create_entry(self):
        uuid = str(uuid4())
        name = self.name_entry.get().encode('utf-8')
        description = self.description_entry.get().encode('utf-8')
        login = self.login_entry.get().encode('utf-8')
        password = self.password_entry.get().encode('utf-8')
        is_totp = self.is_totp_status.get().encode('utf-8')

        # TOTP validation
        if self.is_totp_status.get() == 'y':
            try:
                TOTP(self.password_entry.get()).now()
            except TOTP_Base32_Error:
                msg = CTkMessagebox(icon="warning",
                                    title=self.lang.msg_warning_title,
                                    message=self.lang.msg_warning_message)
                # Waiting until user will press button
                msg.get()
                # Stopping function execution
                return

        encrypted_entry = PBCrypto.encrypt_by_dict(self.master_key,
                                                   {'uuid': uuid,
                                                    'name': name,
                                                    'description': description,
                                                    'login': login,
                                                    'password': password,
                                                    'is_totp': is_totp})
        self.c.execute("INSERT INTO db_storage (uuid, name, description,"
                       "                        login, password, is_totp) VALUES ("
                       "?, ?, ?, ?, ?, ?)", (uuid,
                                             encrypted_entry['name'],
                                             encrypted_entry['description'],
                                             encrypted_entry['login'],
                                             encrypted_entry['password'],
                                             encrypted_entry['is_totp']))
        self.db.commit()
        self.destroy()
        self.self_update_entries()

    def reveal_password(self) -> None:
        """Handles 'Reveal password' checkbox"""
        state = self.reveal_var.get()
        if state == "0":
            self.password_entry.configure(show='*')
        else:
            self.password_entry.configure(show='')
