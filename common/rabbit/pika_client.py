from typing import Awaitable, Callable
import logging
import json
from aio_pika import connect_robust, Message
import os
import sys

RABBIT_QUEUE = os.environ.get('RABBIT_QUEUE', 'queue')
RABBIT_HOST = os.environ.get('RABBIT_HOST', 'localhost')
RABBIT_PORT = os.environ.get('RABBIT_PORT', 5673)

logging.basicConfig()
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
log_handler = logging.StreamHandler(sys.stdout)
log_handler.setFormatter(log_formatter)
logger.addHandler(log_handler)
logger.setLevel(logging.DEBUG)


class PikaClient:
    def __init__(self):
        self.response = None

    async def start(self, loop):
        logger.info('Rabbit client started')
        self._connection = await connect_robust(host=RABBIT_HOST, port=RABBIT_PORT, loop=loop)
        self._channel = await self._connection.channel()
        self._queue = await self._channel.declare_queue(RABBIT_QUEUE)

    async def stop(self):
        await self._channel.close()
        await self._connection.close()


class Consumer(PikaClient):
    def __init__(self, process_callable: Awaitable[str]):
        super().__init__()
        self.process_callable = process_callable

    async def consume(self):
        '''Setup message listener with the current running loop'''
        await self._queue.consume(self.process_incoming_message, no_ack=False)
        logger.info('Established rabbit async listener')
        return self._connection

    async def process_incoming_message(self, message: str):
        '''Processing incoming message'''
        await message.ack()
        body = message.body
        logger.info(f'Received message: {message}')
        if body:
            await self.process_callable(json.loads(body))


class Producer(PikaClient):
    async def publish(self, message: dict):
        logger.info('Published message')
        '''Method to publish message'''
        await self._channel.default_exchange.publish(
            Message(body=json.dumps(message).encode()),
            routing_key=RABBIT_QUEUE
        )
