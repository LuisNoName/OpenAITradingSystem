import abc
from typing import Dict, Any, List


class AbstractStrategy(abc.ABC):
    """Abstract base class for portfolio construction and rebalancing strategies."""

    @abc.abstractmethod
    def get_returns(self, data: Dict[str, Any]) -> float:
        """Calculate the returns of the portfolio over a given period of time.

        Args:
            data: The data to use for calculating the returns.

        Returns:
            The returns of the portfolio.
        """
        pass

    @abc.abstractmethod
    def get_risk(self, data: Dict[str, Any]) -> float:
        """Calculate the risk of the portfolio.

        Args:
            data: The data to use for calculating the risk.

        Returns:
            The risk of the portfolio.
        """
        pass

    @abc.abstractmethod
    def rebalance(self, data: Dict[str, Any]) -> None:
        """Adjust the portfolio weights to align with the goals and constraints of the strategy.

        Args:
            data: The data to use for rebalancing the portfolio.
        """
        pass

    @abc.abstractmethod
    def get_asset_universe(self) -> List[str]:
        """Get the list of assets that are eligible for inclusion in the portfolio.

        Returns:
            The list of eligible assets.
        """
        pass

    @abc.abstractmethod
    def set_portfolio(self, weights: Dict[str, float]) -> None:
        """Set the current portfolio.

        Args:
            weights: The weights of each asset in the portfolio.
        """
        pass
