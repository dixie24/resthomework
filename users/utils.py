import random
from django.core.cache import cache

def generate_and_store_code(user_id):
    code = str(random.randint(100000, 999999))
    TTL_SECONDS = 300 
    cache_key = f"confirmation_code_{user_id}"
    cache.set(cache_key, code, timeout=TTL_SECONDS)
    return code  

