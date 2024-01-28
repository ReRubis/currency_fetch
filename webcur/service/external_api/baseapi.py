from abc import ABC


class BaseAPI(ABC):
    """
    This class defines the interface for external API.
    """

    async def get_exchange_rates(self, pair_name: str) -> dict:
        """
        Returns the exchange rate for the given pair

        Args:
            pair_name (str): The pair to get the exchange rate for
        """
        ...
