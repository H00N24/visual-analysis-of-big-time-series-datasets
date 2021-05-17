from typing import Any

import numpy as np
from sklearn.metrics.pairwise import PAIRWISE_DISTANCE_FUNCTIONS
from tqdm.notebook import tqdm

from .fdtw import FeatureDTWTransformer as _FeatureDTWTransformer


class FeatureDTWTransformer(_FeatureDTWTransformer):
    """Feature DTW transformer

    The Feature DTW transformer [1] transforms a set of time series into a feature space
    representation using randomly selected prototypes [2].

    The `featuredtw.notebook.FeatureDTWTransformer` uses the `tqdm` library to display
    the progress bar of distance computation.

    Args:
        n_components (int, optional): Number of prototypes. Defaults to 30.
        copy_prototypes (bool, optional):
            If True it copies prototypes as standalone `np.ndarray` or only use indices
            from the original X. Defaults to True.
        metric (Union[str, Callable[..., float]], optional):
            Distance measure used for creating feature vectors. It's possible to use any
            distance measure from `sklearn.metrics` or stanalone callabe function.
            Defaults to "euclidean".
        metric_param (dict, optional):
            Parameters for the distance function. Defaults to {}.
        random_state (Optional[int], optional): Random state. Defaults to None.
        n_jobs (Optional[int], optional):
            The number of parallel jobs. Defaults to None.

    References:
        [1] Kate, Rohit. (2015). Using dynamic time warping distances as features for
        improved time series classification. Data Mining and Knowledge Discovery.
        30. 10.1007/s10618-015-0418-x.

        [2] Brian Kenji Iwana, Volkmar Frinken, Kaspar Riesen, Seiichi Uchida,
        Efficient temporal pattern recognition by means of dissimilarity space
        embedding with discriminative prototypes, Pattern Recognition, Volume 64, 2017,
        Pages 268-276, ISSN 0031-3203, https://doi.org/10.1016/j.patcog.2016.11.013.
        (https://www.sciencedirect.com/science/article/pii/S0031320316303739)
    """

    def __pairwise_distances(self, X: Any, Y: Any) -> np.ndarray:
        """Parwise distance with progress bar

        Function for computing distance between two sets of time series with
        progress bar from `tqdm`.

        Args:
            X (array-like, shape (x_sample, x_length)):
                Set of time series of an arbitrary length.
            Y (array-like, shape (y_sample, y_length)):
                Set of time series of an arbitrary length.

        Returns:
            np.ndarray: Distance matrix of shape (x_samples, y_samples)
        """
        if callable(self.metric):
            return np.vstack(
                [
                    [self.metric(x, y, **self.metric_param) for y in Y]
                    for x in tqdm(X, )
                ]
            )
        else:
            return np.vstack(
                [
                    PAIRWISE_DISTANCE_FUNCTIONS[self.metric](
                        [x], Y, **self.metric_param
                    ).flatten()
                    for x in tqdm(X)
                ]
            )
