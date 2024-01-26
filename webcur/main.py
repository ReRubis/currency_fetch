from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from webcur.routes import route
import uvicorn

import os


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

    # os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    return app


app = app_factory()


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
