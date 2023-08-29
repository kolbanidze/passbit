from customtkinter import CTkToplevel, CTkSlider, CTkLabel, CTkEntry,\
    BooleanVar, CTkSwitch, CTkFrame, CTkButton, CTkSegmentedButton, CTkOptionMenu, StringVar
from string import ascii_lowercase, ascii_uppercase, digits, punctuation
from secrets import choice
from CTkMessagebox import CTkMessagebox
from pyperclip import copy as clipboard_copy
from .language import PasswordGeneratorPy
from pkg_resources import resource_filename


class PasswordGenerator(CTkToplevel):
    """Password generator that uses secrets library"""
    def __init__(self):
        super().__init__()
        self.lang = PasswordGeneratorPy()
        self.title(self.lang.title)

        self.segmented_button = CTkSegmentedButton(self,
                                                   values=[self.lang.symbol_password,
                                                           self.lang.word_password],
                                                   command=self.segmented_button_handler)
        self.segmented_button.set(self.lang.symbol_password)
        self.segmented_button.grid(row=0)
        self.active_frame = CTkFrame(self)
        self.active_frame.columnconfigure(0, weight=1)
        self.active_frame.grid(row=1, sticky="nsew")

        self.symbol_password()

    def symbol_password(self):
        self.password_length_label = CTkLabel(self.active_frame, text=f"{self.lang.password_length}: 1")
        self.password_length_label.grid(row=0)

        self.slider = CTkSlider(self.active_frame, from_=1, to=128, command=self.slider_handler)
        self.slider.set(1)
        self.slider.grid(row=1, pady=10)

        self.password_entry = CTkEntry(self.active_frame, state="disabled", width=200)
        self.password_entry.grid(row=2, pady=10)

        config_frame = CTkFrame(self.active_frame)

        self.lowercase = BooleanVar(value=False)
        lowercase_switch = CTkSwitch(config_frame, text=self.lang.lowercase, variable=self.lowercase,
                                     onvalue=True, offvalue=False)

        self.uppercase = BooleanVar(value=False)
        uppercase_switch = CTkSwitch(config_frame, text=self.lang.uppercase, variable=self.uppercase,
                                     onvalue=True, offvalue=False)

        self.numbers = BooleanVar(value=False)
        numbers_switch = CTkSwitch(config_frame, text=self.lang.numbers, variable=self.numbers,
                                   onvalue=True, offvalue=False)

        self.symbols = BooleanVar(value=False)
        symbols_switch = CTkSwitch(config_frame, text=self.lang.symbols, variable=self.symbols,
                                   onvalue=True, offvalue=False)

        generate_pass_btn = CTkButton(self.active_frame, text=self.lang.generate_password,
                                      command=lambda: self.generate_password())
        copy_password = CTkButton(self.active_frame, text=self.lang.copy_password,
                                  command=lambda: self.copy_password())

        lowercase_switch.grid(row=0, column=0, padx=20, pady=10)
        uppercase_switch.grid(row=0, column=1, padx=20, pady=10)
        numbers_switch.grid(row=1, column=0, padx=20, pady=10)
        symbols_switch.grid(row=1, column=1, padx=20, pady=10)
        config_frame.grid(row=3, pady=10)
        generate_pass_btn.grid(row=4, pady=10)
        copy_password.grid(row=5, pady=10)

    def word_password(self):
        """https://xkcd.com/936/"""
        self.password_length_label = CTkLabel(self.active_frame, text=f"{self.lang.password_length}: 1")
        self.password_length_label.grid(row=0, padx=10)

        self.slider = CTkSlider(self.active_frame, from_=1, to=32, command=self.slider_handler)
        self.slider.set(1)
        self.slider.grid(row=1, padx=10, pady=10)

        self.password_entry = CTkEntry(self.active_frame, state="disabled", width=200)
        self.password_entry.grid(row=2, pady=10)

        self.language_var = StringVar(value="English")
        languages = CTkOptionMenu(self.active_frame,
                                  values=["English",
                                          "Russian"],
                                  variable=self.language_var,
                                  command=self.language_handler)
        languages.grid(row=3, pady=10)

        generate_pass_btn = CTkButton(self.active_frame, text=self.lang.generate_password,
                                      command=lambda: self.generate_word_password())
        copy_password = CTkButton(self.active_frame, text=self.lang.copy_password,
                                  command=lambda: self.copy_password())

        generate_pass_btn.grid(row=4, pady=10)
        copy_password.grid(row=5, pady=10)

    def language_handler(self, value):
        self.language_var.set(value)

    def generate_word_password(self):
        self.password_entry.configure(state="normal")
        self.password_entry.delete(0, 'end')
        language = self.language_var.get()
        amount_of_words = int(self.slider.get())
        password = PasswordGenerator.random_words(language, amount_of_words)
        self.password_entry.insert(0, password)
        self.password_entry.configure(state="disabled")

    @staticmethod
    def random_words(language: str,
                     amount_of_words: int) -> str:
        assert language == 'English' or language == 'Russian', "Language that you have selected isn't supported"

        word_file = resource_filename('passbit', f'words/{language.lower()}_words_10k.txt')
        with open(word_file, 'r') as file:
            words_list = file.read().split()

        words = []
        while len(words) != amount_of_words:
            word = choice(words_list)
            if len(word) > 5:
                words.append(word)
        return ' '.join(words)

    def slider_handler(self, value):
        """Handles slider. Changes password length label"""
        self.password_length_label.configure(text=f"{self.lang.password_length}: {int(value)}")

    def generate_password(self):
        """Generates password and inserts it into password entry"""
        password = ''
        password_symbols = ''

        if self.lowercase.get():
            password_symbols += ascii_lowercase
        if self.uppercase.get():
            password_symbols += ascii_uppercase
        if self.numbers.get():
            password_symbols += digits
        if self.symbols.get():
            password_symbols += punctuation

        if len(password_symbols) != 0:
            for _ in range(int(self.slider.get())):
                password += choice(password_symbols)
            self.password_entry.configure(state="normal")
            self.password_entry.delete(0, "end")
            self.password_entry.insert(0, password)
            self.password_entry.configure(state="disabled")
        else:
            CTkMessagebox(icon="cancel", title=self.lang.title, message=self.lang.msg_box_message)

    def clear_active_frame(self) -> None:
        for widget in self.active_frame.winfo_children():
            widget.destroy()

    def copy_password(self) -> None:
        """Just copies password to clipboard"""
        clipboard_copy(self.password_entry.get())

    def segmented_button_handler(self, value) -> None:
        self.clear_active_frame()
        if value == self.lang.symbol_password:
            self.symbol_password()
        elif value == self.lang.word_password:
            self.word_password()
