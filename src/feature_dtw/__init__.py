try:
    from importlib.metadata import distribution  # type: ignore
except ImportError:
    from importlib_metadata import distribution

from .fdtw import FeatureDTWTransformer, fastdtw_distance

_distribution = distribution("feature_dtw")

__version__ = _distribution.version


__all__ = ["FeatureDTWTransformer", "fastdtw_distance"]
