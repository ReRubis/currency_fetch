from abc import ABC, abstractmethod


class BaseAPI(ABC):
    """
    This class defines the interface for external API.
    """

    @abstractmethod
    async def run_websocket(self, pair_name: str) -> None:
        """
        Method that runs the websocket
        """
        ...

    @abstractmethod
    async def get_exchange_rates(self, pair_name: str) -> dict:
        """
        Returns the exchange rate for the given pair

        Args:
            pair_name (str): The pair to get the exchange rate for
        """
        ...

    @abstractmethod
    async def return_rates(self) -> dict:
        """
        Returns all rates stored in attributes
        """
        ...
