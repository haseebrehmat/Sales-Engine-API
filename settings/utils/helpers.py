import re
import uuid


def get_host(request):
    host = request.get_host()
    if 'http' not in host:
        host = 'http://' + host
    return host


def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False


def validate_password(password):
    password_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
    return re.match(password_pattern, password)


def serializer_errors(serializer):
    try:
        fields = list(serializer.errors.keys())
        data = [x + ": " + serializer.errors[x][0] for x in fields]
        data = "\n".join(data)
        return data
    except:
        return serializer.errors


import random
import string

# Function to generate a random email
def generate_random_email():
    # Define the characters to choose from
    alpha_characters = string.ascii_letters  # This includes all alphabets (uppercase and lowercase)
    numeric_characters = string.digits  # This includes 0-9

    # Generate 5 random alphabet characters
    alpha_part = ''.join(random.choice(alpha_characters) for _ in range(5))

    # Generate 10 random numeric characters
    numeric_part = ''.join(random.choice(numeric_characters) for _ in range(10))

    # Combine the alpha and numeric parts with the email domain
    email = alpha_part + numeric_part + "@example.com"

    return email
