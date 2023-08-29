from customtkinter import CTkToplevel, CTkLabel, CTkEntry, CTkOptionMenu, CTkButton,\
    StringVar
from .language import SettingsEditorPy
from .settings import *
from pkg_resources import resource_filename
from CTkMessagebox import CTkMessagebox


class SettingsEditor(CTkToplevel):
    def __init__(self):
        super().__init__()
        self.lang = SettingsEditorPy()
        self.title(self.lang.title)

        version_label = CTkLabel(self, text=self.lang.version)
        version_label.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

        self.version_entry = CTkEntry(self)
        self.version_entry.insert(0, VERSION)
        self.version_entry.configure(state="disabled")
        self.version_entry.grid(row=0, column=1, padx=20, pady=10, sticky="nsew")

        name_label = CTkLabel(self, text=self.lang.name)
        name_label.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        self.name_entry = CTkEntry(self)
        self.name_entry.insert(0, NAME)
        self.name_entry.configure(state="disabled")
        self.name_entry.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")

        file_extension_label = CTkLabel(self, text=self.lang.file_extension)
        file_extension_label.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        self.file_extension_entry = CTkEntry(self)
        self.file_extension_entry.insert(0, FILE_EXTENSION)
        self.file_extension_entry.grid(row=2, column=1, padx=20, pady=10, sticky="nsew")

        export_extension_label = CTkLabel(self, text=self.lang.export_extension)
        export_extension_label.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")
        self.export_extension_entry = CTkEntry(self)
        self.export_extension_entry.insert(0, EXPORT_FILE_EXTENSION)
        self.export_extension_entry.grid(row=3, column=1, padx=20, pady=10, sticky="nsew")

        self.language = StringVar(value=self.lang.os_default)

        language_label = CTkLabel(self,
                                  text=self.lang.language)
        language_label.grid(row=4, column=0, padx=20, pady=10, sticky="nsew")
        language = CTkOptionMenu(self,
                                 values=[self.lang.os_default,
                                         "English",
                                         "Russian"],
                                 command=self.language_handler)
        language.set(self.lang.os_default)
        language.grid(row=4, column=1, padx=20, pady=10, sticky="nsew")

        db_min_width = CTkLabel(self,
                                text=self.lang.db_min_width)
        db_min_height = CTkLabel(self,
                                 text=self.lang.db_min_height)
        self.db_min_width_entry = CTkEntry(self)
        self.db_min_width_entry.insert(0, DB_VIEWER_MIN_WIDTH)
        self.db_min_height_entry = CTkEntry(self)
        self.db_min_height_entry.insert(0, DB_VIEWER_MIN_HEIGHT)
        db_min_width.grid(row=5, column=0, padx=20, pady=10, sticky="nsew")
        db_min_height.grid(row=6, column=0, padx=20, pady=10, sticky="nsew")
        self.db_min_width_entry.grid(row=5, column=1, padx=20, pady=10, sticky="nsew")
        self.db_min_height_entry.grid(row=6, column=1, padx=20, pady=10, sticky="nsew")

        time_cost_label = CTkLabel(self,
                                   text=self.lang.time_cost)
        time_cost_label.grid(row=7, column=0, padx=20, pady=10, sticky="nsew")
        self.time_cost_entry = CTkEntry(self)
        self.time_cost_entry.insert(0, DEFAULT_ARGON2ID_TIME_COST)
        self.time_cost_entry.grid(row=7, column=1, padx=20, pady=10, sticky="nsew")

        memory_cost_label = CTkLabel(self,
                                     text=self.lang.memory_cost)
        memory_cost_label.grid(row=8, column=0, padx=20, pady=10, sticky="nsew")
        self.memory_cost_entry = CTkEntry(self)
        self.memory_cost_entry.insert(0, DEFAULT_ARGON2ID_MEMORY_COST)
        self.memory_cost_entry.grid(row=8, column=1, padx=20, pady=10, sticky="nsew")

        parallelism_label = CTkLabel(self,
                                     text=self.lang.parallelism)
        parallelism_label.grid(row=9, column=0, padx=20, pady=10, sticky="nsew")
        self.parallelism_entry = CTkEntry(self)
        self.parallelism_entry.insert(0, DEFAULT_ARGON2ID_PARALLELISM)
        self.parallelism_entry.grid(row=9, column=1, padx=20, pady=10, sticky="nsew")

        salt_label = CTkLabel(self,
                              text=self.lang.salt)
        salt_label.grid(row=10, column=0, padx=20, pady=10, sticky="nsew")

        self.salt_entry = CTkEntry(self)
        self.salt_entry.insert(0, DEFAULT_SALT_SIZE)
        self.salt_entry.grid(row=10, column=1, padx=20, pady=10, sticky="nsew")

        cat_url_label = CTkLabel(self,
                                 text=self.lang.cat_api)
        cat_url_label.grid(row=11, column=0, padx=20, pady=10, sticky="nsew")
        self.cat_url_entry = CTkEntry(self)
        self.cat_url_entry.insert(0, THE_CAT_API_URL)
        self.cat_url_entry.grid(row=11, column=1, padx=20, pady=10, sticky="nsew")

        self.show_update_button = StringVar(value=self.lang.no)

        update_button = CTkLabel(self,
                                 text=self.lang.update_button)
        update_button.grid(row=12, column=0, padx=20, pady=10, sticky="nsew")
        update_button_optionmenu = CTkOptionMenu(self,
                                                 values=[self.lang.yes,
                                                         self.lang.no],
                                                 command=self.update_button_handler)
        update_button_optionmenu.set(self.lang.no)
        update_button_optionmenu.grid(row=12, column=1, padx=20, pady=10, sticky="nsew")

        save_btn = CTkButton(self,
                             text=self.lang.save,
                             command=lambda: self.save())
        save_btn.grid(row=13, column=1, padx=20, pady=10, sticky="nsew")

    def language_handler(self, value):
        self.language.set(value)

    def update_button_handler(self, value):
        self.show_update_button.set(value)

    def save(self):
        file_extension = self.file_extension_entry.get()
        export_file_extensoin = self.export_extension_entry.get()
        language_var = self.language.get()
        if language_var == self.lang.os_default:
            language = "os_default"
        elif language_var == "English":
            language = "en"
        elif language_var == "Russian":
            language = "ru"

        db_viewer_min_width = self.db_min_width_entry.get()
        db_viewer_min_height = self.db_min_height_entry.get()

        time_cost = self.time_cost_entry.get()
        memory_cost = self.memory_cost_entry.get()
        parallelism = self.parallelism_entry.get()

        salt_size = self.salt_entry.get()

        the_cat_api_url = self.cat_url_entry.get()

        update_btn_var = self.show_update_button.get()
        if update_btn_var == self.lang.yes:
            show_update_button = True
        elif update_btn_var == self.lang.no:
            show_update_button = False

        settings_py=  f"from locale import getlocale, windows_locale\n" \
                      f"from os import name\n\n\n" \
                      f"def get_os_language() -> str:\n" \
                      f"    if name == 'posix':\n" \
                      f"        language = getlocale()[0]\n" \
                      f"        if language[:2] == 'ru':\n" \
                      f"            return 'ru'\n" \
                      f"        else:\n" \
                      f"            return 'en'\n" \
                      f"    else:\n" \
                      f"        import ctypes\n" \
                      f"        windll = ctypes.windll.kernel32\n" \
                      f"        if windows_locale[windll.GetUserDefaultUILanguage()][:2] == 'ru':\n" \
                      f"            return 'ru'\n" \
                      f"        else:\n" \
                      f"            return 'en'\n" \
                      f"\n" \
                      f"\n" \
                      f"VERSION = '{VERSION}'\n" \
                      f"NAME = '{NAME}'\n" \
                      f"\n" \
                      f"# PassBit DataBase\n" \
                      f"FILE_EXTENSION = '{file_extension}'\n" \
                      f"# PassBit EXport\n" \
                      f"EXPORT_FILE_EXTENSION = '{export_file_extensoin}'\n" \
                      f"\n" \
                      f"# Supported languages: 'ru', 'en'\n" \
                      f"# Values: os_default, 'ru', 'en'\n" \
                      f"LANGUAGE = '{language}'\n" \
                      f"\n" \
                      f"if LANGUAGE == 'os_default':\n" \
                      f"    LANGUAGE = get_os_language()\n" \
                      f"# Database viewer screen size constants\n" \
                      f"DB_VIEWER_MIN_WIDTH = {db_viewer_min_width}\n" \
                      f"DB_VIEWER_MIN_HEIGHT = {db_viewer_min_height}\n" \
                      f"\n" \
                      f"# Default KDF parameters\n" \
                      f"DEFAULT_ARGON2ID_TIME_COST = {time_cost}\n" \
                      f"DEFAULT_ARGON2ID_MEMORY_COST = {memory_cost}\n" \
                      f"DEFAULT_ARGON2ID_PARALLELISM = {parallelism}\n" \
                      f"DEFAULT_SALT_SIZE = {salt_size}\n" \
                      f"\n" \
                      f"# Key File Generator URL\n" \
                      f"THE_CAT_API_URL = '{the_cat_api_url}'\n" \
                      f"\n" \
                      f"# Show 'Update' button in 'Database viewer'\n" \
                      f"SHOW_UPDATE_BUTTON = {show_update_button}\n"

        settings_file = resource_filename('passbit', 'settings.py')
        with open(settings_file, 'w') as file:
            file.write(settings_py)

        msg = CTkMessagebox(icon="check",
                            title=self.lang.title,
                            message=self.lang.message)
        msg.get()
        exit(0)
