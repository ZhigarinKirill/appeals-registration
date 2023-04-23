import asyncio
import sys
from common.rabbit.pika_client import Producer
import tornado.web
import logging
import os

logging.basicConfig()
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
log_handler = logging.StreamHandler(sys.stdout)
log_handler.setFormatter(log_formatter)
logger.addHandler(log_handler)
logger.setLevel(logging.DEBUG)
TORNADO_HOST=os.environ.get('TORNADO_HOST', 'localhost')
TORNADO_PORT=os.environ.get('TORNADO_PORT', 8888)


class MainHandler(tornado.web.RequestHandler):
    async def post(self):
        message = tornado.escape.json_decode(self.request.body)
        logger.info('Post request with body: {message}')
        await self.application.producer.publish(message)
        self.write("OK")


def make_app():
    return tornado.web.Application([
        (r"/register-appeal", MainHandler),
    ])


async def main():
    app = make_app()
    app.producer = Producer()
    loop = asyncio.get_running_loop()
    await app.producer.start(loop)
    logger.info('Producer was started')
    app.listen(TORNADO_PORT)
    logger.info(f'Tornado API was started. Listening port {TORNADO_PORT}')
    
    shutdown_event = asyncio.Event()
    await shutdown_event.wait()
    logger.info('Tornado API was shutdown')
