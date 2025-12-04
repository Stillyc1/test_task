from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from app.models import PayoutRequest


class PayoutRequestViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("app:payouts-list")
        self.valid_payload = {
            "amount": "1000.50",
            "currency": "RUB",
            "recipient_details": "Счёт: 1234567890",
            "status": "pending",
            "comment": "Выплата",
        }

    @patch("app.views.process_payout_request.delay")
    def test_create_payout_request_success(self, mock_delay):
        """Тест: успешное создание заявки"""
        response = self.client.post(self.url, self.valid_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PayoutRequest.objects.count(), 1)

        self.assertTrue(mock_delay.called)
        mock_delay.assert_called_once()

        payout = PayoutRequest.objects.first()
        self.assertEqual(payout.amount, 1000.50)
        self.assertEqual(payout.currency, "RUB")
        self.assertEqual(payout.status, "pending")
        self.assertEqual(payout.recipient_details, "Счёт: 1234567890")
