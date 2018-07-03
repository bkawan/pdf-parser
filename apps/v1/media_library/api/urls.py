from . import views

app_name = 'media_library'

# api

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'images', views.ImageViewSet)

urlpatterns = router.urls
