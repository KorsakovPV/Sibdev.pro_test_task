from rest_framework import routers

from accounts.views import AccountViewSet

router = routers.SimpleRouter()
router.register(r'accounts', AccountViewSet)
urlpatterns = router.urls