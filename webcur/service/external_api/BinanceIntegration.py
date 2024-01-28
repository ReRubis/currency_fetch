from webcur.service.external_api.baseapi import BaseAPI


class BinanceIntegration(BaseAPI):
    """
    Class that makes call to the Binance API to get the exchange rates
    """

    async def get_exchange_rates(self, pair_name: str) -> dict:
        """
        Returns the exchange rate for the given pair

        Args:
            pair_name (str): The pair to get the exchange rate for
        """
        return {'Binance': 'Binance'}
