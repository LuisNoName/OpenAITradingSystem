import abc

from TradingSystem.portfolio import AbstractPortfolio


class AbstractPortfolioManager(abc.ABC):
    """Abstract class for a portfolio manager."""

    @abc.abstractmethod
    def rebalance(self) -> None:
        """Rebalance the portfolio managed by this portfolio manager."""
        pass