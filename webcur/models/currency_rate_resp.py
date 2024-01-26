from pydantic import BaseModel


class CurrencyRaterResp(BaseModel):
    currency: str
    rate: float
    date: str

    class Config:
        orm_mode = True