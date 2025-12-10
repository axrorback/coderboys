from datetime import datetime

def get_prefix():
    year = datetime.now().year
    last_two = str(year)[-2:]
    return f"CB{last_two}"

def build_username(prefix, department_code, number):
    return f"{prefix}{department_code}{str(number).zfill(3)}"

def generate_email(username):
    return f"{username.lower()}@coderboys.uz"

