# core/caching.py
from datetime import timedelta
from functools import wraps
import redis  # or use django-cache for simpler setup

cache = redis.Redis(host='localhost', port=6379, db=0)

def cache_result(ttl: timedelta = timedelta(hours=1)):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            result = cache.get(cache_key)
            if result:
                return pickle.loads(result)
            result = func(*args, **kwargs)
            cache.setex(cache_key, ttl, pickle.dumps(result))
            return result
        return wrapper
    return decorator

# Usage in repositories:
@cache_result(timedelta(hours=2))
def search(self, query: str) -> List[ContentItem]:
    ...