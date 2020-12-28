try:
    from importlib.metadata import distribution  # type: ignore
except ImportError:
    from importlib_metadata import distribution

from .fdtw import FeatureDTWTransformer
from .metrics import dd_distance, fast_dtw

_distribution = distribution("feature_dtw")

__version__ = _distribution.version


__all__ = ["FeatureDTWTransformer", "dd_distance", "fast_dtw"]
