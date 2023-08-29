from customtkinter import CTkToplevel, CTkLabel, CTkEntry, CTkButton
from sqlite3 import connect as sql_connect
from tkinter.filedialog import askopenfile
from .settings import NAME, FILE_EXTENSION
from .language import ShowDbInfoPy


class ShowDBInfo(CTkToplevel):
    """Shows database info"""
    def __init__(self):
        super().__init__()
        self.lang = ShowDbInfoPy()
        self.title(self.lang.title)

        self.columnconfigure(0, weight=2)
        open_db_btn = CTkButton(self, text=self.lang.open_db,
                                command=lambda: self.open_db_filedialog())
        open_db_btn.grid(row=0, padx=20, pady=20, sticky="nsew")

    def db_info(self):
        # Clears window
        for widget in self.winfo_children():
            widget.destroy()

        # Gets database header
        db = sql_connect(self.db_filename)
        c = db.cursor()
        c.execute("SELECT * FROM db_header")
        db_header = c.fetchall()[0]

        version_label = CTkLabel(self, text=self.lang.version)
        version_entry = CTkEntry(self)
        version_entry.insert(0, db_header[0])
        version_entry.configure(state="disabled")
        version_label.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")
        version_entry.grid(row=0, column=1, padx=20, pady=10, sticky="nsew")

        name_label = CTkLabel(self, text=self.lang.name)
        name_entry = CTkEntry(self)
        name_entry.insert(0, db_header[1])
        name_entry.configure(state="disabled")
        name_label.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        name_entry.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")

        description_label = CTkLabel(self, text=self.lang.description)
        description_entry = CTkEntry(self)
        description_entry.insert(0, db_header[2])
        description_entry.configure(state="disabled")
        description_label.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        description_entry.grid(row=2, column=1, padx=20, pady=10, sticky="nsew")

        time_cost_label = CTkLabel(self, text=self.lang.time_cost)
        time_cost_entry = CTkEntry(self)
        time_cost_entry.insert(0, db_header[3])
        time_cost_entry.configure(state="disabled")
        time_cost_label.grid(row=4, column=0, padx=20, pady=10, sticky="nsew")
        time_cost_entry.grid(row=4, column=1, padx=20, pady=10, sticky="nsew")

        memory_cost_label = CTkLabel(self, text=self.lang.memory_cost)
        memory_cost_entry = CTkEntry(self)
        memory_cost_entry.insert(0, db_header[4])
        memory_cost_entry.configure(state="disabled")
        memory_cost_label.grid(row=5, column=0, padx=20, pady=10, sticky="nsew")
        memory_cost_entry.grid(row=5, column=1, padx=20, pady=10, sticky="nsew")

        parallelism_label = CTkLabel(self, text=self.lang.parallelism)
        parallelism_entry = CTkEntry(self)
        parallelism_entry.insert(0, db_header[5])
        parallelism_entry.configure(state="disabled")
        parallelism_label.grid(row=6, column=0, padx=20, pady=10, sticky="nsew")
        parallelism_entry.grid(row=6, column=1, padx=20, pady=10, sticky="nsew")

        close_btn = CTkButton(self, text=self.lang.close, command=lambda: self.destroy())
        close_btn.grid(row=7, column=1, padx=20, pady=15, sticky="nsew")

    def open_db_filedialog(self):
        """Handles import filedialog"""
        files = [(f'{NAME} import', f'{FILE_EXTENSION}'), ('All files', '*.*')]
        file = askopenfile(filetypes=files)
        # Checking if db file was selected
        if locals()['file'] is not None:
            self.lift()
            self.db_filename = file.name
            self.db_info()
