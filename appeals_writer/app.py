from typing import Dict, List
from fastapi import FastAPI
from common.rabbit.pika_client import Consumer
# from router import router
import asyncio
import logging
from common.database import appeals_table, appeals_database, engine, metadata
from models.appeals import AppealIn
import sys

logging.basicConfig()
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
log_handler = logging.StreamHandler(sys.stdout)
log_handler.setFormatter(log_formatter)
logger.addHandler(log_handler)
logger.setLevel(logging.DEBUG)


class AppealApp(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.consumer = Consumer(self.save_appeal)

    @classmethod
    async def save_appeal(cls, message: Dict):
        logger.info(f'Incoming message {message}')
        appeal = AppealIn(**message)
        query = appeals_table.insert().values(id=appeal._id, **appeal.dict())
        await appeals_database.execute(query)


app = AppealApp()


@app.on_event('startup')
async def startup():
    loop = asyncio.get_running_loop()
    await app.consumer.start(loop)
    task = loop.create_task(app.consumer.consume())
    await task
    metadata.create_all(engine)
    await appeals_database.connect()
    logger.info('FastAPI writer was started')


@app.on_event("shutdown")
async def shutdown():
    await appeals_database.disconnect()
    await app.consumer.stop()
    logger.info('FastAPI writer was shutdown')
