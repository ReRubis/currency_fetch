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


class OKXCurRateResponse(BaseModel):
    """
    A model for the subscribe message
    """
    arg: WSArgResponse
    data: list[WSDataResponse]


class OKXSubscribeResponse(BaseModel):
    """
    A model for the subscribe message
    """
    event: str
    arg: WSArgResponse
    connId: str
