from pydantic import BaseModel, validator
from enum import Enum


class Status(str, Enum):
    completed = "completed"
    pending = "pending"
    canceled = "canceled"


class Order(BaseModel):
    id: int
    item: str
    quantity: int
    price: float
    status: Status

    @validator('price')
    def price_must_be_positive(cls, v):
        if v < 0:
            raise ValueError('Price cannot be a negative number')
        return v
