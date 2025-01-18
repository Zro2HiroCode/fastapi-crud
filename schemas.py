from typing import Optional
from pydantic import BaseModel

class MsgPayload(BaseModel):
    msg_id: Optional[int]
    msg_name: str

class RecipeCostBase(BaseModel):
    list: str
    weight: Optional[int]
    unit_pkg: str
    price: Optional[float]
    quantity: str
    cost: Optional[float]

class RecipeCostCreate(RecipeCostBase):
    pass

class RecipeCost(RecipeCostBase):
    id: int

    class Config:
        orm_mode = True