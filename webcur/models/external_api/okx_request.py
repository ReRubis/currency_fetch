from pydantic import BaseModel
from webcur.models.external_api.okx_common import InstId


class SubscribeArgs(BaseModel):
    """
    A model for the subscribe message args
    """
    channel: str = 'mark-price'
    instId: InstId = InstId.BTC_USDT


class SubscribeMessage(BaseModel):
    """
    A model for the subscribe message
    """
    op: str = 'subscribe'
    args: list[SubscribeArgs]
