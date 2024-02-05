from webcur.service.external_api.baseapi import BaseAPI
from webcur.config import CONFIG
import websockets
import asyncio
import time
from pydantic import TypeAdapter

from webcur.models.external_api.okx_request import (
    SubscribeMessage,
    SubscribeArgs,
)

from webcur.models.external_api.okx_common import InstId
from webcur.models.external_api.okx_response import (
    OKXCurRateResponse,
    OKXSubscribeResponse
)
from typing import Iterable, Union
from websockets import WebSocketClientProtocol
from multiprocessing import Queue
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


ws_response_adapter = TypeAdapter(
    Union[OKXCurRateResponse, OKXSubscribeResponse])


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

        self._set_queue()

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

                data = ws_response_adapter.validate_json(response)

                if isinstance(data, OKXSubscribeResponse):
                    logger.info(f"Subscribed to {data.arg.instId}")

                elif isinstance(data, OKXCurRateResponse):
                    logger.info('Received Currency exchange rate' +
                                f' for {data.data[0].instId}')
                    await self._update_stored_values(data=data)

                time.sleep(5)

            except websockets.ConnectionClosed:
                logger.info("Connection closed. Reconnecting...")
                break

    def _set_queue(self) -> None:
        """
        Sets the initial state of the queue
        """
        if self.queue.empty():
            data = {
                'BTC-USDT': None,
                'ETH-USDT': None,
                'XRP-USDT': None,
            }
            logger.debug('Setting the initial state of the queue')
            self.queue.put(data)

    async def _update_stored_values(self, data: OKXCurRateResponse) -> None:
        """
        Method that updates the stored values
        """

        ic = data.data[0]
        stored_data = self.queue.get()
        stored_data[ic.instId] = ic
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
