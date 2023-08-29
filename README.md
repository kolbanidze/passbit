# Passbit
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Known Vulnerabilities](https://snyk.io/test/github/kolbanidze/passbit/badge.svg)](https://snyk.io/test/github/kolbanidze/passbit)
[![PyPI version](https://badge.fury.io/py/PassBit.svg)](https://badge.fury.io/py/PassBit)



# Security
## Storing secrets
Valuable data (_name, description, login, password, totp_) is encrypted (AES 256-bit, EAX) in database storage. To open database you need to
enter password or/and key file.

KDF: Argon2ID

## Libraries
GUI: **CustomTkinter**, **CTkMessageBox**

Encryption/KDF: **argon2-cffi**, **PyCryptoDome**

TOTP: **pyotp**

For copying secrets to clipboard: **pyperclip**

For getting cat's images: **requests**

### Full documentation is available in docs directory

# Installation
```
pip install passbit
python -m passbit
```
