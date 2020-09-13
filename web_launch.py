from flaskr import create_app, users_db, toDoList_db
from datetime import timedelta
import os

__author__ = "Itai Dotan"


def check_setting_ini_exist():
    """
    | check if there is a setting.ini file
    | create the file when not found
    """
    if not os.path.exists('setting.ini'):
        with open('setting.ini', 'w') as file:
            file.write('login-timer =\n')
            file.write('public =\n')
            file.write('debug =\n')
            file.write('# gmail account to use for password reset\n')
            file.write('email =\n')
            file.write('email-password =\n')


def clean_setting_line(line):
    """
    | clean the given line from spaces
    :param line: line to clean
    :return: line with out spaces
    """
    temp_line = line.replace(' ', '')
    return temp_line


def clean_setting_line_input(line):
    """
    | clean the given line input to include only the needed parm
    :param line: line to clean
    :return: cleaned parm
    """
    temp_mark = line.index('=')
    temp_setting = line[temp_mark + 1:].replace('\n', '').strip()
    return temp_setting


def get_login_time(setting, default):
    """
    | get the login timer setting
    | when there is no valid value return the given default
    :param setting: new value to use for the timer
    :param default: default value to use when not a valid value given
    :return: value to use as login timer
    """
    try:
        return timedelta(hours=int(setting))
    except ValueError:
        return default
    except OverflowError:
        return default


def get_host_setting(setting):
    """
    | get the host type to use
    | true = publicly open
    | false = only reachable locally
    :param setting: given setting to check against
    :return: '0.0.0.0' for public access
    """
    if setting == 'true' or setting == 'True':
        return '0.0.0.0'
    elif setting == 'false' or setting == 'False':
        return ''


def get_debug_setting(setting):
    """
    | get the debug setting to use
    :param setting: setting to check against
    :return: true when using debug mod
    """
    if setting == 'true' or setting == 'True':
        return True
    elif setting == 'false' or setting == 'False':
        return False


def delete_email_ini_file():
    if os.path.exists('email.ini'):
        os.remove('email.ini')


def get_settings():
    """
    | get the setting to use for the flask launch
    :return:
    """
    session_life_time_setting = timedelta(hours=1)
    host_setting = ''
    debug_setting = False
    delete_email_ini = True
    with open('setting.ini', 'r') as file:
        with open('email.ini', 'w') as mail_file:
            lines = file.readlines()
            for line in lines:
                line = clean_setting_line(line)
                if 'login-timer=' in line:
                    time_int = clean_setting_line_input(line)
                    session_life_time_setting = get_login_time(time_int, session_life_time_setting)
                elif 'public=' in line:
                    temp_host = clean_setting_line_input(line)
                    host_setting = get_host_setting(temp_host)
                elif 'debug=' in line:
                    temp_debug = clean_setting_line_input(line)
                    debug_setting = get_debug_setting(temp_debug)
                elif 'email=' in line:
                    temp_mail = clean_setting_line_input(line)
                    if temp_mail:
                        mail_file.write(f'{temp_mail},')
                        delete_email_ini = False
                elif 'email-password=' in line:
                    temp_mail_psw = clean_setting_line_input(line)
                    if temp_mail_psw:
                        mail_file.write(f'{temp_mail_psw}')
                    else:
                        delete_email_ini = True
    if delete_email_ini:
        delete_email_ini_file()
    return session_life_time_setting, host_setting, debug_setting


if __name__ == "__main__":
    users_db.create_all(app=create_app())
    toDoList_db.create_all(app=create_app())
    app = create_app()
    check_setting_ini_exist()
    session_life_time, host, debug = get_settings()
    app.permanent_session_lifetime = session_life_time
    app.run(debug=debug, host=host)
