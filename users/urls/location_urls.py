from rest_framework import routers

from users.views.location_views import LocationViewSet

router = routers.SimpleRouter()
router.register('location', LocationViewSet)

urlpatterns = [
    # тут все остальные маршруты
]

urlpatterns += router.urls
