from rest_framework import serializers
from .models import FAQ
from django.conf import settings
from django.core.cache import cache

class FAQSerializer(serializers.ModelSerializer):
    translated_question = serializers.SerializerMethodField()
    translated_answer = serializers.SerializerMethodField()

    class Meta:
        model = FAQ
        fields = [
            'id', 
            'translated_question', 
            'translated_answer',
            'default_language'
        ]

    def _get_cached_translation(self, obj, field_type, lang):
        cache_key = f'faq:{obj.id}:{field_type}:{lang}'
        cached_value = cache.get(cache_key)
        
        if cached_value is None:
            if field_type == 'question':
                translation = obj.get_translated_question(lang)
            else:
                translation = obj.get_translated_answer(lang)
            cache.set(cache_key, translation, timeout=settings.FAQ_CACHE_TIMEOUT)
            return translation
        return cached_value

    def get_translated_question(self, obj):
        lang = self.context.get('lang', 'en')
        return self._get_cached_translation(obj, 'question', lang)

    def get_translated_answer(self, obj):
        lang = self.context.get('lang', 'en')
        return self._get_cached_translation(obj, 'answer', lang)