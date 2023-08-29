from .settings import LANGUAGE


class UnsupportedLanguage(ValueError):
    def __init__(self):
        super().__init__("Language that you have selected isn't supported. "
                         "Check 'LANGUAGE' in src/settings.py")


class AppPy:
    def __init__(self, lang=LANGUAGE):
        if lang == 'en':
            self.open_db_btn = "Open database"
            self.create_db_btn = "Create database"
            self.show_db_info = "Show database info"
            self.password_generator = "Password Generator"
            self.exit_btn = "Exit"
        elif lang == 'ru':
            self.open_db_btn = "Открыть базу данных"
            self.create_db_btn = "Создать базу данных"
            self.show_db_info = "Информация о базе данных"
            self.password_generator = "Генератор паролей"
            self.exit_btn = "Выход"
        else:
            raise UnsupportedLanguage


class OpenDBPy:
    def __init__(self, lang=LANGUAGE):
        if lang == 'en':
            # OpenDB
            self.db = "Database"
            self.title = "Database viewer"
            self.select_db_btn = "Select DB"
            self.enter_password_label = "Enter password"
            self.open_db_btn = "Open file"
            self.keyfile_label_part_1 = "Keyfile"
            self.select_file_first = "Select file first"
            self.keyfile_btn = "Select keyfile"
            self.reveal_password = "Reveal password"

            # OpenDB.clear_all
            self.clear_all_msg_title = "Clear?"
            self.clear_all_msg_message = "Do you want to delete all entries?"
            self.clear_all_option_1 = "No"
            self.clear_all_option_3 = "Yes"

            # OpenDB.open_db before opening
            self.master_key_verification_ok = "Master key verification OK."
            self.open_db_msg_title = "Error"
            self.open_db_msg_message = "Master key verification failed. Check your password."
            self.master_key_verification_failed = "Master key verification FAILED."

            # OpenDB.open_db after opening
            self.create_entry_btn = "Create entry"
            self.clear_all_btn = "Clear all"
            self.db_settings_btn = "Database settings"
            self.export_import_btn = "Export/Import entries"
            self.update_btn = "Update"
            self.clear_clipboard = "Clear clipboard"

            self.name_label = "Name"
            self.login_label = "Login"
            self.show_info = "Show"
            self.edit_info = "Edit"
            self.delete_btn = "Delete"
        elif lang == 'ru':
            # OpenDB
            self.db = "База данных"
            self.title = "Просмотр базы данных"
            self.select_db_btn = "Выбрать БД"
            self.enter_password_label = "Введите пароль"
            self.open_db_btn = "Открыть файл"
            self.keyfile_label_part_1 = "Файл-ключ"
            self.select_file_first = "Выберите файл"
            self.keyfile_btn = "Выбрать файл-ключ"
            self.reveal_password = "Показать пароль"

            # OpenDB.clear_all
            self.clear_all_msg_title = "Очистить?"
            self.clear_all_msg_message = "Вы хотите удалить все записи?"
            self.clear_all_option_1 = "Нет"
            self.clear_all_option_3 = "Да"

            # OpenDB.open_db before opening
            self.master_key_verification_ok = "Мастер ключ был успешно верифицирован"
            self.open_db_msg_title = "Ошибка"
            self.open_db_msg_message = "Произошла ошибка во время верификации мастер ключа. Проверьте пароль."

            # OpenDB.open_db after opening
            self.create_entry_btn = "Создать запись"
            self.clear_all_btn = "Очистить всё"
            self.db_settings_btn = "Настройки базы"
            self.export_import_btn = "Экспорт/Импорт записей"
            self.update_btn = "Обновить"
            self.clear_clipboard = "Очистить клавиатуру"

            self.name_label = "Имя"
            self.login_label = "Логин"
            self.show_info = "Информация"
            self.edit_info = "Изменить"
            self.delete_btn = "Удалить"
        else:
            raise UnsupportedLanguage


class PasswordGeneratorPy:
    def __init__(self, lang=LANGUAGE):
        if lang == 'en':
            self.title = "Password Generator"
            self.password_length = "Password length"
            self.lowercase = "Lowercase"
            self.uppercase = "Uppercase"
            self.numbers = "Numbers"
            self.symbols = "Symbols"
            self.generate_password = "Generate password"
            self.copy_password = "Copy password"
            self.symbol_password = "Symbol password"
            self.word_password = "Word password"

            self.msg_box_title = "Error"
            self.msg_box_message = "You need to select at least one parameter"
        elif lang == 'ru':
            self.title = "Генератор паролей"
            self.password_length = "Длина пароля"
            self.lowercase = "Маленькие буквы"
            self.uppercase = "Большие буквы"
            self.numbers = "Цифры"
            self.symbols = "Символы"
            self.generate_password = "Сгенерировать пароль"
            self.copy_password = "Скопировать пароль"
            self.symbol_password = "Символьный пароль"
            self.word_password = "Словесный пароль"

            self.msg_box_title = "Ошибка"
            self.msg_box_message = "Необходимо выбрать как минимум один параметр"
        else:
            raise UnsupportedLanguage


class CreateDBPy:
    def __init__(self, lang=LANGUAGE):
        if lang == 'en':
            self.title = "Database Creation"
            self.db_name = "Name"
            self.db_description = "Description"
            self.password = "Password"
            self.reveal_password = "Reveal password"
            self.kdf_edit = "Edit KDF"
            self.time_cost = "Transform rounds"
            self.memory_cost = "Memory usage"
            self.parallelism = "Parallelism"
            self.salt_size = "Salt size (bytes)"
            self.select_file = "Select file"
            self.filename_label_part_1 = "Database"
            self.filename_label_part_2 = "Select file first"
            self.create_db = "Create database"
            self.add_key_file = "Add key file"
            self.key_file_short_description = "The key file is an additional\n" \
                                              "security measure. If you add it,\n" \
                                              "it will be impossible to open\n" \
                                              "the database without it.\n" \
                                              "P.S. It can be any file"
            self.generate_key_file = "Generate key file"
            self.key_file = "Key file"

            # create_db
            self.msg_box_message = "Database was created successfully"
            self.msg_box_title = "Success"
        elif lang == 'ru':
            self.title = "Создание базы данных"
            self.db_name = "Название"
            self.db_description = "Описание"
            self.password = "Пароль"
            self.reveal_password = "Показать пароль"
            self.kdf_edit = "Изменить KDF"
            self.time_cost = "Циклы преобразования"
            self.memory_cost = "Использование памяти"
            self.parallelism = "Параллелизм"
            self.salt_size = "Размер соли (байт)"
            self.select_file = "Выбрать файл"
            self.filename_label_part_1 = "БД"
            self.filename_label_part_2 = "Выберите файл"
            self.create_db = "Создать базу данных"
            self.add_key_file = "Добавить файл-ключ"
            self.key_file_short_description = "Файл-ключ - дополнительная\n" \
                                              "мера защиты. Если его добавить,\n" \
                                              "без него будет невозможно\n" \
                                              "открыть базу данных\n" \
                                              "P.S. Им может быть любой файл\n"
            self.generate_key_file = "Сгенерировать файл-ключ"
            self.key_file = "Файл-ключ"

            # create_db
            self.msg_box_message = "База данных была успешно создана"
            self.msg_box_title = "Успех"
        else:
            raise UnsupportedLanguage


class CreateEntryPy:
    def __init__(self, lang=LANGUAGE):
        if lang == 'en':
            self.title = "Entry creation"
            self.name_label = "Name"
            self.description_label = "Description"
            self.login_label = "Login"
            self.password_label = "Password"
            self.create_entry = "Create entry"
            self.msg_warning_title = "Warning"
            self.msg_warning_message = "The TOTP key you entered is not in Base32 format. Please check your input"
            self.reveal_password = "Reveal password"
        elif lang == 'ru':
            self.title = "Создание записи"
            self.name_label = "Название"
            self.description_label = "Описание"
            self.login_label = "Логин"
            self.password_label = "Пароль"
            self.create_entry = "Создать запись"
            self.msg_warning_title = "Внимание"
            self.msg_warning_message = "Ключ TOTP, который вы ввели не в формате Base32. Проверьте правильность ввода"
            self.reveal_password = "Показать пароль"
        else:
            UnsupportedLanguage()


class ShowDbInfoPy:
    def __init__(self, lang=LANGUAGE):
        if lang == 'en':
            self.title = "Database info"
            self.open_db = "Open DB"
            self.version = "Version"
            self.name = "Name"
            self.description = "Description"
            self.time_cost = "Transform rounds"
            self.memory_cost = "Memory usage"
            self.parallelism = "Parallelism"
            self.close = "Close"
        elif lang == 'ru':
            self.title = "Информация о БД"
            self.open_db = "Открыть БД"
            self.version = "Версия"
            self.name = "Название"
            self.description = "Описание"
            self.time_cost = "Циклы преобразования"
            self.memory_cost = "Использование памяти"
            self.parallelism = "Параллелизм"
            self.close = "Закрыть"
        else:
            raise UnsupportedLanguage()


class ImportExportDbPy:
    def __init__(self, lang=LANGUAGE):
        if lang == 'en':
            self.title = "Database Import/Export"
            self.export = "Export"
            self.import_ = "Import"
            self.export_name = "Export name"
            self.export_description = "Export description"
            self.export_password = "Export password"
            self.reveal_password = "Reveal password"
            self.kdf_edit = "KDF Edit"
            self.time_cost = "Transform rounds"
            self.memory_cost = "Memory usage"
            self.parallelism = "Parallelism"
            self.salt_size = "Salt size (bytes)"
            self.select_file = "Select file"
            self.select_file_first = "Select file first"
            self.export_database = "Export database"
            self.msg_box_title = "Success"
            self.msg_box_message = "Database was successfully exported"
            self.import_database = "Import database"
            self.uuid_saved_part_1 = "Entry with UUID"
            self.uuid_saved_part_2 = "is already saved in db."
            self.msg_box_error_message = "An error occurred while decryption! Check your password"
            self.msg_box_error_title = "Error"
            self.keyfile_label_part_1 = "Keyfile"
            self.keyfile_btn = "Select keyfile"
            self.generate_key_file = "Generate key file"
        elif lang == 'ru':
            self.title = "Импорт/Экспорт базы данных"
            self.export = "Экспорт"
            self.import_ = "Импорт"
            self.export_name = "Название экспорта"
            self.export_description = "Описание экспорта"
            self.export_password = "Пароль экспорта"
            self.reveal_password = "Показать пароль"
            self.kdf_edit = "Изменение KDF"
            self.time_cost = "Циклы преобразования"
            self.memory_cost = "Использование памяти"
            self.parallelism = "Параллелизм"
            self.salt_size = "Размер соли (байт)"
            self.select_file = "Выбрать файл"
            self.select_file_first = "Выберите файл"
            self.export_database = "Экспорт БД"
            self.msg_box_title = "Успех"
            self.msg_box_message = "База данных была успешно экспортирована"
            self.import_database = "Импортировать БД"
            self.uuid_saved_part_1 = "Запись с UUID"
            self.uuid_saved_part_2 = "уже сохранена в БД."
            self.msg_box_error_message = "Произошла ошибка во время расшифровки. Проверьте пароль"
            self.msg_box_error_title = "Ошибка"
            self.keyfile_label_part_1 = "Файл-ключ"
            self.keyfile_btn = "Выбрать файл-ключ"
            self.generate_key_file = "Сгенерировать файл-ключ"
        else:
            raise UnsupportedLanguage


class ModifyDatabasePy:
    def __init__(self, lang=LANGUAGE):
        if lang == 'en':
            self.title = "Database Editor"
            self.view_db_metadata = "View DB metadata"
            self.modify_db_metadata = "Modify DB metadata"
            self.password_and_kdf = "Password & KDF"
            self.name = "Name"
            self.description = "Description"
            self.time_cost = "Transform rounds"
            self.memory_cost = "Memory usage"
            self.parallelism = "Parallelism"
            self.msg_box_message = "Database metadata was changed successfully"
            self.msg_box_title = "Success"
            self.save = "Save"
            self.msg_box_password_or_kdf_message = "Password/KDF was changed successfully"
            self.msg_box_password_or_kdf_title = "Success"
            self.new_password = "New Password"
            self.reveal_password = "Reveal password"
            self.edit_kdf = "Edit KDF"
            self.salt_size = "Salt size (bytes)"
            self.update_keys_and_kdf = "Update keys & KDF"
            self.keyfile_label_part_1 = "Keyfile"
            self.keyfile_label_part_2 = "Select file first"
            self.keyfile_btn = "Select keyfile"
            self.generate_key_file = "Generate key file"
        elif lang == 'ru':
            self.title = "Редактор базы данных"
            self.view_db_metadata = "Просмотр метаданных БД"
            self.modify_db_metadata = "Изменение метаданных БД"
            self.password_and_kdf = "Пароли и KDF"
            self.name = "Название"
            self.description = "Описание"
            self.time_cost = "Циклы преобразования"
            self.memory_cost = "Использование памяти"
            self.parallelism = "Параллелизм"
            self.msg_box_message = "Метаданные базы данных были успешно изменены"
            self.msg_box_title = "Успех"
            self.save = "Сохранить"
            self.msg_box_password_or_kdf_message = "Пароль/KDF был успешно изменен"
            self.msg_box_password_or_kdf_title = "Успех"
            self.new_password = "Новый пароль"
            self.reveal_password = "Показать пароль"
            self.edit_kdf = "Изменить KDF"
            self.salt_size = "Размер соли (байт)"
            self.update_keys_and_kdf = "Обновить ключи и KDF"
            self.keyfile_label_part_1 = "Файл-ключ"
            self.keyfile_label_part_2 = "Выберите файл"
            self.keyfile_btn = "Выбрать файл-ключ"
            self.generate_key_file = "Сгенерировать файл-ключ"
        else:
            raise UnsupportedLanguage


class ModifyEntryPy:
    def __init__(self, lang=LANGUAGE):
        if lang == 'en':
            self.title = "Entry modification"
            self.name = "Name"
            self.description = "Description"
            self.login = "Login"
            self.password = "Password"
            self.save = "Save"
            self.reveal_password = "Reveal password"
        elif lang == 'ru':
            self.title = "Изменение записи"
            self.name = "Название"
            self.description = "Описание"
            self.login = "Логин"
            self.password = "Пароль"
            self.save = "Сохранить"
            self.reveal_password = "Показать пароль"
        else:
            raise UnsupportedLanguage


class ShowInfoPy:
    def __init__(self, lang=LANGUAGE):
        if lang == 'en':
            self.title = "Entry info"
            self.name = "Name"
            self.description = "Description"
            self.login = "Login"
            self.password = "Password"
            self.reveal_password = "Reveal password"
            self.copy = "Copy"
            self.copy_name = "Copy name"
            self.copy_description = "Copy description"
            self.copy_login = "Copy login"
            self.copy_password = "Copy password"
            self.copy_totp = "Copy TOTP"
            self.msg_box_title = "Error"
            self.totp_error = "Error. TOTP key was saved in invalid format"
        elif lang == 'ru':
            self.title = "Информация о записи"
            self.name = "Название"
            self.description = "Описание"
            self.login = "Логин"
            self.password = "Пароль"
            self.reveal_password = "Показать пароль"
            self.copy = "Скопировать"
            self.copy_name = "Скопировать название"
            self.copy_description = "Скопировать описание"
            self.copy_login = "Скопировать логин"
            self.copy_password = "Скопировать пароль"
            self.copy_totp = "Скопировать TOTP"
            self.totp_error = "Ошибка. Ключ TOTP сохранен в неверном формате"
        else:
            raise UnsupportedLanguage


class KeyFileGeneratorPy:
    def __init__(self, lang=LANGUAGE):
        if lang == 'en':
            self.title = "Key file generator"
            self.random_bytes = "Random bytes"
            self.random_cat = "Random cat"
            self.random_cats = "A lot of random cats"
            # self.one_random_cat_photo = "It will download 1 random cat photo"
            self.file_label = "File"
            self.select_file_first = "Select file first"
            self.select_file = "Select file"
            self.download_photo = "Download photo"
            self.msg_box_title = "Success"
            self.msg_box_message = "Cat photo was successfully downloaded :3"
            self.amount_of_cats = "Amount of cats"
            self.catsfolder = "Folder where to download cats"
            self.select_folder_first = "Select folder first"
            self.download_cats = "Download cats"
            self.select_folder = "Select folder"
            self.msg_box_cats_message = "Cat photos were successfully downloaded :3"
            self.from_bytes = "Minimal amount of bytes"
            self.to_bytes = "Maximal amount of bytes"
            self.create_file = "Create file"
            self.msg_box_bytes_message = "Random bytes were successfully written"
        elif lang == 'ru':
            self.title = "Генератор ключ-файлов"
            self.random_bytes = "Случайные байты"
            self.random_cat = "Случайный кот"
            self.random_cats = "Много случайных котов"
            # self.one_random_cat_photo = "Оно скачает 1 случайное фото кота"
            self.file_label = "Файл"
            self.select_file_first = "Выберите файл"
            self.select_file = "Выбрать файл"
            self.download_photo = "Скачать фото"
            self.msg_box_title = "Успех"
            self.msg_box_message = "Фото кота было успешно загружено :3"
            self.amount_of_cats = "Количество котов"
            self.catsfolder = "Папка, куда скачивать котов"
            self.select_folder_first = "Сначала выберите папку"
            self.download_cats = "Скачать котов"
            self.select_folder = "Выбрать папку"
            self.msg_box_cats_message = "Фотографии котов были успешно загружены :3"
            self.from_bytes = "Минимальное кол-во байтов"
            self.to_bytes = "Максимальное кол-во байтов"
            self.create_file = "Создать файл"
            self.msg_box_bytes_message = "Случайные байты были успешно записаны"
        else:
            raise UnsupportedLanguage
