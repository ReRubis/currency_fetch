from fastapi import APIRouter, FastAPI, HTTPException, Request, Depends, Header, Response, status
from fastapi.responses import RedirectResponse
from typing import Literal

from webcur.models.currency_rate_resp import CurrencyRaterResponce

from webcur.config import CONFIG

router = APIRouter(
    prefix='/exchange',
    tags=['Currency exchange values']
)


@router.get(
    '/',
    response_model=CurrencyRaterResponce
)
async def get_exchange_rates(
    pair_name: Literal['BTC-USDT', 'ETH-USDT', 'XRP-USDT'],
    # exchange_api_service:
):
    """
    Returns the stored exchange rate for the given pair

    Args:
        pair_name (Literal['BTC-USDT', 'ETH-USDT', 'XRP-USDT']): 
        The pair to get the exchange rate for
    """
    return RedirectResponse(url=CONFIG['exchange_api_url'])


# @router.get('/')
# async def get_exchange_rates_list(
#     request:
# ):
#     """
#     Redirects to the exchange rate API
#     """
#     return RedirectResponse(url=CONFIG['exchange_api_url'])
