"""
| create reset code for the user and send it via mail to the registered email
"""
import smtplib
import ssl
from .. import users_db
from random import randrange
from time import time

__author__ = "Itai Dotan"

"""site address to send with the reset code email"""
site_address = "http://127.0.0.1:5000/"


def generate_reset_code():
    chr_template = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    temp_code = ''
    while len(temp_code) < 6:
        temp_chr = randrange(0, len(chr_template))
        temp_code += chr_template[temp_chr]
    return temp_code


def send_reset_mail(code, send_to, user_id):
    with open('email.ini', 'r') as file:
        mail_info = file.read().split(',')
    port = 465
    smtp_server = "smtp.gmail.com"
    message = f"""\
    Subject: Itai's Flask project password reset code

    Your reset code is {code}.
    To use this code go to {site_address}/link#{user_id}"""
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(mail_info[0], mail_info[1])
        server.sendmail(mail_info[0], send_to, message)


def psw_reset_setup(user_add_code):
    user_add_code.psw_reset_time = int(time() + 1800)
    rest_code = generate_reset_code()
    user_add_code.psw_reset = rest_code
    users_db.session.commit()
    send_reset_mail(rest_code, user_add_code.email, user_add_code.id)
