# Passbit documentation

## Main menu
At main menu you can _open db, create db, show db info, generate password_ and _exit_.

_app.py_

## DB Creation
• On the left there are 'select file', 'create database', 'add key file' and 'generate key file' buttons. And text that shows
which database/key file you have selected.

'Select file' - shows filedialog where you need to select file where will be saved passbit database

'Create database' - creates database ¯\_(ツ)_/¯. Button enables only when you select database.

'Add key file' - adds key file to database.

The key file is an additional security measure. If you add it, it will be impossible to open the database without it. It can be any file

'Generate key file' - shows generate key file menu (_key_file_generator.py_)

• On the right there is _name, description and password_ entries. By default all passwords in passbits are
hidden, so there is 'Reveal password' checkbox. 

If you want to edit KDF parameters you need to 
turn on 'KDF Edit' switch and then you can write your parameters.

_create_db.py_

## Show database info
When you click 'Open DB' button you will be prompted to select database. After that it will show
all unencrypted db header parameters.

_show_db_info.py_

## Generate password
It supports 2 modes: symbol password and word password. Word password supports 2 languages: english and russian.
![Thanks for XKCD for idea of creation word password](https://imgs.xkcd.com/comics/password_strength.png)

Symbol password can be configured with switches (uppercase, lowercase, digits, symbols)

You can select password length/amount of words with slider.
P.S. minimal word length - 5 symbols.

_password_generator.py_

## Open DB
Opens db ¯\_(ツ)_/¯

First menu:

Shows 'Select DB', 'Select keyfile' and 'Open DB' buttons and which db/keyfile you have selected.
Prompts you to enter password.

After opening (decrypting) database shows second menu (database viewer).

Second menu:

On the left side there are '_Create entry', 'Clear all', 'Database settings', 'Export/Import entries', and 'Clear clipboard'_ buttons

On the right side there are entries. Every entry has 'Show', 'Edit' and 'Delete' buttons.

## Entry creation
Prompts you to enter name, description, login and password. If password is totp key you need to turn on "TOTP" switch.

_create_entry.py_

## Clear all
Clears all entries in database

_OpenDB.clear_all()_

## Database settings
Shows menu where you can view/edit database metadata and change Password/KDF/Keyfile

_modify_database.py_

## Export/Import entries
Shows menu where you can export/import entries in json. All exported entries are encrypted. You 
can't import entry if there is already such entry in your database.

_import_export_db.py_

## Clear clipboard
Just clears clipboard. Idk what to write here else

_OpenDB.clear_clipboard()_

## Exit

_OpenDB.exit()_
