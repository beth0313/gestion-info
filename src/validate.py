import re

def validate_id(user_id, ids_set):
    if not user_id:
        raise ValueError("ID requerido")

    if user_id in ids_set:
        raise ValueError("ID duplicado")


def validate_name(name):
    if not name or len(name.strip()) < 2:
        raise ValueError("Nombre inválido")


def validate_email(email, emails_set):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    if not re.match(pattern, email):
        raise ValueError("Email inválido")

    if email in emails_set:
        raise ValueError("Email duplicado")