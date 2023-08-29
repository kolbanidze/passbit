from .settings import NAME, VERSION
from customtkinter import CTk, CTkLabel, CTkFont, CTkButton
from .open_db import OpenDB
from .create_db import CreateDB
from .show_db_info import ShowDBInfo
from .password_generator import PasswordGenerator
from .language import AppPy


class App(CTk):
    def __init__(self) -> None:
        """Shows main menu"""
        super().__init__()
        self.lang = AppPy()
        self.title(NAME)
        self.resizable(False, False)

        self.columnconfigure(0, weight=2)

        main_menu_label = CTkLabel(self,
                                   text=f"{NAME} {VERSION}",
                                   font=CTkFont(size=20, weight="bold"))
        main_menu_label.grid(row=0, padx=20, pady=10)

        main_menu_open_db_btn = CTkButton(self,
                                          text=self.lang.open_db_btn,
                                          command=lambda: OpenDB().mainloop())
        main_menu_open_db_btn.grid(row=1, sticky="nsew", padx=20, pady=10)

        main_menu_create_db_btn = CTkButton(self,
                                            text=self.lang.create_db_btn,
                                            command=lambda: CreateDB().mainloop())
        main_menu_create_db_btn.grid(row=2, sticky="nsew", padx=20, pady=10)

        main_menu_show_db_info = CTkButton(self,
                                           text=self.lang.show_db_info,
                                           command=lambda: ShowDBInfo().mainloop())
        main_menu_show_db_info.grid(row=3, sticky="nsew", padx=20, pady=10)

        main_menu_password_generator = CTkButton(self,
                                                 text=self.lang.password_generator,
                                                 command=lambda: PasswordGenerator().mainloop())
        main_menu_password_generator.grid(row=4, sticky="nsew", padx=20, pady=10)

        exit_btn = CTkButton(self,
                             text=self.lang.exit_btn,
                             command=lambda: self.destroy())
        exit_btn.grid(row=5, sticky="nsew", padx=20, pady=10)

    def hide_window(self) -> None:
        """Just hides window"""
        self.withdraw()
