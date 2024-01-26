from fastapi import APIRouter
from webcur.routes import exchange


def router_factory():
    """
    puts other routes under 1 prefix
    """
    router = APIRouter(
        prefix='/api'
    )
    router.include_router(exchange.router)

    return router


router = router_factory()
