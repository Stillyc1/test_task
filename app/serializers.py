from rest_framework import serializers

from .models import CURRENCY_CHOICES, PayoutRequest
from .validators import (validate_currency, validate_positive_amount,
                         validate_recipient_details)


class PayoutRequestSerializer(serializers.ModelSerializer):
    """
    Сериализатор представления заявки на выплату.
    """

    amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, validators=[validate_positive_amount]
    )
    currency = serializers.ChoiceField(
        choices=CURRENCY_CHOICES, validators=[validate_currency]
    )
    recipient_details = serializers.CharField(
        max_length=500, validators=[validate_recipient_details]
    )

    class Meta:
        model = PayoutRequest
        exclude = ("owner",)
        read_only_fields = ["id", "created_at", "updated_at"]


class PayoutRequestUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор обновления статуса заявки на выплату.
    """

    class Meta:
        model = PayoutRequest
        fields = [
            "id",
            "status",
            "comment",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
