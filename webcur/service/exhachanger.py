from webcur.service.external_api.baseapi import BaseAPI


class ExchangeRatesService():
    """
    This class

    Args:
        - repository: Any class that implements the
        DataBaseRepository interface

        - queue_value: The value that is stored in the queue
    """

    def __init__(
        self,
        integrations: list[BaseAPI],
    ):
        self.integrations = integrations

    async def return_rates_list(self) -> dict:
        """
        Returns all rates in the database
        """

        return {'data': await self.integrations[0].return_rates()}

    async def return_rate(self, pair_name) -> dict:
        """
        Returns rates for the given pair

        Args:
            pair_name (str): The pair to get the exchange rate for
        """
        return await self.integrations[0].get_exchange_rates(pair_name)
