from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from webcur.routes import route
from webcur.service.external_api.OKXintegration import OKXIntegration
import uvicorn
from webcur.config import CONFIG
import multiprocessing
import asyncio
from webcur.service.injectors import data_queue_injector
import logging

logger = logging.getLogger(__name__)


def background_process(
    data_queue: multiprocessing.Queue
):
    """
    Background process that fetches the data from API and saves it database
    """
    async def run():
        api = [
            # BinanceIntegration(),
            OKXIntegration(data_queue)
        ]
        for api in api:
            logger.info(f'Starting {api.__class__.__name__}')
            await api.run_websocket(
                pair_name=CONFIG['CURRENCY_PAIRS']
            )

    asyncio.run(run())


def app_factory():
    """
    Builds the FastAPI app
    """
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


if __name__ == '__main__':
    data_queue = data_queue_injector()
    app = app_factory()

    multiprocessing.Process(
        target=background_process,
        args=(data_queue,)
    ).start()
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, workers=4)
    server = uvicorn.Server(config)
    server.run()
