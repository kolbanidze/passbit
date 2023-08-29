from customtkinter import CTkToplevel, CTkSegmentedButton, CTkFrame, CTkLabel, CTkEntry,\
    CTkButton, StringVar, CTkCheckBox, CTkSwitch, CTkFont, filedialog
from secrets import token_bytes
from argon2.low_level import hash_secret_raw
from argon2 import Type
from Crypto.Cipher import AES
from .pb_crypto import PBCrypto
from .settings import DEFAULT_ARGON2ID_PARALLELISM, DEFAULT_ARGON2ID_TIME_COST,\
    DEFAULT_ARGON2ID_MEMORY_COST, DEFAULT_SALT_SIZE
from CTkMessagebox import CTkMessagebox
from sqlite3 import Cursor, Connection
from .language import ModifyDatabasePy
from os.path import basename
from .key_file_generator import KeyFileGenerator


class ModifyDatabase(CTkToplevel):
    def __init__(self,
                 db: Connection,
                 cursor: Cursor,
                 master_key: bytes,
                 exit_function) -> None:
        """Creates segmented button and frame, where will be content"""
        super().__init__()
        self.lang = ModifyDatabasePy()
        self.key_file_status = False
        self.title(self.lang.title)
        self.db = db
        self.c = cursor
        self.master_key = master_key
        self.exit_function = exit_function

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.segmented_button = CTkSegmentedButton(self,
                                                   values=[self.lang.view_db_metadata,
                                                           self.lang.modify_db_metadata,
                                                           self.lang.password_and_kdf],
                                                   command=self.segmented_button_handler)
        self.segmented_button.set(self.lang.view_db_metadata)
        self.segmented_button.grid(row=0)
        self.active_frame = CTkFrame(self)

        self.active_frame.grid(row=1, sticky="nsew")

        # Showing default menu
        self.view_db_metadata()

    def view_db_metadata(self) -> None:
        """View db metadata menu (inside active frame)"""

        # Getting database header
        self.c.execute("SELECT * FROM db_header")
        db_header = self.c.fetchall()[0]

        version_label = CTkLabel(self.active_frame, text="Version")
        version_entry = CTkEntry(self.active_frame)
        version_entry.insert(0, db_header[0])
        version_entry.configure(state="disabled")
        version_label.grid(row=0, column=0, padx=20, pady=5, sticky="nsew")
        version_entry.grid(row=0, column=1, padx=20, pady=5, sticky="nsew")

        name_label = CTkLabel(self.active_frame, text=self.lang.name)
        name_entry = CTkEntry(self.active_frame)
        name_entry.insert(0, db_header[1])
        name_entry.configure(state="disabled")
        name_label.grid(row=1, column=0, padx=20, pady=5, sticky="nsew")
        name_entry.grid(row=1, column=1, padx=20, pady=5, sticky="nsew")

        description_label = CTkLabel(self.active_frame, text=self.lang.description)
        description_entry = CTkEntry(self.active_frame)
        description_entry.insert(0, db_header[2])
        description_entry.configure(state="disabled")
        description_label.grid(row=2, column=0, padx=20, pady=5, sticky="nsew")
        description_entry.grid(row=2, column=1, padx=20, pady=5, sticky="nsew")

        time_cost_label = CTkLabel(self.active_frame, text=self.lang.time_cost)
        time_cost_entry = CTkEntry(self.active_frame)
        time_cost_entry.insert(0, db_header[3])
        time_cost_entry.configure(state="disabled")
        time_cost_label.grid(row=3, column=0, padx=20, pady=5, sticky="nsew")
        time_cost_entry.grid(row=3, column=1, padx=20, pady=5, sticky="nsew")

        memory_cost_label = CTkLabel(self.active_frame, text=self.lang.memory_cost)
        memory_cost_entry = CTkEntry(self.active_frame)
        memory_cost_entry.insert(0, db_header[4])
        memory_cost_entry.configure(state="disabled")
        memory_cost_label.grid(row=4, column=0, padx=20, pady=5, sticky="nsew")
        memory_cost_entry.grid(row=4, column=1, padx=20, pady=5, sticky="nsew")

        parallelism_label = CTkLabel(self.active_frame, text=self.lang.parallelism)
        parallelism_entry = CTkEntry(self.active_frame)
        parallelism_entry.insert(0, db_header[5])
        parallelism_entry.configure(state="disabled")
        parallelism_label.grid(row=5, column=0, padx=20, pady=5, sticky="nsew")
        parallelism_entry.grid(row=5, column=1, padx=20, pady=5, sticky="nsew")

    def modify_db_metadata(self):
        """Modify DB metadata menu"""
        def _update_db():
            """Internal function for updating database name and description"""
            self.c.execute("UPDATE db_header SET "
                           "db_name=?,"
                           "db_description=?", (name_entry.get(), description_entry.get()))
            self.db.commit()
            self.clear_active_frame()
            CTkMessagebox(icon="check",
                          message=self.lang.msg_box_message,
                          title=self.lang.msg_box_title)
            self.modify_db_metadata()

        # Getting db header
        self.c.execute("SELECT * FROM db_header")
        db_header = self.c.fetchall()[0]

        name_label = CTkLabel(self.active_frame,
                              text=self.lang.name)
        name_entry = CTkEntry(self.active_frame)
        name_entry.insert(0, db_header[1])
        name_label.grid(row=0, column=0, padx=20, pady=5, sticky="nsew")
        name_entry.grid(row=0, column=1, padx=20, pady=5, sticky="nsew")

        description_label = CTkLabel(self.active_frame,
                                     text=self.lang.description)
        description_entry = CTkEntry(self.active_frame)
        description_entry.insert(0, db_header[2])
        description_label.grid(row=1, column=0, padx=20, pady=5, sticky="nsew")
        description_entry.grid(row=1, column=1, padx=20, pady=5, sticky="nsew")

        save_btn = CTkButton(self.active_frame,
                             text=self.lang.save,
                             command=lambda: _update_db())
        save_btn.grid(row=2, column=1, padx=20, pady=5, sticky="nsew")

    def clear_active_frame(self):
        """Clears active frame. Used when changing menu"""

        for widget in self.active_frame.winfo_children():
            widget.destroy()

    def update_keys(self):
        """Backend for 'Password & KDF' menu"""
        # Updating master key
        new_master_key = token_bytes(32)

        # Getting password and generating salt
        new_password = self.password_entry.get().encode('utf-8')
        new_salt = token_bytes(int(self.salt_size_entry.get()))
        if self.key_file_status:
            with open(self.path_to_keyfile, 'rb') as file:
                new_password += file.read()

        # Getting KDF parameters
        new_time_cost = int(self.time_cost_entry.get())
        new_memory_cost = int(self.memory_cost_entry.get())
        new_parallelism = int(self.parallelism_entry.get())

        new_key = hash_secret_raw(secret=new_password,
                                  salt=new_salt,
                                  time_cost=new_time_cost,
                                  memory_cost=new_memory_cost,
                                  parallelism=new_parallelism,
                                  hash_len=32,
                                  type=Type.ID)

        # Encrypting new master key
        cipher = AES.new(new_key, AES.MODE_EAX)
        nonce = cipher.nonce
        enc_master_key, master_key_tag = cipher.encrypt_and_digest(new_master_key)

        encrypted_master_key = nonce + master_key_tag + enc_master_key

        # Updates db header
        self.c.execute("UPDATE db_header SET "
                       "time_cost=?,"
                       "memory_cost=?,"
                       "parallelism=?,"
                       "salt=?,"
                       "encrypted_master_key=?", (new_time_cost, new_memory_cost, new_parallelism,
                                                  new_salt, encrypted_master_key))
        self.db.commit()

        # Re-encrypting entries
        self.c.execute("SELECT * FROM db_storage")
        enc_entries = self.c.fetchall()
        all_entries = [PBCrypto.decrypt_by_list(self.master_key, i) for i in enc_entries]
        new_enc_entries = [PBCrypto.encrypt_by_dict(new_master_key, i) for i in all_entries]

        # Clearing db storage
        self.c.execute("DELETE FROM db_storage")
        self.db.commit()

        for entry in new_enc_entries:
            uuid = entry['uuid']
            self.c.execute("INSERT INTO db_storage (uuid, name, description,"
                           "                        login, password, is_totp) VALUES (?, ?, ?, ?, ?, ?)",
                           (uuid, entry['name'], entry['description'], entry['login'], entry['password'],
                            entry['is_totp']))
            self.db.commit()
        self.destroy()
        CTkMessagebox(icon="check",
                      message=self.lang.msg_box_password_or_kdf_message,
                      title=self.lang.msg_box_password_or_kdf_title)
        self.exit_function()

    def password_and_kdf(self):
        """'Password & KDF' menu"""
        password_label = CTkLabel(self.active_frame, text=self.lang.new_password)
        self.password_entry = CTkEntry(self.active_frame, show='*')
        password_label.grid(row=0, column=0, padx=20, pady=5, sticky="nsew")
        self.password_entry.grid(row=0, column=1, padx=20, pady=5, sticky="nsew")

        self.key_file_label = CTkLabel(self.active_frame,
                                       text=f"{self.lang.keyfile_label_part_1}: {self.lang.keyfile_label_part_2}")
        self.key_file_label.grid(row=1, column=0, padx=20, pady=5, sticky="nsew")

        key_file_button = CTkButton(self.active_frame,
                                    text=self.lang.keyfile_btn,
                                    command=lambda: self.open_keyfile_filedialog())
        key_file_button.grid(row=1, column=1, padx=20, pady=5, sticky="nsew")

        self.reveal_var = StringVar()
        password_reveal_checkbox = CTkCheckBox(self.active_frame, text=self.lang.reveal_password,
                                               onvalue=True, offvalue=False,
                                               variable=self.reveal_var,
                                               command=lambda: self.reveal_password())
        password_reveal_checkbox.grid(row=2, column=1, padx=20, pady=5, sticky="nsew")

        self.kdf_status = StringVar()
        kdf_config_btn = CTkSwitch(self.active_frame, text=self.lang.edit_kdf, variable=self.kdf_status,
                                   onvalue=True, offvalue=False,
                                   command=lambda: self.kdf_switch())
        kdf_config_btn.grid(row=2, column=0, sticky="nsew", padx=20, pady=5)

        time_cost_label = CTkLabel(self.active_frame, text=self.lang.time_cost)
        self.time_cost_entry = CTkEntry(self.active_frame)
        time_cost_label.grid(row=3, column=0, sticky="nsew", padx=20, pady=5)
        self.time_cost_entry.grid(row=3, column=1, sticky="nsew", padx=20, pady=5)

        memory_cost_label = CTkLabel(self.active_frame, text=self.lang.memory_cost)
        self.memory_cost_entry = CTkEntry(self.active_frame)
        memory_cost_label.grid(row=4, column=0, sticky="nsew", padx=20, pady=5)
        self.memory_cost_entry.grid(row=4, column=1, sticky="nsew", padx=20, pady=5)

        parallelism_label = CTkLabel(self.active_frame, text=self.lang.parallelism)
        self.parallelism_entry = CTkEntry(self.active_frame)
        parallelism_label.grid(row=5, column=0, sticky="nsew", padx=20, pady=5)
        self.parallelism_entry.grid(row=5, column=1, sticky="nsew", padx=20, pady=5)

        salt_size_label = CTkLabel(self.active_frame, text=self.lang.salt_size)
        self.salt_size_entry = CTkEntry(self.active_frame)
        salt_size_label.grid(row=6, column=0, sticky="nsew", padx=20, pady=5)
        self.salt_size_entry.grid(row=6, column=1, sticky="nsew", padx=20, pady=5)

        self.time_cost_entry.insert(0, f'{DEFAULT_ARGON2ID_TIME_COST}')
        self.memory_cost_entry.insert(0, f'{DEFAULT_ARGON2ID_MEMORY_COST}')
        self.parallelism_entry.insert(0, f'{DEFAULT_ARGON2ID_PARALLELISM}')
        self.salt_size_entry.insert(0, f'{DEFAULT_SALT_SIZE}')
        self.time_cost_entry.configure(state="disabled")
        self.memory_cost_entry.configure(state="disabled")
        self.parallelism_entry.configure(state="disabled")
        self.salt_size_entry.configure(state="disabled")

        generate_key_file_btn = CTkButton(self.active_frame,
                                          text=self.lang.generate_key_file,
                                          command=lambda: KeyFileGenerator().mainloop())
        generate_key_file_btn.grid(row=7, column=0, padx=20, pady=5, sticky="nsew")

        update_keys_btn = CTkButton(self.active_frame, text=self.lang.update_keys_and_kdf,
                                    command=lambda: self.update_keys())
        update_keys_btn.grid(row=7, column=1, padx=20, pady=5, sticky="nsew")

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

    def segmented_button_handler(self, value):
        """Handles segmented button"""

        self.clear_active_frame()
        match value:
            case self.lang.view_db_metadata:
                self.view_db_metadata()
            case self.lang.modify_db_metadata:
                self.modify_db_metadata()
            case self.lang.password_and_kdf:
                self.password_and_kdf()

    def open_keyfile_filedialog(self) -> None:
        files = [('All files', '*.*')]
        file = filedialog.askopenfile(filetypes=files)
        if locals()['file'] is not None:
            self.key_file_status = True
            self.path_to_keyfile = file.name

            self.key_file_label.configure(text=f"{self.lang.keyfile_label_part_1}: {basename(self.path_to_keyfile)}",
                                          font=CTkFont(weight="bold"))
        self.lift()
