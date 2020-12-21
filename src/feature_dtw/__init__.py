import logging
from importlib.metadata import distribution

_distribution = distribution("feature_dtw")

__version__ = _distribution.version

logger = logging.getLogger(__name__)


def say_hello(name: str = "world") -> None:
    """
    Print a greeting.

    >>> say_hello()
    Hello, world!
    """

    logging.debug("Saying 'Hello %s!'", name)
    print(f"Hello, {name}!")
