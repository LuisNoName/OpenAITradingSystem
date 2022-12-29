import abc
from typing import Dict, Any


class AbstractTrader(abc.ABC):
    """An abstract class representing a trader."""

    @abc.abstractmethod
    def send_order(self, order: Dict[str, Any]) -> Dict[str, Any]:
        """Send an order to the broker.

        Args:
            order: The order to send.

        Returns:
            A dictionary containing information about the order, such as the order ID, status, and any errors.
        """
        pass

    @abc.abstractmethod
    def cancel_order(self, order_id: str) -> Dict[str, Any]:
        """Cancel an order with the given ID.

        Args:
            order_id: The ID of the order to cancel.

        Returns:
            A dictionary containing information about the cancellation, such as the order ID, status, and any errors.
        """
        pass

    @abc.abstractmethod
    def get_order_status(self, order_id: str) -> Dict[str, Any]:
        """Get the status of an order with the given ID.

        Args:
            order_id: The ID of the order to check.

        Returns:
            A dictionary containing information about the order, such as the order ID, status, and any errors.
        """
        pass
