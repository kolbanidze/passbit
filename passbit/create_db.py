from customtkinter import CTkToplevel, CTkFrame, CTkLabel, CTkEntry, StringVar, \
    CTkCheckBox, CTkSwitch, CTkButton, CTkFont
from tkinter import filedialog
from sqlite3 import connect as sql_connect
from .settings import *
from secrets import token_bytes
from Crypto.Cipher import AES
from argon2.low_level import hash_secret_raw
from argon2 import Type
from os.path import basename
from CTkMessagebox import CTkMessagebox
from .language import CreateDBPy
from .key_file_generator import KeyFileGenerator


class CreateDB(CTkToplevel):
    def __init__(self) -> None:
        """Creates user interface"""
        super().__init__()
        self.lang = CreateDBPy()
        # False - key file wasn't added
        # True - key file was added
        self.key_file_status = False

        self.title(self.lang.title)
        self.resizable(False, False)

        # ----- Left Frame ----- #

        left_frame = CTkFrame(self)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        filename_select_btn = CTkButton(left_frame, text=self.lang.select_file,
                                        command=lambda: self.save_db_filedialog())
        filename_select_btn.grid(row=0, pady=20, padx=15)

        self.filename_label = CTkLabel(left_frame,
                                       text=f"{self.lang.filename_label_part_1}: {self.lang.filename_label_part_2}")
        self.filename_label.grid(row=1, pady=10, padx=15)

        self.key_file_label = CTkLabel(left_frame,
                                       text=f"{self.lang.key_file}: {self.lang.filename_label_part_2}")
        self.key_file_label.grid(row=2, pady=10, padx=15)

        self.create_db_btn = CTkButton(left_frame, text=self.lang.create_db, state="disabled",
                                       command=lambda: self.create_db())
        self.create_db_btn.grid(row=3, pady=20, padx=15)

        self.key_file_btn = CTkButton(left_frame, text=self.lang.add_key_file,
                                      command=lambda: self.open_keyfile_filedialog())
        self.key_file_btn.grid(row=4, pady=20, padx=15)

        generate_key_file_btn = CTkButton(left_frame, text=self.lang.generate_key_file,
                                          command=lambda: KeyFileGenerator().mainloop())
        generate_key_file_btn.grid(row=5, pady=20, padx=15)

        key_file_description = CTkLabel(left_frame, text=self.lang.key_file_short_description)
        key_file_description.grid(row=6, pady=20, padx=5)

        # ----- Right Frame ----- #

        right_frame = CTkFrame(self)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        database_name_label = CTkLabel(right_frame, text=self.lang.db_name)
        self.database_name_entry = CTkEntry(right_frame)
        database_name_label.grid(row=0, column=0, sticky="nsew", padx=15, pady=10)
        self.database_name_entry.grid(row=0, column=1, sticky="nsew", padx=15, pady=10)

        database_description_label = CTkLabel(right_frame, text=self.lang.db_description)
        self.database_description_entry = CTkEntry(right_frame)
        database_description_label.grid(row=1, column=0, sticky="nsew", padx=15, pady=10)
        self.database_description_entry.grid(row=1, column=1, sticky="nsew", padx=15, pady=10)

        password_label = CTkLabel(right_frame, text=self.lang.password)
        self.password_entry = CTkEntry(right_frame, show='*')
        password_label.grid(row=2, column=0, sticky="nsew", padx=15, pady=10)
        self.password_entry.grid(row=2, column=1, sticky="nsew", padx=15, pady=10)

        self.reveal_var = StringVar()
        password_reveal_checkbox = CTkCheckBox(right_frame, text=self.lang.reveal_password,
                                               onvalue=True, offvalue=False,
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

    def create_db(self) -> None:
        """Gets parameters from 'Database creation' window. Generates master key (256-bit) and
        user key (256-bit, argon2id). Encrypts master key with user key. Creates tables (db_header and db_storage).
        Inserts data into db_header. Shows success message after creation."""

        # Getting db from password entry
        password = self.password_entry.get().encode("utf-8")

        if self.key_file_status:
            with open(self.path_to_keyfile, 'rb') as file:
                password += file.read()

        argon2id_time_cost = int(self.time_cost_entry.get())
        argon2id_memory_cost = int(self.memory_cost_entry.get())
        argon2id_parallelism = int(self.salt_size_entry.get())
        salt_size = int(self.salt_size_entry.get())
        db_name = self.database_name_entry.get()
        db_description = self.database_description_entry.get()

        # Assertions
        assert type(salt_size) is int, "Salt size must be integer."
        assert type(argon2id_time_cost) is int, "Time cost must be integer."
        assert type(argon2id_memory_cost) is int, "Memory cost must be integer."
        assert type(argon2id_parallelism) is int, "Parallelism must be integer."
        assert type(db_name) is str, "Database name must be string."
        assert type(db_description) is str, "Database description must be string."
        assert type(password) is bytes, "Password must be bytes."

        # Generating salt
        salt = token_bytes(salt_size)

        # Getting 256-bit key
        key = hash_secret_raw(secret=password,
                              salt=salt,
                              time_cost=argon2id_time_cost,
                              memory_cost=argon2id_memory_cost,
                              parallelism=argon2id_parallelism,
                              hash_len=32,
                              type=Type.ID)

        # Generating 256-bit master key
        master_key = token_bytes(32)

        # Assertions
        assert type(salt) is bytes, "Salt must be bytes."
        assert len(salt) == salt_size, "Salt size mismatch."

        # Encrypting master key with user's key
        cipher = AES.new(key, AES.MODE_EAX)
        master_key_nonce = cipher.nonce
        encrypted_master_key, master_key_tag = cipher.encrypt_and_digest(master_key)

        encrypted_master_key_with_nonce_and_tag = master_key_nonce + master_key_tag + encrypted_master_key

        # Assertions
        assert len(master_key_nonce) == 16, "Encrypted master key nonce must be 16 bytes."
        assert len(master_key_tag) == 16, "Encrypted master key tag must be 16 bytes."

        # Creating db
        db = sql_connect(self.fullpath_to_db)
        c = db.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS db_header ("
                  "version text,"
                  "db_name text,"
                  "db_description text,"
                  "time_cost int,"
                  "memory_cost int,"
                  "parallelism int,"
                  "salt blob,"
                  "encrypted_master_key blob)")

        c.execute("CREATE TABLE IF NOT EXISTS db_storage ("
                  "uuid text,"
                  "name blob,"
                  "description blob,"
                  "login blob,"
                  "password blob,"
                  "is_totp blob)")
        db.commit()

        # Inserting data into db header
        c.execute("INSERT INTO db_header (version, db_name, db_description,"
                  "                       time_cost, memory_cost, parallelism,"
                  "                       salt, encrypted_master_key) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                  (VERSION, db_name, db_description, argon2id_time_cost, argon2id_memory_cost, argon2id_parallelism,
                   salt, encrypted_master_key_with_nonce_and_tag))
        db.commit()
        db.close()
        # Closing window
        self.destroy()
        # Showing success message
        CTkMessagebox(icon="check",
                      message=self.lang.msg_box_message,
                      title=self.lang.msg_box_title)

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

    def reveal_password(self) -> None:
        """Handles 'Reveal password' checkbox"""

        state = self.reveal_var.get()
        if state == "0":
            self.password_entry.configure(show='*')
        else:
            self.password_entry.configure(show='')

    def save_db_filedialog(self) -> None:
        """Handles filedialog"""

        files = [(f'{NAME} database', f'{FILE_EXTENSION}'), ('All files', '*.*')]
        file = filedialog.asksaveasfile(filetypes=files)
        # Checking if db file was selected
        if locals()['file'] is not None:
            filename = basename(file.name)
            self.fullpath_to_db = file.name
            self.filename_label.configure(text=f"{self.lang.filename_label_part_1}: {filename}",
                                          font=CTkFont(underline=True))
            self.create_db_btn.configure(state="normal")
            # DB creation window will be active after filedialog
        self.lift()

    def open_keyfile_filedialog(self) -> None:
        files = [('All files', '*.*')]
        file = filedialog.askopenfile(filetypes=files)
        if locals()['file'] is not None:
            self.key_file_status = True
            self.path_to_keyfile = file.name

            self.key_file_label.configure(text=f"{self.lang.key_file}: {basename(self.path_to_keyfile)}",
                                          font=CTkFont(underline=True))
        self.lift()
