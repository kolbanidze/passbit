from customtkinter import CTkToplevel, CTkSegmentedButton,\
    CTkFrame, CTkLabel, CTkEntry, StringVar, CTkCheckBox, CTkSwitch, CTkButton,\
    CTkFont
from tkinter.filedialog import asksaveasfile, askopenfile
from .settings import DEFAULT_ARGON2ID_PARALLELISM, DEFAULT_ARGON2ID_TIME_COST,\
    DEFAULT_ARGON2ID_MEMORY_COST, DEFAULT_SALT_SIZE, NAME, EXPORT_FILE_EXTENSION,\
    VERSION
from os.path import basename
from json import dumps as json_encode
from json import loads as json_decode
from .pb_crypto import PBCrypto, DecryptionFailed
from base64 import b64encode, b64decode
from secrets import token_bytes
from argon2.low_level import hash_secret_raw
from argon2 import Type
from CTkMessagebox import CTkMessagebox
from sqlite3 import Connection, Cursor
from .language import ImportExportDbPy
from .key_file_generator import KeyFileGenerator


class ImportExportDB(CTkToplevel):
    def __init__(self,
                 db: Connection,
                 c: Cursor,
                 master_key: bytes,
                 update_list_function) -> None:
        """Creates segmented button and active frame"""
        super().__init__()
        self.lang = ImportExportDbPy()
        self.key_file_status = False

        self.title(self.lang.title)
        self.db = db
        self.c = c
        self.master_key = master_key
        self.update_list = update_list_function
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.segmented_button = CTkSegmentedButton(self,
                                                   values=[f"{self.lang.export} ({EXPORT_FILE_EXTENSION})",
                                                           f"{self.lang.import_} ({EXPORT_FILE_EXTENSION})"],
                                                   command=self.segmented_button_handler)
        self.segmented_button.set(f"{self.lang.export} ({EXPORT_FILE_EXTENSION})")
        self.segmented_button.grid(row=0)
        self.active_frame = CTkFrame(self)
        self.active_frame.grid(row=1, sticky="nsew")
        self.export()

    def clear_active_frame(self) -> None:
        for widget in self.active_frame.winfo_children():
            widget.destroy()

    def export(self) -> None:
        # ----- Left Frame ----- #

        left_frame = CTkFrame(self.active_frame)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        filename_select_btn = CTkButton(left_frame, text=self.lang.select_file,
                                        command=lambda: self.save_export_filedialog())
        filename_select_btn.grid(row=0, pady=20, padx=15)

        self.filename_label = CTkLabel(left_frame, text=f"{self.lang.export}: {self.lang.select_file_first}")
        self.filename_label.grid(row=1, pady=20, padx=15)

        self.create_db_btn = CTkButton(left_frame, text=self.lang.export_database, state="disabled",
                                       command=lambda: self.export_db())
        self.create_db_btn.grid(row=2, pady=20, padx=15)

        self.key_file_label = CTkLabel(left_frame,
                                       text=f"{self.lang.keyfile_label_part_1}: {self.lang.select_file_first}")
        self.key_file_label.grid(row=3, pady=20, padx=15)

        key_file_button = CTkButton(left_frame,
                                    text=self.lang.keyfile_btn,
                                    command=lambda: self.open_keyfile_filedialog())
        key_file_button.grid(row=4, pady=20, padx=15)

        generate_key_file_btn = CTkButton(left_frame, text=self.lang.generate_key_file,
                                          command=lambda: KeyFileGenerator().mainloop())
        generate_key_file_btn.grid(row=5, pady=20, padx=15)


        # ----- Right Frame ----- #

        right_frame = CTkFrame(self.active_frame)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        database_name_label = CTkLabel(right_frame, text=self.lang.export_name)
        self.database_name_entry = CTkEntry(right_frame)
        database_name_label.grid(row=0, column=0, sticky="nsew", padx=15, pady=10)
        self.database_name_entry.grid(row=0, column=1, sticky="nsew", padx=15, pady=10)

        database_description_label = CTkLabel(right_frame, text=self.lang.export_description)
        self.database_description_entry = CTkEntry(right_frame)
        database_description_label.grid(row=1, column=0, sticky="nsew", padx=15, pady=10)
        self.database_description_entry.grid(row=1, column=1, sticky="nsew", padx=15, pady=10)

        password_label = CTkLabel(right_frame, text=self.lang.export_password)
        self.password_entry = CTkEntry(right_frame, show='*')
        password_label.grid(row=2, column=0, sticky="nsew", padx=15, pady=10)
        self.password_entry.grid(row=2, column=1, sticky="nsew", padx=15, pady=10)

        self.reveal_var = StringVar()
        password_reveal_checkbox = CTkCheckBox(right_frame, text=self.lang.reveal_password, onvalue=True,
                                               offvalue=False,
                                               variable=self.reveal_var,
                                               command=lambda: self.reveal_password())
        password_reveal_checkbox.grid(row=3, column=0, sticky="nsew", padx=15, pady=10)

        self.kdf_status = StringVar()
        kdf_config_btn = CTkSwitch(right_frame, text=self.lang.kdf_edit, variable=self.kdf_status,
                                   onvalue=True, offvalue=False,
                                   command=lambda: self.kdf_switch())
        kdf_config_btn.grid(row=3, column=1, sticky="nsew", padx=15, pady=10)

        time_cost_label = CTkLabel(right_frame, text=self.lang.time_cost)
        self.time_cost_entry = CTkEntry(right_frame)
        time_cost_label.grid(row=4, column=0, sticky="nsew", padx=15, pady=10)
        self.time_cost_entry.grid(row=4, column=1, sticky="nsew", padx=15, pady=10)

        memory_cost_label = CTkLabel(right_frame, text=self.lang.memory_cost)
        self.memory_cost_entry = CTkEntry(right_frame)
        memory_cost_label.grid(row=5, column=0, sticky="nsew", padx=15, pady=10)
        self.memory_cost_entry.grid(row=5, column=1, sticky="nsew", padx=15, pady=10)

        parallelism_label = CTkLabel(right_frame, text=self.lang.parallelism)
        self.parallelism_entry = CTkEntry(right_frame)
        parallelism_label.grid(row=6, column=0, sticky="nsew", padx=15, pady=10)
        self.parallelism_entry.grid(row=6, column=1, sticky="nsew", padx=15, pady=10)

        salt_size_label = CTkLabel(right_frame, text=self.lang.salt_size)
        self.salt_size_entry = CTkEntry(right_frame)
        salt_size_label.grid(row=7, column=0, sticky="nsew", padx=15, pady=10)
        self.salt_size_entry.grid(row=7, column=1, sticky="nsew", padx=15, pady=10)

        self.time_cost_entry.insert(0, f'{DEFAULT_ARGON2ID_TIME_COST}')
        self.memory_cost_entry.insert(0, f'{DEFAULT_ARGON2ID_MEMORY_COST}')
        self.parallelism_entry.insert(0, f'{DEFAULT_ARGON2ID_PARALLELISM}')
        self.salt_size_entry.insert(0, f'{DEFAULT_SALT_SIZE}')
        self.time_cost_entry.configure(state="disabled")
        self.memory_cost_entry.configure(state="disabled")
        self.parallelism_entry.configure(state="disabled")
        self.salt_size_entry.configure(state="disabled")

    def export_db(self):
        password = self.password_entry.get().encode('utf-8')
        argon2id_time_cost = int(self.time_cost_entry.get())
        argon2id_memory_cost = int(self.memory_cost_entry.get())
        argon2id_parallelism = int(self.salt_size_entry.get())
        salt_size = int(self.salt_size_entry.get())
        db_name = self.database_name_entry.get()
        db_description = self.database_description_entry.get()

        if self.key_file_status:
            with open(self.path_to_keyfile, 'rb') as file:
                password += file.read()

        # Assertions
        assert type(salt_size) is int, "Salt size must be integer."
        assert type(argon2id_time_cost) is int, "Time cost must be integer."
        assert type(argon2id_memory_cost) is int, "Memory cost must be integer."
        assert type(argon2id_parallelism) is int, "Parallelism must be integer."
        assert type(db_name) is str, "Database name must be string."
        assert type(db_description) is str, "Database description must be string."
        assert type(password) is bytes, "Password must be bytes."

        salt = token_bytes(salt_size)
        key = hash_secret_raw(secret=password,
                              salt=salt,
                              time_cost=argon2id_time_cost,
                              memory_cost=argon2id_memory_cost,
                              parallelism=argon2id_parallelism,
                              hash_len=32,
                              type=Type.ID)

        # Assertions
        assert type(salt) is bytes, "Salt must be bytes."
        assert len(salt) == salt_size, "Salt size mismatch."

        export_header = {
            "version": VERSION,
            "name": db_name,
            "description": db_description,
            "time_cost": argon2id_time_cost,
            "memory_cost": argon2id_memory_cost,
            "parallelism": argon2id_parallelism,
            "salt": b64encode(salt).decode('utf-8')
        }

        self.c.execute("SELECT * FROM db_storage")
        all_entries = self.c.fetchall()
        plaintext_entries = [PBCrypto.decrypt_by_list(self.master_key, i) for i in all_entries]
        export_enc_entries = [PBCrypto.encrypt_by_dict(key, i) for i in plaintext_entries]
        encoded_entries = ImportExportDB.convert_list_to_base64(export_enc_entries)

        # Saving to json file
        to_save = {"header": export_header,
                   "export_storage": encoded_entries}
        with open(self.fullpath_to_db, 'w') as file:
            file.write(json_encode(to_save))

        CTkMessagebox(icon="check",
                      title=self.lang.msg_box_title,
                      message=self.lang.msg_box_message)

    @staticmethod
    def convert_list_to_base64(encrypted_list: list) -> list:
        encoded_list = []
        for i in encrypted_list:
            encoded_list.append({'uuid': i['uuid'],
                                 'name': b64encode(i['name']).decode('utf-8'),
                                 'description': b64encode(i['description']).decode('utf-8'),
                                 'login': b64encode(i['login']).decode('utf-8'),
                                 'password': b64encode(i['password']).decode('utf-8'),
                                 'is_totp': b64encode(i['is_totp']).decode('utf-8')})
        return encoded_list

    @staticmethod
    def convert_list_from_base64(encrypted_list: list) -> list:
        decoded_list = []
        for i in encrypted_list:
            decoded_list.append({'uuid': i['uuid'],
                                 'name': b64decode(i['name']),
                                 'description': b64decode(i['description']),
                                 'login': b64decode(i['login']),
                                 'password': b64decode(i['password']),
                                 'is_totp': b64decode(i['is_totp'])})
        return decoded_list

    def reveal_password(self) -> None:
        """Handles 'Reveal password' checkbox"""
        state = self.reveal_var.get()
        if state == "0":
            self.password_entry.configure(show='*')
        else:
            self.password_entry.configure(show='')

    def kdf_switch(self) -> None:
        """Handles 'Allow KDF Edit' switch"""

        state = self.kdf_status.get()
        if state == "0":
            self.time_cost_entry.configure(state="disabled")
            self.memory_cost_entry.configure(state="disabled")
            self.parallelism_entry.configure(state="disabled")
            self.salt_size_entry.configure(state="disabled")
        else:
            self.time_cost_entry.configure(state="normal")
            self.memory_cost_entry.configure(state="normal")
            self.parallelism_entry.configure(state="normal")
            self.salt_size_entry.configure(state="normal")

    def save_export_filedialog(self) -> None:
        """Handles filedialog"""
        files = [(f'{NAME} export', f'{EXPORT_FILE_EXTENSION}'), ('All files', '*.*')]
        file = asksaveasfile(filetypes=files)
        # Checking if db file was selected
        if locals()['file'] is not None:
            filename = basename(file.name)
            self.fullpath_to_db = file.name
            self.filename_label.configure(text=f"{self.lang.export}: {filename}", font=CTkFont(underline=True))
            self.create_db_btn.configure(state="normal")
        # DB export window will be active after filedialog
        self.lift()
        self.segmented_button.configure(state="disabled")

    def import_from_export(self) -> None:
        # ----- Left Frame ----- #

        left_frame = CTkFrame(self.active_frame)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        filename_select_btn = CTkButton(left_frame, text=self.lang.select_file,
                                        command=lambda: self.import_db_filedialog())
        filename_select_btn.grid(row=0, pady=20, padx=15)

        self.filename_label = CTkLabel(left_frame, text=f"{self.lang.import_}: {self.lang.select_file_first}")
        self.filename_label.grid(row=1, pady=20, padx=15)

        self.import_db_btn = CTkButton(left_frame, text=self.lang.import_database, state="disabled",
                                       command=lambda: self.import_db())
        self.import_db_btn.grid(row=2, pady=20, padx=15)

        self.key_file_label = CTkLabel(left_frame,
                                       text=f"{self.lang.keyfile_label_part_1}: {self.lang.select_file_first}")
        self.key_file_label.grid(row=3, pady=20, padx=15)

        key_file_button = CTkButton(left_frame,
                                    text=self.lang.keyfile_btn,
                                    command=lambda: self.open_keyfile_filedialog())
        key_file_button.grid(row=4, pady=20, padx=15)

        generate_key_file_btn = CTkButton(left_frame, text=self.lang.generate_key_file,
                                          command=lambda: KeyFileGenerator().mainloop())
        generate_key_file_btn.grid(row=5, pady=20, padx=15)

        # ----- Right Frame ----- #

        right_frame = CTkFrame(self.active_frame)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        database_name_label = CTkLabel(right_frame, text=self.lang.export_name)
        self.database_name_entry = CTkEntry(right_frame)
        database_name_label.grid(row=0, column=0, sticky="nsew", padx=15, pady=10)
        self.database_name_entry.grid(row=0, column=1, sticky="nsew", padx=15, pady=10)

        database_description_label = CTkLabel(right_frame, text=self.lang.export_description)
        self.database_description_entry = CTkEntry(right_frame)
        database_description_label.grid(row=1, column=0, sticky="nsew", padx=15, pady=10)
        self.database_description_entry.grid(row=1, column=1, sticky="nsew", padx=15, pady=10)

        password_label = CTkLabel(right_frame, text=self.lang.export_password)
        self.password_entry = CTkEntry(right_frame, show='*')
        password_label.grid(row=2, column=0, sticky="nsew", padx=15, pady=10)
        self.password_entry.grid(row=2, column=1, sticky="nsew", padx=15, pady=10)

        self.reveal_var = StringVar()
        password_reveal_checkbox = CTkCheckBox(right_frame, text=self.lang.reveal_password, onvalue=True,
                                               offvalue=False,
                                               variable=self.reveal_var,
                                               command=lambda: self.reveal_password())
        password_reveal_checkbox.grid(row=3, column=0, sticky="nsew", padx=15, pady=10)

        time_cost_label = CTkLabel(right_frame, text=self.lang.time_cost)
        self.time_cost_entry = CTkEntry(right_frame)
        time_cost_label.grid(row=4, column=0, sticky="nsew", padx=15, pady=10)
        self.time_cost_entry.grid(row=4, column=1, sticky="nsew", padx=15, pady=10)

        memory_cost_label = CTkLabel(right_frame, text=self.lang.memory_cost)
        self.memory_cost_entry = CTkEntry(right_frame)
        memory_cost_label.grid(row=5, column=0, sticky="nsew", padx=15, pady=10)
        self.memory_cost_entry.grid(row=5, column=1, sticky="nsew", padx=15, pady=10)

        parallelism_label = CTkLabel(right_frame, text=self.lang.parallelism)
        self.parallelism_entry = CTkEntry(right_frame)
        parallelism_label.grid(row=6, column=0, sticky="nsew", padx=15, pady=10)
        self.parallelism_entry.grid(row=6, column=1, sticky="nsew", padx=15, pady=10)

        salt_size_label = CTkLabel(right_frame, text=self.lang.salt_size)
        self.salt_size_entry = CTkEntry(right_frame)
        salt_size_label.grid(row=7, column=0, sticky="nsew", padx=15, pady=10)
        self.salt_size_entry.grid(row=7, column=1, sticky="nsew", padx=15, pady=10)

        self.database_name_entry.insert(0, self.lang.select_file_first)
        self.database_description_entry.insert(0, self.lang.select_file_first)
        self.time_cost_entry.insert(0, self.lang.select_file_first)
        self.memory_cost_entry.insert(0, self.lang.select_file_first)
        self.parallelism_entry.insert(0, self.lang.select_file_first)
        self.salt_size_entry.insert(0, self.lang.select_file_first)

        self.database_name_entry.configure(state="disabled")
        self.database_description_entry.configure(state="disabled")
        self.time_cost_entry.configure(state="disabled")
        self.memory_cost_entry.configure(state="disabled")
        self.parallelism_entry.configure(state="disabled")
        self.salt_size_entry.configure(state="disabled")

    def import_db_filedialog(self) -> None:
        """Handles import filedialog"""
        files = [(f'{NAME} import', f'{EXPORT_FILE_EXTENSION}'), ('All files', '*.*')]
        file = askopenfile(filetypes=files)
        # Checking if db file was selected
        if locals()['file'] is not None:
            filename = basename(file.name)
            self.fullpath_to_export = file.name
            self.filename_label.configure(text=f"{self.lang.import_}: {filename}", font=CTkFont(underline=True))
            self.import_db_btn.configure(state="normal")

            self.database_name_entry.configure(state="normal")
            self.database_description_entry.configure(state="normal")
            self.time_cost_entry.configure(state="normal")
            self.memory_cost_entry.configure(state="normal")
            self.parallelism_entry.configure(state="normal")
            self.salt_size_entry.configure(state="normal")

            with open(self.fullpath_to_export, 'r') as file:
                self.export = json_decode(file.read())
            header = self.export['header']
            self.database_name_entry.delete(0, "end")
            self.database_description_entry.delete(0, "end")
            self.time_cost_entry.delete(0, "end")
            self.memory_cost_entry.delete(0, "end")
            self.parallelism_entry.delete(0, "end")
            self.salt_size_entry.delete(0, "end")
            self.database_name_entry.insert(0, header['name'])
            self.database_description_entry.insert(0, header['description'])
            self.time_cost_entry.insert(0, header['time_cost'])
            self.memory_cost_entry.insert(0, header['memory_cost'])
            self.parallelism_entry.insert(0, header['parallelism'])
            self.salt_size_entry.insert(0, str(len(header['salt'])))

            self.time_cost_entry.configure(state="disabled")
            self.memory_cost_entry.configure(state="disabled")
            self.parallelism_entry.configure(state="disabled")
            self.salt_size_entry.configure(state="disabled")
            self.segmented_button.configure(state="disabled")

        # DB export window will be active after filedialog
        self.lift()

    def segmented_button_handler(self, value) -> None:
        self.clear_active_frame()
        if value == f"{self.lang.export} ({EXPORT_FILE_EXTENSION})":
            self.export()
        elif value == f"{self.lang.import_} ({EXPORT_FILE_EXTENSION})":
            self.import_from_export()

    def merge_databases(self, import_db: list) -> None:
        self.c.execute("SELECT * FROM db_storage")
        current_entries = self.c.fetchall()
        for i in import_db:
            merge_entry = True
            for j in current_entries:
                if j[0] == i['uuid']:
                    print(f"{self.lang.uuid_saved_part_1} {i['uuid']} {self.lang.uuid_saved_part_2}")
                    merge_entry = False
            if merge_entry:
                encrypted_entry = PBCrypto.encrypt_by_dict(self.master_key, i)
                uuid = encrypted_entry['uuid']
                self.c.execute("INSERT INTO db_storage (uuid, name, description,"
                               "                        login, password, is_totp) VALUES ("
                               "?, ?, ?, ?, ?, ?)", (uuid, encrypted_entry['name'], encrypted_entry['description'],
                                                     encrypted_entry['login'], encrypted_entry['password'],
                                                     encrypted_entry['is_totp']))
                self.db.commit()

    def import_db(self) -> None:
        with open(self.fullpath_to_export, 'r') as file:
            export_db = json_decode(file.read())
        password = self.password_entry.get().encode('utf-8')
        if self.key_file_status:
            with open(self.path_to_keyfile, 'rb') as file:
                password += file.read()
        key = hash_secret_raw(secret=password,
                              salt=b64decode(export_db['header']['salt']),
                              time_cost=export_db['header']['time_cost'],
                              memory_cost=export_db['header']['memory_cost'],
                              parallelism=export_db['header']['parallelism'],
                              hash_len=32,
                              type=Type.ID)
        entries = export_db['export_storage']
        decoded_entries = self.convert_list_from_base64(entries)
        try:
            decrypted_entries = [PBCrypto.decrypt_by_dict(key, i) for i in decoded_entries]
        except DecryptionFailed:
            msg = CTkMessagebox(icon="cancel",
                                message=self.lang.msg_box_error_message,
                                title=self.lang.msg_box_error_title)
            # It will exit only once 'OK' button is clicked
            msg.get()
            exit(1)

        self.merge_databases(decrypted_entries)
        self.update_list()
        CTkMessagebox(icon="check",
                      message=self.lang.msg_box_message,
                      title=self.lang.msg_box_title)

    def open_keyfile_filedialog(self) -> None:
        files = [('All files', '*.*')]
        file = askopenfile(filetypes=files)
        if locals()['file'] is not None:
            self.key_file_status = True
            self.path_to_keyfile = file.name

            self.key_file_label.configure(text=f"{self.lang.keyfile_label_part_1}: {basename(self.path_to_keyfile)}",
                                          font=CTkFont(underline=True))
        self.lift()
