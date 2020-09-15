from .. import users_db
from random import randrange
from time import time

__author__ = "Itai Dotan"


def generate_reset_code():
    chr_template = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    temp_code = ''
    while len(temp_code) < 7:
        temp_chr = randrange(0, len(chr_template))
        temp_code += chr_template[temp_chr]
    return temp_code


def send_reset_mail(code, send_to):
    with open('email.ini', 'r') as file:
        mail_info = file.read().split(',')


def psw_reset_setup(user_add_code):
    user_add_code.psw_reset_time = int(time() + 1800)
    rest_code = generate_reset_code()
    user_add_code.psw_reset = rest_code
    users_db.session.commit()
    send_reset_mail(rest_code, user_add_code.email)
