import hashlib
import string

ALPHABET = list(string.ascii_lowercase)

# salt and hash as password in sha256, with a number of iteration equal to the password lenght
def hash_password(password:str) -> str:
    """
    Hash the password a number of time taht is equal to its lenght.
    The password will first be salted.
    Args:
        - password (str) : password that will bge salted and hashed.

    Returns the hexdigest (str format) hashed password.
    """
    # Generate a salt from the password
    salt = ''.join([str(ALPHABET.index(char)) for char in password.lower() if char in ALPHABET])
    for _ in range((len(password) % 3 + 5) * 100 + 150):
        password = salt + password + salt
        password = hashlib.sha256(password.encode()).hexdigest()
    return password



# test function
if __name__ == '__main__':
    password = input('password : ')

    # checks if the hashing function gives the same result for the same password
    print(hash_password(password))
    print(hash_password(password))

