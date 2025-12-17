from django.db import connection
from django.contrib.auth.hashers import check_password

def insert_user_user(auth_user_id):
    with connection.cursor() as cursor:
        cursor.callproc("insert_user_user", [auth_user_id])



def loginUser(username, password):
    # This will get the username using the stored procedure
    # then if user exists then it will return the hashed password
    # then usings Django check_password it will compare the password from the input and with the hash
    with connection.cursor() as cursor:
        cursor.callproc("LoginUser", [username])
        result = cursor.fetchone()

    if not result:
        return False

    hashed_password = result[0]
    return check_password(password, hashed_password)

def update_user_email(username, new_email):
    with connection.cursor() as cursor:
        cursor.callproc("update_userEmail", [username, new_email])
    connection.commit()


def verify_user_password(username, plain_password):
    #will just use the LoginUser to authenticate since that stored procedure will return a hash password
    with connection.cursor() as cursor:
        cursor.callproc('LoginUser', [username])
        result = cursor.fetchone()
        if not result:
            return False  # user not found
        db_password = result[0]

    return check_password(plain_password, db_password)

