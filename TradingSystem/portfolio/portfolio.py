import abc
from typing import List

from TradingSystem.data import AbstractDataProvider
from TradingSystem.strategy import AbstractStrategy


class AbstractPortfolio(abc.ABC):
    """An abstract portfolio."""

    @abc.abstractmethod
    def set_portfolio(self, data_provider: AbstractDataProvider, strategies: List[AbstractStrategy]) -> None:
        """Set the portfolio with the given symbols and weights.

        Args:
            symbols: A list of symbols to include in the portfolio.
            weights: A list of weights corresponding to the symbols. The weights
                should sum to 1.
        """
        pass

    @abc.abstractmethod
    def rebalance(self):
        """ Rebalance the strategy. """
        pass

    @abc.abstractmethod
    def add_strategy(self, strategy: AbstractStrategy):
        """ Add a new strategy to the portfolio. """
        pass

    @abc.abstractmethod
    def remove_strategy(self, strategy: AbstractStrategy):
        """ Add a new strategy to the portfolio. """
        pass

    @abc.abstractmethod
    def get_asset_universe(self) -> List[str]:
        """Get the symbols in the portfolio."""
        pass

    @abc.abstractmethod
    def get_risk(self) -> float:
        """Get the risk of the portfolio."""
        pass

    @abc.abstractmethod
    def get_returns(self) -> float:
        """Get the returns of the portfolio."""
        pass
