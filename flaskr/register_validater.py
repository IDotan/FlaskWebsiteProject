
def check_form_data(user_id, psw):
    """
    | used to check for valid register info validity
    :param user_id: the user to check
    :param psw: the password to be validated
    :return: True when valid
    """
    if len(user_id) < 5:
        return False
    if not valid_user(user_id):
        return False
    if not valid_psw(psw):
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
            continue
        elif 97 <= temp_acsii <= 122:
            continue
        elif 48 <= temp_acsii <= 57:
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

