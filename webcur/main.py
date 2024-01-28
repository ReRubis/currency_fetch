from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from webcur.routes import route
from webcur.service.exhachanger import ExchangeRatesService
from webcur.service.external_api.BinanceIntegration import BinanceIntegration
from webcur.service.external_api.OKXintegration import OKXIntegration
from webcur.database.repository import DataBaseRepository
import uvicorn
from webcur.config import CONFIG
import threading
import asyncio


def background_process():
    """
    Background process that fetches the data from API and saves it database
    """
    # repository = DataBaseRepository

    async def run():
        api = [
            # BinanceIntegration(),
            OKXIntegration()
        ]
        print("Starting background process")
        for api in api:
            await api.run_websocket(
                pair_name=CONFIG['CURRENCY_PAIRS']
            )

    asyncio.run(run())


def app_factory():
    app = FastAPI()

    origins = [
        "*",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(route.router)

    return app


app = app_factory()


if __name__ == '__main__':
    threading.Thread(target=background_process).start()
    uvicorn.run(app, host="0.0.0.0", port=8000)
