try:
    from importlib.metadata import distribution  # type: ignore
except ImportError:
    # Fallback for older Python version
    from importlib_metadata import distribution

from .fdtw import FeatureDTWTransformer, MultiComponentFDTWTransformer
from .metrics import dd_distance

_distribution = distribution("feature_dtw")

__version__ = _distribution.version


__all__ = [
    "FeatureDTWTransformer",
    "MultiComponentFDTWTransformer",
    "dd_distance",
]
