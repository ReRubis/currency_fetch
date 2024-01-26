from fastapi import APIRouter, FastAPI, HTTPException, Request, Depends, Header, Response, status
from fastapi.responses import RedirectResponse

from webcur.config import CONFIG

router = APIRouter(
    prefix='/exchange',
    tags=['Currency exchange values']
)

@router.get('/')
async def get_exchange_rates(
    request: 
):
    """
    Redirects to the exchange rate API
    """
    return RedirectResponse(url=CONFIG['exchange_api_url'])


@router.get('/')
async def get_exchange_rates_list(
    request: 
):
    """
    Redirects to the exchange rate API
    """
    return RedirectResponse(url=CONFIG['exchange_api_url'])