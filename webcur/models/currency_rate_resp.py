from pydantic import BaseModel


class CurrencyRaterResponce(BaseModel):
    currency: str
    rate: float
    date: str

    class Config:
        orm_mode = True
