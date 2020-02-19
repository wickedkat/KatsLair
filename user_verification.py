import password_handler
from database import data_handler


def check_user_in_database(username):
    '''
Function calls database query, that returns user data by username given.
If there is no username in database, it returns False

:argument
username - dictionary

:returns
user_exists - dictionary
or
False
'''
    user_exists = data_handler.select_user_by_username(username)
    if user_exists:
       return user_exists
    else:
        return False




def verify_user(user):
    '''
    Function chcecks if username and password given in the login form are identical with
    credentials in database.

    :argument
    user - dict

    :returns
    True or False

    '''
    username = user['username']
    form_password = user['password']
    user_in_base = check_user_in_database(username)
    if user_in_base:
        password_in_base = user_in_base['password']
        verify =  password_handler.verify_password(form_password, password_in_base)
        if verify:
            return True
    return False




