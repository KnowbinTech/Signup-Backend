from django.test import TestCase

# Create your tests here.

def hash_with_sha256(data, data_encode=True):
    import hashlib
    """
        Function to hash the string into SHA-256 format
    """
    sha256 = hashlib.sha256()
    if data_encode:
        sha256.update(data.encode('utf-8'))
        hashed_data = sha256.hexdigest()
    else:
        sha256.update(data)
        hashed_data = sha256.hexdigest()
    return hashed_data

def generate_headers(input_string):
    CHECK_SUM_FORMAT = '{}###{}'
    sha256_value = hash_with_sha256(input_string)
    check_sum = CHECK_SUM_FORMAT.format(sha256_value, 1)

    headers = {
        'Content-Type': 'application/json',
        'X-VERIFY': check_sum,
        'accept': 'application/json',
    }

    return headers


if __name__ == '__main__':

    string = f'/pg/v1/status/M22Q3JLT6IUGJ/SC-TXN00003735456a48-fc84-4a0f-ad63-d53de7f4659b'

    sha = generate_headers(string)

    print('sha : ', sha)

