from customtkinter import CTkToplevel, CTkLabel, CTkEntry, CTkButton, StringVar, CTkSwitch,\
    CTkCheckBox
from .pb_crypto import PBCrypto
from sqlite3 import Cursor, Connection
from .language import ModifyEntryPy


class ModifyEntry(CTkToplevel):
    def __init__(self,
                 entry: dict,
                 master_key: bytes,
                 update_list_function,
                 c: Cursor,
                 db: Connection):
        """Shows ui and inserts entry parameters"""
        super().__init__()
        self.lang = ModifyEntryPy()
        self.title(self.lang.title)
        self.master_key = master_key
        self.entry = entry
        self.c = c
        self.db = db
        self.update_list = update_list_function

        name_label = CTkLabel(self, text=self.lang.name)
        self.name_entry = CTkEntry(self)

        description_label = CTkLabel(self, text=self.lang.description)
        self.description_entry = CTkEntry(self)

        login_label = CTkLabel(self, text=self.lang.login)
        self.login_entry = CTkEntry(self)

        password_label = CTkLabel(self, text=self.lang.password)
        self.password_entry = CTkEntry(self, show='*')

        self.reveal_var = StringVar()
        password_reveal_checkbox = CTkCheckBox(self, text=self.lang.reveal_password, onvalue=True,
                                               offvalue=False,
                                               variable=self.reveal_var,
                                               command=lambda: self.reveal_password())

        save_btn = CTkButton(self,
                             text=self.lang.save,
                             command=lambda: self.save())

        self.name_entry.insert(0, entry['name'])
        self.description_entry.insert(0, entry['description'])
        self.login_entry.insert(0, entry['login'])
        self.password_entry.insert(0, entry['password'])

        name_label.grid(row=0, column=0, sticky="nsew", padx=20, pady=5)
        self.name_entry.grid(row=0, column=1, sticky="nsew", padx=20, pady=5)

        description_label.grid(row=1, column=0, sticky="nsew", padx=20, pady=5)
        self.description_entry.grid(row=1, column=1, sticky="nsew", padx=20, pady=5)

        login_label.grid(row=2, column=0, sticky="nsew", padx=20, pady=5)
        self.login_entry.grid(row=2, column=1, sticky="nsew", padx=20, pady=5)

        password_label.grid(row=3, column=0, sticky="nsew", padx=20, pady=5)
        self.password_entry.grid(row=3, column=1, sticky="nsew", padx=20, pady=5)

        password_reveal_checkbox.grid(row=4, column=1, sticky="nsew", padx=20, pady=5)

        self.is_totp_status = StringVar(value=entry['is_totp'])
        self.is_totp_switch = CTkSwitch(self, text="TOTP", variable=self.is_totp_status,
                                        onvalue='y', offvalue='n')
        self.is_totp_switch.grid(row=5, column=1, padx=20, pady=5, sticky="nsew")

        save_btn.grid(row=6, column=1, sticky="nsew", padx=20, pady=5)

    def save(self):
        """Updates entry parameters"""
        entry = PBCrypto.encrypt_by_dict(self.master_key, {
            'uuid': self.entry['uuid'],
            'name': self.name_entry.get(),
            'description': self.description_entry.get(),
            'login': self.login_entry.get(),
            'password': self.password_entry.get(),
            'is_totp': self.is_totp_status.get(),
        })
        self.c.execute("UPDATE db_storage SET "
                       "name=?,"
                       "description=?,"
                       "login=?,"
                       "password=?,"
                       "is_totp=? WHERE "
                       "uuid=?", (entry['name'], entry['description'], entry['login'], entry['password'],
                                  entry['is_totp'], entry['uuid']))
        self.db.commit()
        self.update_list()
        self.destroy()

    def reveal_password(self) -> None:
        """Handles 'Reveal password' checkbox"""
        state = self.reveal_var.get()
        if state == "0":
            self.password_entry.configure(show='*')
        else:
            self.password_entry.configure(show='')
