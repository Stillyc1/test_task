from celery import shared_task
from .models import PayoutRequest
import logging
import random
import time

logger = logging.getLogger(__name__)

@shared_task
def process_payout_request(payout_id):
    """
    Асинхронная задача: обработка заявки на выплату.
    """
    try:
        payout = PayoutRequest.objects.get(id=payout_id)
        logger.info(f"Начата обработка заявки #{payout_id}: {payout.amount} {payout.currency}")

        time.sleep(3)

        # Имитируем успешность выполнения заявки (90% одобрена, 10% отклонена)
        if random.random() < 0.9:
            payout.status = 'approved'
            logger.info(f"Заявка #{payout_id} одобрена.")
        else:
            payout.status = 'rejected'
            logger.info(f"Заявка #{payout_id} отклонена.")

        payout.save()
        logger.info(f"Заявка #{payout_id} обновлена: статус = {payout.status}")

    except PayoutRequest.DoesNotExist:
        logger.error(f"Заявка с id={payout_id} не найдена.")
        raise
    except Exception as e:
        logger.error(f"Ошибка при обработке заявки #{payout_id}: {str(e)}")
        raise
