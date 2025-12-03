from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

# Список поддерживаемых валют
CURRENCY_CHOICES = [
    ("RUB", "Российский рубль"),
    ("USD", "Доллар США"),
    ("EUR", "Евро"),
    ("KZT", "Казахский тенге"),
]

# Статусы заявки
STATUS_CHOICES = [
    ("pending", "В обработке"),
    ("approved", "Одобрена"),
    ("rejected", "Отклонена"),
    ("paid", "Выплачена"),
    ("cancelled", "Отменена"),
]


class PayoutRequest(models.Model):
    """
    Модель заявки на выплату.
    Представляет запрос пользователя на вывод средств.
    """

    amount = models.DecimalField(
        verbose_name="Сумма выплаты",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
        help_text="Минимальная сумма — 0.01",
    )
    currency = models.CharField(
        verbose_name="Валюта", max_length=3, choices=CURRENCY_CHOICES, default="RUB"
    )
    recipient_details = models.TextField(
        verbose_name="Реквизиты получателя",
        help_text="Например, номер счёта, карта, электронный кошелёк",
    )
    status = models.CharField(
        verbose_name="Статус заявки",
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Дата обновления", auto_now=True)
    comment = models.TextField(
        verbose_name="Комментарий",
        blank=True,
        null=True,
        help_text="Дополнительная информация (необязательно)",
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Владелец заявки",
    )

    def __str__(self):
        return f"Выплата {self.amount} {self.currency} — {self.status}"

    class Meta:
        verbose_name = "Заявка на выплату"
        verbose_name_plural = "Заявки на выплату"
        ordering = ["-created_at"]
        db_table = "payout_requests"
