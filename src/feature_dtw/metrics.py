from typing import Any, Callable

import numpy as np
from fastdtw import fastdtw


def fast_dtw(x: Any, y: Any, **kwargs: Any) -> float:
    return fastdtw(x[~np.isnan(x)], y[~np.isnan(y)])[0]


def dd_distance(
    x: Any, y: Any, a: float, metric: Callable[..., float], **kwargs: Any
) -> float:

    return (1 - a) * metric(x, y, **kwargs) + a * metric(
        np.diff(x), np.diff(y), **kwargs
    )
