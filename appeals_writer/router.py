from typing import List
from fastapi import APIRouter
from common.rabbit.pika_client import logger
from models.appeals import Appeal, AppealIn
from common.database import appeals_table, appeals_database

router = APIRouter(
    tags=['appeals'],
    responses={404: {"description": "Page not found"}}
)


@router.get("/list", response_model=List[Appeal])
async def read_notes():
    query = appeals_table.select()
    return await appeals_database.fetch_all(query)


@router.post("/save", response_model=Appeal)
async def create_note(appeal: AppealIn):
    print(appeal.dict(), appeal._id)
    query = appeals_table.insert().values(id=appeal._id, **appeal.dict())
    last_record_id = await appeals_database.execute(query)
    return {**appeal.dict(), "id": last_record_id}
