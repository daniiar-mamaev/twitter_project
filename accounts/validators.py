import re

special_symbols = set('~`!@#$%^&*()_-+={[}]|\:;<,>.?/')


def password_validation(password):
    if len(password) < 8:
        return False
    elif not any(char.isdigit() for char in password):
        return False
    elif re.search('[A-Z]', password) is None:
        return False
    elif re.search('[a-z]', password) is None:
        return False
    elif not special_symbols.intersection(password):
        return False
    return True
