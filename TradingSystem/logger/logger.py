import abc
from typing import Any

class AbstractLogger(metaclass=abc.ABCMeta):
    """An abstract class representing a logger."""

    @abc.abstractmethod
    def log(self, message: str, data: Any = None) -> None:
        """Log a message with optional data.

        Args:
            message: The message to log.
            data: Optional data to include in the log entry.
        """
        pass