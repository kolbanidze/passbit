from customtkinter import CTkToplevel, CTkSegmentedButton, CTkFrame, CTkLabel, CTkButton, \
    CTkSlider, CTkEntry, CTkFont
from .language import KeyFileGeneratorPy
from tkinter.filedialog import asksaveasfile, askdirectory
from requests import get
from json import loads as json_decode
from .settings import THE_CAT_API_URL
from CTkMessagebox import CTkMessagebox
from os.path import basename, join
from uuid import uuid4
from secrets import token_bytes, choice


class KeyFileGenerator(CTkToplevel):
    def __init__(self):
        super().__init__()
        self.lang = KeyFileGeneratorPy()
        self.amount_of_cats = 1
        self.title(self.lang.title)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.segmented_button = CTkSegmentedButton(self,
                                                   values=[self.lang.random_bytes,
                                                           self.lang.random_cat,
                                                           self.lang.random_cats],
                                                   command=self.segmented_button_handler)
        self.segmented_button.set(self.lang.random_cat)
        self.segmented_button.grid(row=0)
        self.active_frame = CTkFrame(self)

        self.active_frame.grid(row=1, sticky="nsew")
        self.random_cat()

    def random_cat(self):
        self.file_label = CTkLabel(self.active_frame,
                              text=f"{self.lang.file_label}: {self.lang.select_file_first}")
        self.file_label.pack(pady=10, padx=10)
        select_file_btn = CTkButton(self.active_frame,
                                    text=self.lang.select_file,
                                    command=lambda: self.random_cat_filedialog())
        select_file_btn.pack(pady=10, padx=10)

        self.download_photo = CTkButton(self.active_frame,
                                        text=self.lang.download_photo,
                                        state="disabled",
                                        command=lambda: self.download_cat_photo(self.cat_path))
        self.download_photo.pack(pady=10, padx=10)

    def random_cats(self):
        self.amount_of_cats_label = CTkLabel(self.active_frame,
                                             text=f"{self.lang.amount_of_cats}: {self.amount_of_cats}")
        self.amount_of_cats_label.pack(padx=10, pady=10)
        self.slider = CTkSlider(self.active_frame, from_=1, to=128,
                                command=self.slider_handler)
        self.slider.set(self.amount_of_cats)
        self.slider.pack(padx=10, pady=10)

        self.folder_label = CTkLabel(self.active_frame,
                                     text=f"{self.lang.catsfolder}: {self.lang.select_folder_first}")
        self.folder_label.pack(padx=10, pady=10)

        select_folder = CTkButton(self.active_frame,
                                  text=self.lang.select_folder,
                                  command=lambda: self.select_folder_filedialog())
        select_folder.pack(padx=10, pady=10)

        self.download_cats_btn = CTkButton(self.active_frame,
                                           text=self.lang.download_cats,
                                           command=lambda: self.download_cats(),
                                           state="disabled")
        self.download_cats_btn.pack(padx=10, pady=10)

    def select_folder_filedialog(self):
        directory = askdirectory()
        # Checking if db file was selected
        if directory is not tuple:
            self.cat_dir = directory

            self.download_cats_btn.configure(state="normal")
            self.folder_label.configure(text=f"{self.lang.catsfolder}: {basename(self.cat_dir)}",
                                        font=CTkFont(underline=True))
        self.lift()

    def download_cats(self):
        for _ in range(self.amount_of_cats):
            # extension will be added
            self.download_cat_photo(cat_path=join(self.cat_dir, str(uuid4())),
                                    show_success_message=False)
        CTkMessagebox(icon="check",
                      title=self.lang.msg_box_title,
                      message=self.lang.msg_box_cats_message)

    def random_cat_filedialog(self):
        files = [('Photo', '.jpg'), ('All files', '*.*')]
        file = asksaveasfile(filetypes=files)
        # Checking if file was selected
        if locals()['file'] is not None:
            self.cat_path = file.name

            self.download_photo.configure(state="normal")
            self.file_label.configure(text=f"{self.lang.file_label}: {basename(self.cat_path)}",
                                      font=CTkFont(underline=True))
        self.lift()

    def download_cat_photo(self, cat_path: str, show_success_message: bool = True):
        cat_json = get(THE_CAT_API_URL).content
        cat_photo_url = json_decode(cat_json)[0]['url']
        extension = cat_photo_url.split('.')[-1]
        cat_photo = get(cat_photo_url).content

        full_cat_path = cat_path + f'.{extension}'

        with open(full_cat_path, 'bw') as file:
            file.write(cat_photo)

        if show_success_message:
            CTkMessagebox(icon="check",
                          title=self.lang.msg_box_title,
                          message=self.lang.msg_box_message)

    def clear_active_frame(self) -> None:
        for widget in self.active_frame.winfo_children():
            widget.destroy()

    def segmented_button_handler(self, value):
        self.clear_active_frame()
        if value == self.lang.random_bytes:
            self.random_bytes()
        elif value == self.lang.random_cat:
            self.random_cat()
        elif value == self.lang.random_cats:
            self.random_cats()

    def slider_handler(self, value):
        self.amount_of_cats = int(value)
        self.amount_of_cats_label.configure(text=f"{self.lang.amount_of_cats}: {self.amount_of_cats}")

    def random_bytes(self):
        from_bytes_label = CTkLabel(self.active_frame, text=self.lang.from_bytes)
        self.from_bytes_entry = CTkEntry(self.active_frame)

        to_bytes_label = CTkLabel(self.active_frame, text=self.lang.to_bytes)
        self.to_bytes_entry = CTkEntry(self.active_frame)

        from_bytes_label.grid(row=0, column=0, padx=15, pady=10)
        self.from_bytes_entry.grid(row=0, column=1, padx=15, pady=10)
        to_bytes_label.grid(row=1, column=0, padx=15, pady=10)
        self.to_bytes_entry.grid(row=1, column=1, padx=15, pady=10)

        self.file_label = CTkLabel(self.active_frame, text=f"{self.lang.file_label}: {self.lang.select_file_first}")
        file_select_btn = CTkButton(self.active_frame,
                                    text=self.lang.select_file,
                                    command=lambda: self.select_random_file())
        self.file_label.grid(row=2, column=0, padx=15, pady=10)
        file_select_btn.grid(row=2, column=1, padx=15, pady=10)

        self.create_random_bytes = CTkButton(self.active_frame,
                                             text=self.lang.create_file,
                                             state="disabled",
                                             command=lambda: self.write_random_bytes_to_file())
        self.create_random_bytes.grid(row=3, column=1, padx=15, pady=10)

    def select_random_file(self):
        files = [('Binary file', '.bin'), ('All files', '*.*')]
        file = asksaveasfile(filetypes=files)
        if locals()['file'] is not None:
            self.random_file_path = file.name
            filename = basename(self.random_file_path)

            self.file_label.configure(text=f"{self.lang.file_label}: {filename}", font=CTkFont(underline=True))
            self.create_random_bytes.configure(state="normal")
        self.lift()

    def write_random_bytes_to_file(self):
        min_bytes = int(self.from_bytes_entry.get())
        max_bytes = int(self.to_bytes_entry.get())
        assert max_bytes > min_bytes, "Minimal amount of bytes must be less that max amount of bytes"
        with open(self.random_file_path, 'bw') as file:
            file.write(token_bytes(choice(range(min_bytes, max_bytes))))

        CTkMessagebox(icon="check",
                      title=self.lang.msg_box_title,
                      message=self.lang.msg_box_bytes_message)
