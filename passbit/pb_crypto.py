from Crypto.Cipher import AES


class DecryptionFailed(ValueError):
    def __init__(self):
        super().__init__("An error occurred while decryption. Check your password")


class PBCrypto:
    """Class that handles most of cryptographic operations of PassBit"""
    @staticmethod
    def encrypt_by_dict(master_key: bytes, dictionary: dict) -> dict:
        """Gets {"uuid": "str",
        "name": "bytes | str",
        "description": "bytes | str",
        "login": "bytes | str",
        "password": "bytes | str",
        "is_totp": "bytes | str"}

        Returns {"uuid": "str",
        "name": "bytes",
        "description": "bytes",
        "login": "bytes",
        "password": "bytes",
        "is_totp": "bytes"}"""

        if type(dictionary['name']) is str:
            dictionary['name'] = dictionary['name'].encode('utf-8')
        cipher = AES.new(master_key, AES.MODE_EAX)
        name_nonce = cipher.nonce
        name, name_tag = cipher.encrypt_and_digest(dictionary['name'])

        if type(dictionary['description']) is str:
            dictionary['description'] = dictionary['description'].encode('utf-8')
        cipher = AES.new(master_key, AES.MODE_EAX)
        description_nonce = cipher.nonce
        description, description_tag = cipher.encrypt_and_digest(dictionary['description'])

        if type(dictionary['login']) is str:
            dictionary['login'] = dictionary['login'].encode('utf-8')
        cipher = AES.new(master_key, AES.MODE_EAX)
        login_nonce = cipher.nonce
        login, login_tag = cipher.encrypt_and_digest(dictionary['login'])

        if type(dictionary['password']) is str:
            dictionary['password'] = dictionary['password'].encode('utf-8')
        cipher = AES.new(master_key, AES.MODE_EAX)
        password_nonce = cipher.nonce
        password, password_tag = cipher.encrypt_and_digest(dictionary['password'])

        if type(dictionary['is_totp']) is str:
            dictionary['is_totp'] = dictionary['is_totp'].encode('utf-8')
        cipher = AES.new(master_key, AES.MODE_EAX)
        is_totp_nonce = cipher.nonce
        is_totp, is_totp_tag = cipher.encrypt_and_digest(dictionary['is_totp'])

        encrypted_name = name_nonce + name_tag + name
        encrypted_description = description_nonce + description_tag + description
        encrypted_login = login_nonce + login_tag + login
        encrypted_password = password_nonce + password_tag + password
        encrypted_is_totp = is_totp_nonce + is_totp_tag + is_totp

        return {'uuid': dictionary['uuid'],
                'name': encrypted_name,
                'description': encrypted_description,
                'login': encrypted_login,
                'password': encrypted_password,
                'is_totp': encrypted_is_totp}

    @staticmethod
    def decrypt_by_list(master_key: bytes, enc_list: list) -> dict:
        """Gets ['uuid', b'name', b'description', b'login', b'password', b'is_totp']

        Returns {"uuid": "str",
        "name": "bytes",
        "description": "bytes",
        "login": "bytes",
        "password": "bytes",
        "is_totp": "bytes"}"""

        uuid = enc_list[0]
        name = enc_list[1]
        description = enc_list[2]
        login = enc_list[3]
        password = enc_list[4]
        is_totp = enc_list[5]
        return PBCrypto.decrypt_by_dict(master_key,
                                        {'uuid': uuid,
                                         'name': name,
                                         'description': description,
                                         'login': login,
                                         'password': password,
                                         'is_totp': is_totp})

    @staticmethod
    def decrypt_by_dict(master_key: bytes, dictionary: dict) -> dict:
        """Gets {"uuid": "str",
        "name": "bytes",
        "description": "bytes",
        "login": "bytes",
        "password": "bytes",
        "is_totp": "bytes"}

        Returns {"uuid": "str",
        "name": "bytes | str",
        "description": "bytes | str",
        "login": "bytes | str",
        "password": "bytes | str",
        "is_totp": "bytes | str"}"""

        name_nonce, name_tag, name = dictionary['name'][:16], \
            dictionary['name'][16:32], \
            dictionary['name'][32:]

        description_nonce, description_tag, description = dictionary['description'][:16], \
            dictionary['description'][16:32], \
            dictionary['description'][32:]

        login_nonce, login_tag, login = dictionary['login'][:16], \
            dictionary['login'][16:32], \
            dictionary['login'][32:]

        password_nonce, password_tag, password = dictionary['password'][:16], \
            dictionary['password'][16:32], \
            dictionary['password'][32:]

        is_totp_nonce, is_totp_tag, is_totp = dictionary['is_totp'][:16], \
            dictionary['is_totp'][16:32], \
            dictionary['is_totp'][32:]

        cipher = AES.new(master_key, AES.MODE_EAX, nonce=name_nonce)
        plaintext_name = cipher.decrypt(name)
        try:
            cipher.verify(name_tag)
        except ValueError:
            raise DecryptionFailed

        cipher = AES.new(master_key, AES.MODE_EAX, nonce=description_nonce)
        plaintext_description = cipher.decrypt(description)
        try:
            cipher.verify(description_tag)
        except ValueError:
            raise DecryptionFailed

        cipher = AES.new(master_key, AES.MODE_EAX, nonce=login_nonce)
        plaintext_login = cipher.decrypt(login)
        try:
            cipher.verify(login_tag)
        except ValueError:
            raise DecryptionFailed

        cipher = AES.new(master_key, AES.MODE_EAX, nonce=password_nonce)
        plaintext_password = cipher.decrypt(password)
        try:
            cipher.verify(password_tag)
        except ValueError:
            raise DecryptionFailed

        cipher = AES.new(master_key, AES.MODE_EAX, nonce=is_totp_nonce)
        plaintext_is_totp = cipher.decrypt(is_totp)
        try:
            cipher.verify(is_totp_tag)
        except ValueError:
            raise DecryptionFailed

        return {'uuid': dictionary['uuid'],
                'name': plaintext_name.decode('utf-8'),
                'description': plaintext_description.decode('utf-8'),
                'login': plaintext_login.decode('utf-8'),
                'password': plaintext_password.decode('utf-8'),
                'is_totp': plaintext_is_totp.decode('utf-8')}
