from pydantic import BaseModel, PrivateAttr
import uuid


class Appeal(BaseModel):
    id: uuid.UUID
    surname: str
    name: str
    middle_name: str
    text: str
    phone: str
    email: str


class AppealIn(BaseModel):
    _id: uuid.UUID = PrivateAttr(default_factory=uuid.uuid4)
    surname: str
    name: str
    middle_name: str
    text: str
    phone: str
    email: str
