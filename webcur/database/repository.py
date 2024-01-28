from typing import Protocol


class DataBaseRepository(Protocol):
    """
    Protocol for the database repository
    """

    async def read(self, pair_name: str) -> float:
        """
        Returns the stored exchange rate for the given pair

        Args:
            pair_name (str): The pair to get the exchange rate for
        """
        ...

    async def write(self, pair_name: str, rate: float) -> None:
        """
        Writes the exchange rate for the given pair

        Args:
            pair_name (str): The pair to write the exchange rate for
            rate (float): The exchange rate to write
        """
        ...


class DummyRepository():
    """
    Dummy repository for testing purposes

    Uses memory to store the exchange rates
    """

    def __init__(self):
        """
        Initializes the repository
        """
        self._rates = {}

    async def read(self, pair_name: str) -> float:
        """
        Returns the stored exchange rate for the given pair

        Args:
            pair_name (str): The pair to get the exchange rate for
        """
        return self._rates[pair_name]

    async def write(self, pair_name: str, rate: float) -> None:
        """
        Writes the exchange rate for the given pair

        Args:
            pair_name (str): The pair to write the exchange rate for
            rate (float): The exchange rate to write
        """
        self._rates[pair_name] = rate
