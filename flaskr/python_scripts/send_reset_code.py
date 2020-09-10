from web_launch import email_to_send_code_from, email_to_send_code_from_psw
from .. import users_db
from random import randrange
from time import time


def generate_reset_code():
    chr_template = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    temp_code = ''
    while len(temp_code) < 7:
        temp_chr = randrange(0, len(chr_template))
        temp_code += chr_template[temp_chr]
    return temp_code


def psw_reset_setup(user_add_code):
    code_time_out = int(time() + 1800)
    user_add_code.psw_reset_time = code_time_out
    rest_code = generate_reset_code()
    user_add_code.psw_reset = rest_code
    users_db.session.commit()
