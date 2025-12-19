from django.db import connection

def create_basic_card_proc(user_id, deck_id, front, back):
    with connection.cursor() as cursor:
        cursor.callproc("create_basic_card", [user_id, deck_id, front, back])

def create_identification_card_proc(user_id, deck_id, front, hidden):
    with connection.cursor() as cursor:
        cursor.callproc("create_identification_card", [user_id, deck_id, front, hidden])

def create_image_card_proc(user_id, deck_id, front, img_path):
    with connection.cursor() as cursor:
        cursor.callproc("create_image_card", [user_id, deck_id, front, img_path])

def update_basic_card_proc(card_id, user_id, front, back):
    with connection.cursor() as cursor:
        cursor.callproc("update_basic_card", [card_id, user_id, front, back])

def update_identification_card_proc(card_id, user_id, front, hidden):
    with connection.cursor() as cursor:
        cursor.callproc("update_identification_card", [card_id, user_id, front, hidden])

def update_image_card_proc(card_id, user_id, front, img_path):
    with connection.cursor() as cursor:
        cursor.callproc("update_image_card", [card_id, user_id, front, img_path])

def delete_card_proc(card_id, username):
    with connection.cursor() as cursor:
        cursor.callproc("delete_card_procedure", [card_id, username])