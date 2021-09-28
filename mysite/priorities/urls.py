from rest_framework import routers

from priorities.views import PrioritiesViewSet, PrioritiesNameViewSet

router = routers.SimpleRouter()
router.register(r'priorities', PrioritiesViewSet)
router.register(r'priorities_name', PrioritiesNameViewSet)
urlpatterns = router.urls
