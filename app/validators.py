from decimal import Decimal
from rest_framework import serializers

from app.models import CURRENCY_CHOICES


def validate_positive_amount(value):
    """
    Проверяет, что сумма выплаты положительная.
    """
    if value <= Decimal('0'):
        raise serializers.ValidationError("Сумма должна быть больше 0")
    return value


def validate_recipient_details(value):
    """
    Проверяет, что реквизиты получателя не пустые и содержат минимум 5 символов.
    """
    if not value or len(value.strip()) < 5:
        raise serializers.ValidationError("Реквизиты должны содержать не менее 5 символов.")
    return value


def validate_currency(value):
    """
    Проверяет, что валюта входит в список допустимых.
    """
    valid_currencies = [code for code, _ in CURRENCY_CHOICES]
    if value not in valid_currencies:
        raise serializers.ValidationError(f"Допустимые валюты: {', '.join(valid_currencies)}")
    return value
