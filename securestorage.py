# Created by Zack Wagner
# 3/10/2022

from os.path import exists
from json import dumps, loads

# PyCryptodome 3.14.1
from Crypto.Cipher import AES
from Crypto.Hash import SHA512
from Crypto.Protocol.KDF import HKDF
from Crypto.Util.Padding import pad, unpad


'''
Raised upon opening a vault file that does not start with the correct magic bytes
'''
class BadVaultFile(Exception):
    def __init__(self, path):
        super().__init__(f'Incorrect or corrupt vault file at {path}')


'''
Raised upon decryption failure for any reason
'''
class DecryptionError(Exception):
    def __init__(self):
        super().__init__(f'Vault decryption failed, check password or file')


'''
Secure password storage object
Encrypts password library with AES-256-CBC using HKDF based key from user input
'''
class Vault():

    # TODO improve corrupt vault detection
    def __init__(self, passwd, path="vault.bin", overwrite=False):
        '''
        Secure password vault object, stored in an encrypted binary file

        Parameters
        ----------
        passwd : str
            Password to encrypt/decrypt this vault
        path : str
            Path to vault file
        overwrite : bool
            If true, does not read vault file if it already exists

        Raises
        ------
        BadVaultFile
            Raised when vault file does not start with magic bytes ACED
            Used to prevent people from trying to load non-vault files
        DecryptionError
            Raised when AES decryption fails for any reason
            Usually is an incorrect password, but could indicate corrupt file
        '''
        self.path = path
        self.__passwd = passwd.encode('utf-8')

        if exists(path) and not overwrite:
            self.__data = self.__decrypt(self.__passwd)

            if not self.__data:
                raise DecryptionError

        else:
            self.__data = {}


    # TODO add password class
    def add_creds(self, site, username, password):
        '''
        Add credentials for a specific site
        Currently only supports one set of credentials per site string

        Parameters
        ----------
        site : str
            Site credentials are associated with
        username: str
            Username to site
        password: str
            Password to site
        '''
        self.__data[site] = [
            username,
            password
        ]

    
    def del_creds(self, site):
        '''
        Deletes credentials from database for a specific site

        Parameters
        ----------
        site : str
            Site to delete credentials for

        Returns
        -------
        bool
            True if site credentials exist and were deleted
        '''
        try:
            del self.__data[site]
        
        except KeyError:
            return False
        
        else:
            return True
        

    def get_creds(self, site):
        '''
        Gets credentials from database for a certain site

        Parameters
        ----------
        site : str
            Site to get credentials for

        Returns
        -------
        tuple
            (username, password), empty tuple if credentials not found
        '''
        return tuple(self.__data.get(site, []))


    # TODO Add search function within?
    def list_creds(self):
        '''
        Lists site names stored within database

        Returns
        -------
        list
            list of site name strings
        '''
        return list(self.__data.keys())


    def write(self):
        '''
        Write database changes to encrypted file
        '''
        self.__encrypt(self.__passwd)


    # TODO better way of checking if vault is new or not
    def is_empty(self):
        '''
        Checks if vault contains any credentials

        Returns
        -------
        bool
            True if vault is empty
        '''
        return True if len(self.__data) == 0 else False


    def __encrypt(self, passwd):
        f = open(self.path, 'wb')

        plaintext = pad(dumps(self.__data, separators=(',',':')).encode('utf-8'), AES.block_size)

        key = HKDF(passwd, 16, b'', SHA512)
        cipher = AES.new(key, AES.MODE_CBC)

        ciphertext = cipher.encrypt(plaintext)

        f.write(b'\xAC\xED')
        f.write(cipher.iv)
        f.write(ciphertext)

        f.close()


    def __decrypt(self, passwd):
        f = open(self.path, 'rb')

        if (f.read(2) != b'\xAC\xED'):
                raise BadVaultFile(self.path)
        
        iv = f.read(16)
        ciphertext = f.read()

        key = HKDF(passwd, 16, b'', SHA512)
        cipher = AES.new(key, AES.MODE_CBC, iv)

        try:
            return loads(unpad(cipher.decrypt(ciphertext), AES.block_size))

        except:
            return False


# Example program
if __name__ == "__main__":
    from os import remove

    try:
        my_vault = Vault('superpasswdord123', "testvault.bin")

    except BadVaultFile:
        print("Error opening vault file.")

    except DecryptionError:
        print("Possible incorrect password")


    if my_vault.is_empty():
        print("Vault is empty, writing example credentials")

        my_vault.add_creds("test1.com", "joe", "password1")
        my_vault.add_creds("test2.org", "bob", "password2")
        my_vault.add_creds("test3.net", "steve", "password3")

        my_vault.write()
        print("Written to disk as ./testvault.bin")
        print("Restart program to load file")

    else:
        print("Vault found, opening vault\n")

        p1 = my_vault.get_creds("test1.com")
        p2 = my_vault.get_creds("test2.org")
        p3 = my_vault.get_creds("test3.net")

        print('Credentials for test1.com')
        print(f'Username: {p1[0]}')
        print(f'Password: {p1[1]}\n')

        print('Credentials for test2.com')
        print(f'Username: {p2[0]}')
        print(f'Password: {p2[1]}\n')
        
        print('Credentials for test3.com')
        print(f'Username: {p3[0]}')
        print(f'Password: {p3[1]}')

        print("Delete example vault file? [y/N]")
        if input('> ').lower() == "y":
            remove("testvault.bin")
