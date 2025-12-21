import hashlib


def create_short_hash(*args, length=8):
    data_string = "".join(map(str, args))
    return hashlib.shake_128(data_string.encode()).hexdigest(length // 2)