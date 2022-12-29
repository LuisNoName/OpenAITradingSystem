import abc
from typing import Dict, Any, List

class AbstractDataProvider(metaclass=abc.ABCMeta):
    """An abstract class for a data provider.

    A data provider is responsible for providing data to the trading system. This
    includes both historical and real-time data.

    Attributes:
        _data: A dictionary of data provided by the data provider. The keys are
            the names of the data, and the values are the actual data.
    """
    def __init__(self, data_sources: List[str]) -> None:
        self.data_sources: List[str] = data_sources
        self.price_subscriptions: List = []

    @abc.abstractmethod
    def get_price_data(self, symbols: List[str]) -> Dict[str, Any]:
        """Get data for the given symbols.

        Args:
            symbols: A list of symbols for which to get data.

        Returns:
            A dictionary where the keys are the symbols and the values are the
            data for the symbols.
        """
        pass

    @abc.abstractmethod
    def get_fundamental_data(self, symbols: List[str]) -> Dict[str, Any]:
        """Get fundamental data for the given symbols.

        Args:
            symbols: A list of symbols for which to get fundamental data.

        Returns:
            A dictionary where the keys are the symbols and the values are the
            fundamental data for the symbols.
        """
        pass

    @abc.abstractmethod
    def get_market_data(self, symbols: List[str]) -> Dict[str, Any]:
        pass