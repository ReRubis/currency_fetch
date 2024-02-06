from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from webcur.service.external_api.baseapi import BaseAPI
from webcur.routes import route
import uvicorn
import asyncio
from webcur.config import CONFIG
from webcur.service.injectors import okx_integration_injector
from contextlib import asynccontextmanager
import logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def background_process(app: FastAPI):
    """Background process for the FastAPI app

    Starts the websocket connection on FastAPI startup
    """
    api = [
        okx_integration_injector()
    ]

    async def run_websocket(api: BaseAPI):
        await api.run_websocket(
            pair_name=CONFIG['CURRENCY_PAIRS']
        )

    for api in api:
        logger.info(f'Starting {api.__class__.__name__}')
        asyncio.create_task(run_websocket(api))

    yield


def app_factory():
    """
    Builds the FastAPI app
    """
    app = FastAPI(lifespan=background_process)

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
    app = app_factory()

    config = uvicorn.Config(app, host="0.0.0.0", port=8000, workers=4)
    server = uvicorn.Server(config)
    server.run()
