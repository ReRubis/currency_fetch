from pydantic import BaseModel
from webcur.models.external_api.okx_common import InstId


class WSArgResponse(BaseModel):
    """
    A model for the subscribe message args
    """
    channel: str
    instId: InstId


class WSDataResponse(BaseModel):
    """
    A model for the subscribe message args
    """
    instId: InstId
    instType: str
    markPx: str
    ts: str


class WSCurRateResponse(BaseModel):
    """
    A model for the subscribe message
    """
    arg: WSArgResponse
    data: list[dict]
