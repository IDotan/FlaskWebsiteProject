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
    """
    | generate reset code
    :return: reset code
    """
    chr_template = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    temp_code = ''
    while len(temp_code) < 6:
        temp_chr = randrange(0, len(chr_template))
        temp_code += chr_template[temp_chr]
    return temp_code


def send_reset_mail(code, send_to, user_id, timer):  # pragma: no cover
    """
    | send mail to the user with their link and reset code
    :param code: reset code to send
    :param send_to: email to send to
    :param user_id: user id
    :param timer: code timer
    """
    # for pytest to skip sending mail, to be able to run more test
    if send_to == 'i@i.com':
        return
    with open('email.ini', 'r') as file:
        mail_info = file.read().split(',')
    port = 465
    smtp_server = "smtp.gmail.com"
    message = f"""\
    Subject: Itai's Flask project password reset code

    Your reset code is {code}.
    To use this code go to {site_address}/passwordRest/{user_id}${str(timer)[::2]}
    Your rest code and link will be available for 30min."""
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(mail_info[0], mail_info[1])
        server.sendmail(mail_info[0], send_to, message)


def psw_reset_setup(user_add_code):
    """
    | set up the user reset password process
    :param user_add_code: user to set up its password reset
    """
    timer = int(time() + 1800)
    user_add_code.psw_reset_time = timer
    rest_code = generate_reset_code()
    user_add_code.psw_reset = rest_code
    users_db.session.commit()
    send_reset_mail(rest_code, user_add_code.email, user_add_code.id, timer)
