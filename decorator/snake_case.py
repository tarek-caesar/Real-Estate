def snake_case(func):
    def normalizer(*args):
        import re
        # install first using pip3 install unidecode
        from unidecode import unidecode
        txt = unidecode(func(*args)).replace(" ", "_").lower()
        return re.sub('[^a-zA-Z0-9 \n\.]', '_', txt)
    return normalizer


@snake_case
def get_file_name(user_name):
    return user_name


users = [
    "John Doe",
    "Max Müller",
    "Ariya O'Gallagher"
]
for user in users:
    print(get_file_name(user))
