"""
| basic form input validation
"""
import re

__author__ = "Itai Dotan"


def check_form_data(user_id, psw, email, f_name, l_name, gender):
    """
    | used to check for valid register info validity
    :param user_id: the user to check
    :param psw: the password to be validated
    :param email: the E-mail to be validated
    :param f_name: the first name to be validated
    :param l_name: the last name to be validated
    :param gender: the gender to be validated
    :return: True when valid
    """
    if len(user_id) < 5:
        return False
    if not valid_user(user_id):
        return False
    if not valid_psw(psw):
        return False
    if gender != "1" and gender != "2":
        return False
    if not valid_email(email):
        return False
    if not valid_name_string(f_name):
        return False
    if not valid_name_string(l_name):
        return False
    return True


def valid_user(user):
    """
    | validate the legality of the giving user
    :param user: the user to check
    :return: True when valid
    """
    for ch in user:
        temp_acsii = ord(ch)
        if 65 <= temp_acsii <= 90:
            temp_coverage = 1  # only for pytest coverage to see this condition
            continue
        elif 97 <= temp_acsii <= 122:
            temp_coverage = 1  # only for pytest coverage to see this condition
            continue
        elif 48 <= temp_acsii <= 57:
            temp_coverage = 1  # only for pytest coverage to see this condition
            continue
        else:
            return False
    return True


def valid_psw(psw):
    """
    | validate the legality of the giving password
    :param psw: the password to be validated
    :return: True when Valid
    """
    cap, low, num, sym = 0, 0, 0, 0
    for ch in psw:
        temp_acsii = ord(ch)
        if 65 <= temp_acsii <= 90:
            cap = 1
        elif 97 <= temp_acsii <= 122:
            low = 1
        elif 48 <= temp_acsii <= 57:
            num = 1
        elif 33 <= temp_acsii <= 46 or 58 <= temp_acsii <= 64 \
                or 91 <= temp_acsii <= 96 or 123 <= temp_acsii <= 126:
            sym = 1
        else:
            # when the ch is not one of the above its not valid char to use
            return False
        if cap == low == num == sym == 1:
            return True
    return False


def valid_email(email):
    """
    | validate the legality of the giving email
    :param email: the email to be validated
    :return: True when valid
    """
    regex = r'[^@]+@[^@]+\.[^@]+'
    if re.search(regex, email):
        return True
    return False


def valid_name_string(name):
    """
    | validate the legality of the giving name
    :param name: the name to be validated
    :return: True when valid
    """
    if len(name) > 30:
        return False
    char = set("~:[]{}()")
    if any((c in char) for c in name):
        return False
    return True
