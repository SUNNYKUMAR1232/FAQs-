import redis
from django.core.cache import cache
from django.conf import settings

class RedisManager:
    def __init__(self):
        self.redis_client = redis.Redis.from_url(
            settings.CACHES['default']['LOCATION']
        )

    def cache_faq(self, faq_id, data, timeout=3600):
        """Cache FAQ data with specific key"""
        cache_key = f'faq:{faq_id}'
        self.redis_client.setex(cache_key, timeout, data)

    def get_cached_faq(self, faq_id):
        """Retrieve cached FAQ data"""
        cache_key = f'faq:{faq_id}'
        return self.redis_client.get(cache_key)

    def invalidate_faq_cache(self, faq_id):
        """Remove specific FAQ from cache"""
        cache_key = f'faq:{faq_id}'
        self.redis_client.delete(cache_key)

    def cache_translation(self, question, lang, translation):
        """Cache translations separately"""
        cache_key = f'translation:{question}:{lang}'
        self.redis_client.setex(cache_key, 86400, translation)  # 24-hour cache

    def get_cached_translation(self, question, lang):
        """Retrieve cached translation"""
        cache_key = f'translation:{question}:{lang}'
        return self.redis_client.get(cache_key)

redis_manager = RedisManager()