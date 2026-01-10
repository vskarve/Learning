import random
import string
def random_string(n):
    chars = string.ascii_letters + string.digits + " "
    return ''.join(random.choices(chars, k=n))