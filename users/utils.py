import random
from django.core.cache import cache

def generate_and_store_code(user_id):
    code = str(random.randint(100000, 999999))
    TTL_SECONDS = 300 
    cache_key = f"confirmation_code_{user_id}"
    cache.set('test_key_superman', 'it_works_123', timeout=60)
    result = cache.get('test_key_superman')
    print(result)
    
