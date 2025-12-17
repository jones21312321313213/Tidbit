from django.db import connection

def insert_user_user(auth_user_id):
    with connection.cursor() as cursor:
        cursor.callproc("insert_user_user", [auth_user_id])
