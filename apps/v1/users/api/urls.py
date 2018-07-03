from . import views

app_name = 'users'

# api

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'', views.UserViewSet)

urlpatterns = router.urls
