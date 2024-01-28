from fastapi import APIRouter, Depends
from typing import Literal

from webcur.models.currency_rate_resp import (
    CurrencyRateResponce,
    CurrencyRateListResponce
)
from webcur.service.exhachanger import ExchangeRatesService
from webcur.service.injectors import main_service_injector


router = APIRouter(
    prefix='/exchange',
    tags=['Currency exchange values']
)


@router.get(
    '/',
    response_model=CurrencyRateResponce
)
async def get_exchange_rates(
    pair_name: Literal['BTC-USDT', 'ETH-USDT', 'XRP-USDT'],
    service: ExchangeRatesService = Depends(main_service_injector),
):
    """
    Returns the stored exchange rate for the given pair

    Args:
        pair_name (Literal['BTC-USDT', 'ETH-USDT', 'XRP-USDT']):
        The pair to get the exchange rate for
    """
    return await service.return_rate(pair_name)


@router.get(
    '/courses',
    response_model=CurrencyRateListResponce
)
async def get_exchange_rates_list(
    service: ExchangeRatesService = Depends(main_service_injector),
):
    """
    Redirects to the exchange rate API.
    """
    return await service.return_rates_list()
