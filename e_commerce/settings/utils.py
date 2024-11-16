def get_env():
    import os

    dir_name = os.path.dirname(__file__)
    path = os.path.join(dir_name, '.dj-env')
    if not os.path.exists(path):
        raise SystemExit(".dj-env is not present. Please create one.")

    fp = open(path)
    mode = fp.read().strip()
    fp.close()

    return mode


def get_logto_public_key(issuer):
    from django.core.cache import cache
    import requests

    jwks_url = f"{issuer}/jwks"
    cached_key = cache.get("logto_public_key")
    print('cached_key : ', cached_key)
    if cached_key:
        return cached_key

    response = requests.get(jwks_url)
    print('response : ', response)
    jwks = response.json()
    print('jwks : ', jwks)
    public_key = jwks['keys'][0]  # Use the first key; adjust if necessary
    print('public_key : ', public_key)

    # Cache the key to reduce network calls
    cache.set("logto_public_key", public_key, timeout=60 * 60 * 24)  # Cache for 1 day
    return public_key


