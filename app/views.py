from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from app.models import PayoutRequest
from app.serializers import (PayoutRequestSerializer,
                             PayoutRequestUpdateSerializer)
from app.tasks import process_payout_request


class PayoutRequestViewSet(ModelViewSet):
    """Реализация представления заявки на выплату через ViewSet (полный crud)"""

    queryset = PayoutRequest.objects.all()
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.action == "partial_update":
            return PayoutRequestUpdateSerializer
        return PayoutRequestSerializer

    def perform_create(self, serializer):
        payout = serializer.save()

        # Запускаем асинхронную задачу
        process_payout_request.delay(payout.id)
