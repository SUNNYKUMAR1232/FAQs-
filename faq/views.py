from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
import logging
from django.conf import settings
from .models import FAQ
from .serializers import FAQSerializer
from .utils import redis_manager

logger = logging.getLogger(__name__)

CACHE_TIMEOUT = getattr(settings, 'FAQ_CACHE_TIMEOUT', 3600)  # 1 hour default
SUPPORTED_LANGUAGES = getattr(settings, 'SUPPORTED_LANGUAGES', ['en', 'hi', 'bn'])

class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    def _get_cache_status(self):
        """Monitor cache health"""
        try:
            return redis_manager.ping()
        except Exception as e:
            logger.error(f"Redis health check failed: {str(e)}")
            return False

    def list(self, request):
        """Cached FAQ list retrieval"""
        lang = request.query_params.get('lang', 'en')
        if lang not in SUPPORTED_LANGUAGES:
            return Response(
                {'error': f'Invalid language. Supported: {SUPPORTED_LANGUAGES}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        cache_key = f'faq_list_{lang}'
        cache_hit = False

        try:
            cache_faqs = redis_manager.get_cache_faq(cache_key)
            if cache_faqs:
                cache_hit = True
                return Response({
                    'data': cache_faqs,
                    'cache_hit': cache_hit
                })
        except Exception as e:
            logger.error(f"Redis cache error: {str(e)}")

        queryset = self.get_queryset()
        serializer = self.get_serializer(
            queryset, many=True, context={'lang': lang}
        )

        try:
            redis_manager.cache_faq(
                cache_key, 
                serializer.data,
                timeout=CACHE_TIMEOUT
            )
        except Exception as e:
            logger.error(f"Redis cache error: {str(e)}")

        return Response({
            'data': serializer.data,
            'cache_hit': cache_hit
        })

    @action(detail=False, methods=['GET'])
    def search(self, request):
        """Cached search endpoint"""
        query = request.query_params.get('q', '')
        lang = request.query_params.get('lang', 'en')
        
        if not query:
            return Response(
                {'error': 'Search query required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        cache_key = f'faq_search_{lang}_{query}'
        cache_hit = False

        try:
            cached_results = redis_manager.get_cache_faq(cache_key)
            if cached_results:
                cache_hit = True
                return Response({
                    'data': cached_results,
                    'cache_hit': cache_hit
                })
        except Exception as e:
            logger.error(f"Redis search cache error: {str(e)}")

        queryset = FAQ.objects.filter(question__icontains=query)
        serializer = self.get_serializer(
            queryset,
            many=True,
            context={'lang': lang}
        )

        try:
            redis_manager.cache_faq(
                cache_key, 
                serializer.data,
                timeout=300  # Short timeout for search results
            )
        except Exception as e:
            logger.error(f"Redis search cache error: {str(e)}")

        return Response({
            'data': serializer.data,
            'cache_hit': cache_hit
        })

    @action(detail=False, methods=['POST'])
    def bulk_create(self, request):
        """Bulk create FAQs with cache management"""
        serializer = self.get_serializer(
            data=request.data, 
            many=True
        )
        serializer.is_valid(raise_exception=True)
        faqs = serializer.save()

        try:
            # Invalidate all list caches after bulk create
            redis_manager.invalidate_faq_cache('faq_list_*')
            # Cache individual FAQs
            for faq in faqs:
                redis_manager.cache_faq(
                    f'faq:{faq.id}', 
                    self.get_serializer(faq).data,
                    timeout=CACHE_TIMEOUT
                )
        except Exception as e:
            logger.error(f"Redis bulk create cache error: {str(e)}")

        return Response(
            serializer.data, 
            status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=['POST'])
    def warm_cache(self, request):
        """Warm up the cache for all FAQs"""
        try:
            queryset = self.get_queryset()
            for lang in SUPPORTED_LANGUAGES:
                serializer = self.get_serializer(
                    queryset,
                    many=True,
                    context={'lang': lang}
                )
                redis_manager.cache_faq(
                    f'faq_list_{lang}',
                    serializer.data,
                    timeout=CACHE_TIMEOUT
                )
            return Response({'status': 'Cache warmed successfully'})
        except Exception as e:
            logger.error(f"Cache warmup failed: {str(e)}")
            return Response(
                {'error': 'Cache warmup failed'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )