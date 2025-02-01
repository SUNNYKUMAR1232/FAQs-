from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import FAQViewSet

router = DefaultRouter()
router.register(r'faqs', FAQViewSet, basename='faq')

urlpatterns = [
    path('api/', include(router.urls)),
]