# Security documentation

## Database scheme
File extension: .pbdb

Type: sqlite3

Tables: _db_header_, _db_storage_

KDF: Argon2ID

DB Header contains database metadata and encrypted master key.

DB Header: _version, database name, database description, argon2id time cost, argon2id memory cost, argon2id parallelism,
salt and encrypted master key_

DB storage contains all entries. Entries are encrypted with master key. The only thing that isn't
encrypted in db storage is uuid. But since it uses uuid4 it doesn't contain metadata and absolutely random.

DB storage: _uuid, name, description, login, password, is totp_

File where database is being created: _create_db.py_
## KDF

Obtaining key for decryption master key without key file:

_Argon2ID(password, salt)_

With key file:

_Argon2ID(password+key_file_contents, salt)_

The key file is an additional security measure. If you add it, it will be impossible to open the database without it.
P.S. It can be any file

Default KDF parameters are located in _settings.py_

## Export/Import
You can export/import your database in json format. Export/Import also contains header and storage. But with one difference,
there isn't master key. Everything is encrypted with export password (could be different from your db password) 
with/o key file.

Handles export/import (both gui and backend): _import_export_db.py_

## Encryption
Everything that need to be encrypted - encrypts with AES EAX with nonce and tag for authentication. 

Handles encryption operations: _pb_crypto.py_

## Password generator
Password generator support 2 modes: symbol password and word password.

![Thanks for XKCD for idea of creation word password](https://imgs.xkcd.com/comics/password_strength.png)

Symbol password can be configured with switches (uppercase, lowercase, digits, symbols)

There is 2 supported languages for generating word password: english and russian

For generating random passwords it uses in-built _secrets_ library

## Generating key file
If you want to increase security of your database consider adding key file. But if you can't select key file you can simply
generate it.

Since key file could be any file there is 3 options in generating key file:
random bytes, 1 random cat image, a lot of cats images (amount of cats can be easily edited with slider)
