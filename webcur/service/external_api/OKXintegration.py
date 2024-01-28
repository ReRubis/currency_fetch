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
from multiprocessing import Queue
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# TODO: Add Pydantic model for the WS response
# That will remove the hard-coded strings


class OKXIntegration(BaseAPI):
    """
    Class that makes call to the OKX API to get the exchange rates

    Args:
        data_queue (Queue): The queue to store the data
    """

    def __init__(self, data_queue: Queue):
        self.api_key = CONFIG['OKX_API_KEY']
        self.api_secret = CONFIG['OKX_SECRET']
        self.base_uri = CONFIG['OKX_BASE_PUBLIC_URL']
        self.queue = data_queue

    async def run_websocket(
            self,
            pair_name: Iterable[str],
    ) -> None:
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
    ) -> None:
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
                    logger.info('Received Currency exchange rate' +
                                f' for {data["data"][0]["instId"]}')
                    await self._update_stored_values(data=data)

                time.sleep(5)

            except websockets.ConnectionClosed:
                logger.info("Connection closed. Reconnecting...")
                break

    async def _update_stored_values(self, data: dict) -> None:
        """
        Method that updates the stored values
        """

        # Short from input_currency
        # TODO: Change the variable name and remove strings
        ic = data['data'][0]

        if self.queue.empty():
            data = {
                'BTC-USDT':
                ic['instId'] if ic['instId'] == 'BTC-USDT' else None,
                'ETH-USDT':
                ic['instId'] if ic['instId'] == 'BTC-USDT' else None,
                'XRP-USDT':
                ic['instId'] if ic['instId'] == 'BTC-USDT' else None,
            }
            logger.debug('Stored data is None. Adding stored data')
            self.queue.put(data)

        else:
            stored_data = self.queue.get()
            stored_data[ic['instId']] = ic
            logger.debug('Updating the stored data')
            self.queue.put(stored_data)


if __name__ == '__main__':
    data_queue = Queue()
    service = OKXIntegration(data_queue)

    async def test_ws():
        await service.run_websocket(
            pair_name=['BTC-USDT', 'ETH-USDT', 'XRP-USDT']
        )
    asyncio.run(test_ws())
