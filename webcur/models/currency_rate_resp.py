from pydantic import BaseModel


class CurrencyRateResponce(BaseModel):
    """
    A response model for the exchange rate API
    """
    instId: str
    instType: str
    markPx: str
    ts: str


class CurrencyRateListResponce(BaseModel):
    """
    A response model for when all rates are requested

    Returns a list of CurrencyRaterResponce
    """
    data: dict[str, CurrencyRateResponce]
