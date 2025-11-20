from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

async def verify_password(input_password: str, hashed_password: str):
    return password_hash.verify(input_password, hashed_password)

async def get_hashed_password(password: str):
    return password_hash.hash(password)