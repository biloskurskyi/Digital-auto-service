from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from .views import ManagerViewSet

router = DefaultRouter()
router.register('managers', ManagerViewSet, basename='manager')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
