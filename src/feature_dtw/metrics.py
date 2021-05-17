from typing import Any, Callable

import numpy as np


def dd_distance(
    x: Any, y: Any, a: float, distance: Callable[..., float], **kwargs: Any
) -> float:
    """Combination of metric on original time series and their derivations

    (1 - a) * dist(x, y) + a * dist(x', y')

    Args:
        x (array-like): Sample
        y (array-like: Sample
        a (float): Percentage of derivation in final metric
        distance (Callable[..., float]): Distance measure

    Returns:
        float: Computed distance measure
    """

    # Dynamic window size
    if "window" in kwargs and kwargs["window"] == -1:
        kwargs["window"] = np.ceil(0.1 * np.max((x.shape[0], y.shape[0]))).astype(int)

    return (1 - a) * distance(x, y, **kwargs) + a * distance(
        np.diff(x), np.diff(y), **kwargs
    )
