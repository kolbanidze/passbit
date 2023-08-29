from customtkinter import CTkToplevel, CTkButton, CTkLabel, CTkEntry,\
    CTkFrame, CTkScrollableFrame, CTkFont, StringVar, CTkCheckBox
from tkinter import filedialog
from sqlite3 import connect as sql_connect
from argon2.low_level import hash_secret_raw
from argon2 import Type
from Crypto.Cipher import AES
from functools import partial
from .create_entry import CreateEntry
from .modify_database import ModifyDatabase
from .pb_crypto import PBCrypto
from .show_info import ShowInfo
from .modify_entry import ModifyEntry
from .import_export_db import ImportExportDB
from .settings import DB_VIEWER_MIN_WIDTH, DB_VIEWER_MIN_HEIGHT, SHOW_UPDATE_BUTTON
from CTkMessagebox import CTkMessagebox
from .language import OpenDBPy
from os.path import basename
from pyperclip import copy as clipboard_copy


class OpenDB(CTkToplevel):
    def __init__(self) -> None:
        """Database viewer. Shows 'select db' menu. After opening (decrypting) database
        shows entries (right frame) and database-related buttons (left frame)"""
        super().__init__()
        self.lang = OpenDBPy()
        self.key_file_status = False

        self.title(self.lang.title)
        self.resizable(False, False)

        self.db_label = CTkLabel(self,
                                 text=f"{self.lang.db}: {self.lang.select_file_first}")
        self.db_label.pack(padx=20, pady=10)

        select_db_btn = CTkButton(self,
                                  text=self.lang.select_db_btn,
                                  command=lambda: self.select_db_handler())
        select_db_btn.pack(padx=20, pady=10)

        self.key_file_label = CTkLabel(self,
                                       text=f"{self.lang.keyfile_label_part_1}: {self.lang.select_file_first}")
        self.key_file_label.pack(padx=20, pady=10)

        key_file_button = CTkButton(self,
                                    text=self.lang.keyfile_btn,
                                    command=lambda: self.open_keyfile_filedialog())
        key_file_button.pack(padx=20, pady=10)

        enter_password_label = CTkLabel(self,
                                        text=self.lang.enter_password_label)
        enter_password_label.pack(padx=20, pady=10)

        self.password_entry = CTkEntry(self,
                                       state="disabled",
                                       show='*')
        self.password_entry.pack(padx=20, pady=10)

        self.reveal_var = StringVar()
        password_reveal_checkbox = CTkCheckBox(self, text=self.lang.reveal_password, onvalue=True,
                                               offvalue=False,
                                               variable=self.reveal_var,
                                               command=lambda: self.reveal_password())
        password_reveal_checkbox.pack(padx=20, pady=10)

        self.open_db_btn = CTkButton(self,
                                     state="disabled",
                                     text=self.lang.open_db_btn,
                                     command=lambda: self.open_db())
        self.open_db_btn.pack(padx=20, pady=10)

    def select_db_handler(self):
        db = filedialog.askopenfile()
        # Checking if db file was selected
        if locals()['db'] is not None:
            self.db_path = db.name

            self.password_entry.configure(state="normal")
            self.open_db_btn.configure(state="normal")
            self.db_label.configure(text=f"{self.lang.db}: {basename(self.db_path)}",
                                    font=CTkFont(underline=True))
        self.lift()

    def clear_all(self):
        msg = CTkMessagebox(title=self.lang.clear_all_msg_title,
                            message=self.lang.clear_all_msg_message,
                            icon="question",
                            option_1=self.lang.clear_all_option_1,
                            option_3=self.lang.clear_all_option_3)
        response = msg.get()

        if response == self.lang.clear_all_option_3:
            self.c.execute("DELETE FROM db_storage")
            self.db.commit()
            self.update_entries_list()

    def open_db(self):
        """Gets db header and decrypts master key"""

        self.db = sql_connect(self.db_path)
        self.c = self.db.cursor()
        self.c.execute("SELECT * FROM db_header")
        output = self.c.fetchall()[0]

        time_cost = output[3]
        memory_cost = output[4]
        parallelism = output[5]
        salt = output[6]
        encrypted_master_key = output[7]
        master_key_nonce = encrypted_master_key[:16]
        master_key_tag = encrypted_master_key[16:32]
        enc_master_key = encrypted_master_key[32:]

        # Gets key, decrypts and verifies master key
        password = self.password_entry.get().encode('utf-8')
        if self.key_file_status:
            with open(self.path_to_keyfile, 'rb') as file:
                password += file.read()
        key = hash_secret_raw(secret=password,
                              salt=salt,
                              time_cost=time_cost,
                              memory_cost=memory_cost,
                              parallelism=parallelism,
                              hash_len=32,
                              type=Type.ID)

        cipher = AES.new(key, AES.MODE_EAX, nonce=master_key_nonce)
        self.master_key = cipher.decrypt(enc_master_key)

        try:
            cipher.verify(master_key_tag)
            print(self.lang.master_key_verification_ok)
        except ValueError:
            msg = CTkMessagebox(icon="cancel",
                                title=self.lang.open_db_msg_title,
                                message=self.lang.open_db_msg_message)
            print(self.lang.open_db_msg_message)
            self.destroy()
            # It will exit only once 'OK' button is clicked
            msg.get()

            exit(1)

        # Clearing window
        for widget in self.winfo_children():
            widget.destroy()

        # Setting minimal window size
        self.minsize(DB_VIEWER_MIN_WIDTH, DB_VIEWER_MIN_HEIGHT)

        # Allowing resize
        self.resizable(True, True)

        # ----- Left Frame ----- #

        left_frame = CTkFrame(self)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        create_entry_button = CTkButton(left_frame,
                                        text=self.lang.create_entry_btn,
                                        command=lambda: CreateEntry(self.master_key,
                                                                    self.db, self.c,
                                                                    self.update_entries_list).mainloop())
        create_entry_button.grid(row=0, column=0, sticky="nsew", padx=20, pady=10)

        clear_all_btn = CTkButton(left_frame,
                                  text=self.lang.clear_all_btn,
                                  command=lambda: self.clear_all())
        clear_all_btn.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

        db_settings = CTkButton(left_frame,
                                text=self.lang.db_settings_btn,
                                command=lambda: ModifyDatabase(self.db,
                                                               self.c,
                                                               self.master_key,
                                                               self.exit).mainloop())
        db_settings.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)

        export_import_btn = CTkButton(left_frame,
                                      text=self.lang.export_import_btn,
                                      command=lambda: ImportExportDB(self.db, self.c, self.master_key,
                                                                     self.update_entries_list).mainloop())
        export_import_btn.grid(row=3, column=0, sticky="nsew", padx=20, pady=10)

        if SHOW_UPDATE_BUTTON:
            update_btn = CTkButton(left_frame,
                                   text=self.lang.update_btn,
                                   command=lambda: self.update_entries_list())
            update_btn.grid(row=4, column=0, sticky="nsew", padx=20, pady=10)

        clear_clipboard_btn = CTkButton(left_frame,
                                        text=self.lang.clear_clipboard,
                                        command=lambda: self.clear_clipboard())
        clear_clipboard_btn.grid(row=5, column=0, sticky="nsew", padx=20, pady=10)

        # ----- Right Frame ----- #

        self.right_frame = CTkScrollableFrame(self)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.update_entries_list()

    def delete_entry(self, uuid):
        """Deletes entry. Handles 'delete' button in right frame"""
        self.c.execute("DELETE FROM db_storage WHERE "
                       "uuid=?", (uuid,))
        self.db.commit()
        self.update_entries_list()

    def update_entries_list(self):
        """Updates entries list (hard to guess, right?).
        Clears right frame, then creates 'Name' and 'Login' labels. Gets all entries from database
        and decrypts with self.master_key"""
        # Clears right frame
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        name_label = CTkLabel(self.right_frame,
                              text=self.lang.name_label,
                              font=CTkFont(weight="bold"))
        name_label.grid(row=2, column=0, padx=30, pady=10)

        login_label = CTkLabel(self.right_frame,
                               text=self.lang.login_label,
                               font=CTkFont(weight="bold"))
        login_label.grid(row=2, column=1, padx=30, pady=10)

        # Gets all entries
        self.c.execute("SELECT * FROM db_storage")
        all_entries = self.c.fetchall()
        # Decrypts entries
        decrypted_entries = [PBCrypto.decrypt_by_list(self.master_key, i) for i in all_entries]
        # Database entries will appear under name and login labels
        row_index = 3
        for i in decrypted_entries:
            name_label = CTkLabel(self.right_frame,
                                  text=i['name'])
            name_label.grid(column=0, row=row_index, padx=10, pady=5)

            login_label = CTkLabel(self.right_frame,
                                   text=i['login'])
            login_label.grid(column=1, row=row_index, padx=10, pady=5)

            show_info = CTkButton(self.right_frame,
                                  text=self.lang.show_info,
                                  width=90,
                                  command=partial(ShowInfo, i))
            show_info.grid(column=2, row=row_index, padx=10, pady=5)

            edit_info = CTkButton(self.right_frame,
                                  text=self.lang.edit_info,
                                  width=90,
                                  command=partial(ModifyEntry,
                                                  i, self.master_key,
                                                  self.update_entries_list,
                                                  self.c, self.db))

            edit_info.grid(column=3, row=row_index, padx=10, pady=5)

            delete_btn = CTkButton(self.right_frame,
                                   text=self.lang.delete_btn,
                                   width=90,
                                   command=partial(self.delete_entry, i['uuid']))
            delete_btn.grid(column=4, row=row_index, padx=5, pady=5)

            row_index += 1

    def exit(self):
        self.destroy()

    def open_keyfile_filedialog(self) -> None:
        files = [('All files', '*.*')]
        file = filedialog.askopenfile(filetypes=files)
        if locals()['file'] is not None:
            self.key_file_status = True
            self.path_to_keyfile = file.name

            self.key_file_label.configure(text=f"{self.lang.keyfile_label_part_1}: {basename(self.path_to_keyfile)}",
                                          font=CTkFont(underline=True))
        self.lift()

    def reveal_password(self) -> None:
        """Handles 'Reveal password' checkbox"""
        state = self.reveal_var.get()
        if state == "0":
            self.password_entry.configure(show='*')
        else:
            self.password_entry.configure(show='')

    @staticmethod
    def clear_clipboard() -> None:
        clipboard_copy("")
