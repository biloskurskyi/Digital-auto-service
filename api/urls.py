from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AuthTokenView, ManagerViewSet

router = DefaultRouter()
router.register('managers', ManagerViewSet, basename='manager')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-token-auth/', AuthTokenView.as_view(), name='api_token_auth'),
]
