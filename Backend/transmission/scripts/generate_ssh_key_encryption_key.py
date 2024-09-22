import environ
from cryptography.fernet import Fernet


env = environ.Env()
environ.Env.read_env()

# Generate a key
key = Fernet.generate_key()

print("Write the following key to the .env file in transmission/.env please. Remove the 'b'")
print(key)