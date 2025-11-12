import bcrypt

hashedPsw=bcrypt.hashpw(b"admin123", bcrypt.gensalt())

USERS_DB={
    "admin":hashedPsw
}