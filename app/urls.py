from rest_framework.routers import DefaultRouter

from app.apps import AppConfig
from app.views import PayoutRequestViewSet

app_name = AppConfig.name

router = DefaultRouter()
router.register(prefix=r"payouts", viewset=PayoutRequestViewSet, basename="payouts")

urlpatterns = [] + router.urls
