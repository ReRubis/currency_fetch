from webcur.service.external_api.baseapi import BaseAPI
from webcur.config import CONFIG
import websockets
import asyncio
import json
import time

from webcur.models.external_api.okx_request import (
    SubscribeMessage,
    SubscribeArgs,
)

from webcur.models.external_api.okx_common import InstId
from typing import Iterable
from websockets import WebSocketClientProtocol
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class OKXIntegration(BaseAPI):
    """
    Class that makes call to the OKX API to get the exchange rates
    """

    def __init__(self):
        self.api_key = CONFIG['OKX_API_KEY']
        self.api_secret = CONFIG['OKX_SECRET']
        self.base_uri = CONFIG['OKX_BASE_PUBLIC_URL']

    async def run_websocket(
            self,
            pair_name: Iterable[str],
    ):
        """
        Method that runs the websocket
        """
        uri = self.base_uri
        async with websockets.connect(uri=uri, ping_interval=20) as websocket:
            await self._get_exchange_rates(
                pair_name=pair_name,
                websocket=websocket
            )

    async def _get_exchange_rates(
        self,
        pair_name: Iterable[str],
        websocket: WebSocketClientProtocol,
    ) -> dict:
        """
        Method that makes the call to the OKX API to get the exchange rates
        """

        args = [SubscribeArgs(instId=InstId(pair)) for pair in pair_name]

        subscribe_msg = SubscribeMessage(
            args=args
        )

        await websocket.send(subscribe_msg.model_dump_json())

        while True:
            try:
                response = await websocket.recv()
                data = json.loads(response)

                if data.get('event') == 'subscribe':
                    logger.info(f"Subscribed to {data['arg']['instId']}")

                elif data.get('data'):
                    print(data)
                    logger.info('Received Currency exchange rate' +
                                f'for {data["data"][0]["instId"]}')

                time.sleep(5)

            except websockets.ConnectionClosed:
                logger.info("Connection closed. Reconnecting...")
                break


if __name__ == '__main__':
    service = OKXIntegration()

    async def test_ws():
        await service.run_websocket(
            pair_name=['BTC-USDT', 'ETH-USDT', 'XRP-USDT']
        )
    asyncio.run(test_ws())
