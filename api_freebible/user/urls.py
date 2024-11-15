from .views import CustomUserViewSet
from rest_framework.routers import DefaultRouter

router_consumer = DefaultRouter()

# Registrando o CustomUserViewSet no roteador
router_consumer.register('custom_user', CustomUserViewSet)

urlpatterns = router_consumer.urls