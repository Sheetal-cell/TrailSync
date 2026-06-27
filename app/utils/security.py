from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

def hash_password(password):
    """
    Converts plain password into hashed password.
    """
    return generate_password_hash(password)

def verify_password(hashed_password, password):
    """
    Verifies entered password.
    """
    return check_password_hash(hashed_password, password)