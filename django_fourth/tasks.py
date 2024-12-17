import logging

from celery import shared_task
from kombu import Exchange, Queue, Connection, Consumer
from kombu.exceptions import OperationalError

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Объявляем exchange
book_exchange = Exchange('book-create-exchange', type='topic')


@shared_task
def consume_messages():
    logger.info("Consumer task started.")

    # Очереди с привязкой к exchange
    queue1 = Queue('book-topic-q-History', exchange=book_exchange, routing_key='book.History')
    queue2 = Queue('book-topic-q-Classic', exchange=book_exchange, routing_key='book.Classic')
    queue3 = Queue('book-topic-q-common', exchange=book_exchange, routing_key='book.#')

    with Connection('amqp://guest:guest@rabbitmq:5672//') as conn:
        with conn.channel() as channel:
            try:
                # Указываем каналу, что мы хотим использовать указанные очереди
                queue1.declare(channel=channel)
                queue2.declare(channel=channel)
                queue3.declare(channel=channel)

                # Создаем consumer
                with Consumer(channel, queues=[queue1, queue2, queue3], callbacks=[callback], accept=['json']):
                    logger.info("Consumer registered, waiting for messages...")
                    while True:
                        conn.drain_events()
            except OperationalError as e:
                logger.error(f"Error in RabbitMQ connection: {e}")
            except Exception as e:
                logger.error(f"Unexpected error: {e}")


def callback(body, message):
    logger.info(f"Received message: {body}")
    message.ack()

consume_messages.delay()