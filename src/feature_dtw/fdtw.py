from typing import Any, Callable, Iterable, List, Optional, Union

import numpy as np
from sklearn.base import TransformerMixin
from sklearn.metrics import pairwise_distances
from sklearn.utils import check_array, check_random_state


class FeatureDTWTransformer(TransformerMixin):
    """Feature DTW transformer

    The Feature DTW transformer [1] transforms a set of time series into a feature space
    representation using randomly selected prototypes [2].

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

    def __init__(
        self,
        n_components: int = 30,
        copy_prototypes: bool = True,
        metric: Union[str, Callable[..., float]] = "euclidean",
        metric_param: dict = {},
        random_state: Optional[int] = None,
        n_jobs: Optional[int] = None,
    ) -> None:
        self.n_components = n_components
        self.random_state = random_state
        self.copy_prototypes = copy_prototypes
        self.metric = metric
        self.metric_param = metric_param
        self.n_jobs = n_jobs

    def fit(self, X: Any, y: Any = None) -> "FeatureDTWTransformer":
        """Fits the estimator

        Selects indices of new prototypes (`self.indices_` of shape (n_components, )).

        Args:
            X (array-like of shape (n_samples, length)):
                The input time series.
            y (Any, optional):
                Ignored. Maintained only for API consistency. Defaults to None.

        Returns:
            FeatureDTWTransformer: Fitted estimator
        """

        raw_data = self.__check_array(X)

        self._shape = raw_data.shape

        rnd = check_random_state(self.random_state)

        self.index_ = rnd.choice(self._shape[0], self.n_components, replace=False)

        self.prototypes_ = np.array(raw_data[self.index_], copy=self.copy_prototypes)

        return self

    def transform(self, X: Any, y: Any = None) -> np.ndarray:
        """Transforming time series into a feature space representation

        Transformation into a feature space representation
        of shape (n_samples, n_components)

        Args:
            X (array-like of shape (n_samples, length)): The input time series.
            y (Any, optional):
                Ignored. Maintained only for API consistency. Defaults to None.

        Returns:
            np.ndarray: Feature space representation of shape (n_samples, n_components)
        """
        raw_data = self.__check_array(X)

        self.distances_ = self.__pairwise_distances(
            raw_data,
            self.prototypes_,
        )

        return self.distances_

    def fit_transform(self, X: Any, y: Any = None) -> np.ndarray:
        """Fitting & Transformation

        Fits the estimator and transforms X into a feature space representation
        of shape (n_samples, n_components)

        Args:
            X (array-like of shape (n_samples, length)): The input time series.
            y (Any, optional):
                Ignored. Maintained only for API consistency. Defaults to None.

        Returns:
            np.ndarray: Feature space representation of shape (n_samples, n_components)
        """
        self.fit(X, y)

        return self.transform(X, y)

    def add_protype(self, X: Any, index: Union[int, List[int]]) -> np.ndarray:
        """Adding new prototype

        Adding new prototypes to the Feature DTW estimator.

        Args:
            X (array-like of shape (n_samples, length)): The input time series.
            index (Union[int, List[int]]): Index or list of indices of new prototypes.

        Returns:
            np.ndarray: Transformation of X into a feature space including newly
            selected prototypes. Shape (n_samples, n_components)

        """

        if isinstance(index, int):
            index = [index]

        mask = ~np.isin(index, self.index_)

        new_index = np.array(index)[mask]

        raw_data = self.__check_array(X)

        new_prototypes = raw_data[new_index]

        self.distances_ = np.hstack(
            (
                self.distances_,
                self.__pairwise_distances(
                    raw_data,
                    new_prototypes,
                ),
            )
        )

        self.prototypes_ = np.vstack((self.prototypes_, new_prototypes))
        self.index_ = np.append(self.index_, new_index)

        return self.distances_

    def remove_prototype(self, index: Union[int, List[int]]) -> np.ndarray:
        """Removing prototype

        Removing prototype from the Feature DTW estimator

        Args:
            index (Union[int, List[int]]):
                Index or list of indices of new prototypes to remove.

        Returns:
            np.ndarray: Transformation of X into a feature space without removed
            selected prototypes. Shape (n_samples, n_components)
        """
        if isinstance(index, int):
            index = [index]

        mask = ~np.isin(self.index_, index)

        self.index_ = self.index_[mask]
        self.prototypes_ = self.prototypes_[mask]
        self.distances_ = self.distances_[:, mask]

        return self.distances_

    def __check_array(self, X: Any) -> np.ndarray:
        """Checking the validity of an input array

        Helper function for checking the validity of input.

        Args:
            X (array-like of shape (n_samples, length)): The input time series.

        Returns:
            np.ndarray: X
        """
        return check_array(
            X, accept_sparse=False, dtype="numeric", force_all_finite="allow-nan"
        )

    def __pairwise_distances(self, X: Any, Y: Any) -> np.ndarray:
        """Parwise distance

        Function for computing distance between two sets of time series.

        Args:
            X (array-like, shape (x_sample, x_length)):
                Set of time series of an arbitrary length.
            Y (array-like, shape (y_sample, y_length)):
                Set of time series of an arbitrary length.

        Returns:
            np.ndarray: Distance matrix of shape (x_samples, y_samples)
        """
        return pairwise_distances(
            X, Y, metric=self.metric, n_jobs=self.n_jobs, **self.metric_param
        )


class MultiComponentFDTWTransformer(TransformerMixin):
    """Multi-Component Feature DTW Transformer

    This class combines multiple underlying Feature DTW transformers into a single
    transformer for multi-component time series. To maintain high flexibility we are
    using several pre-prepared Feature DTW tranformers.

    Args:
        n_transformers (List[FeatureDTWTransformer]):
            List of underlying Feature DTW transformers
    """

    def __init__(self, n_transformers: List[FeatureDTWTransformer]) -> None:
        self.transformers = n_transformers

    def fit(self, X: Iterable[Any], y: Any = None) -> "MultiComponentFDTWTransformer":
        """Fiting the underlying FDTW transformers

        Args:
            X (Iterable[array-like], shape (n_transformers, x_sample, x_length)):
                The input multi-component time series divided by each component into
                multiple arrays.
            y (Any, optional):
                Ignored. Maintained only for API consistency. Defaults to None.

        Returns:
            MultiComponentFDTWTransformer: Fitted estimator
        """
        for transformer, x in zip(self.transformers, X):
            transformer.fit(x, y)

        return self

    def transform(self, X: Iterable[Any], y: Any = None) -> np.ndarray:
        """Transforming multi-component time series into a feature space representation

        Args:
            X (Iterable[array-like], shape (n_transformers, x_sample, x_length)):
                The input multi-component time series divided by each component into
                multiple arrays.
            y (Any, optional):
                Ignored. Maintained only for API consistency. Defaults to None.

        Returns:
            np.ndarray:
                Transformed multi-component time series into a feature space of shape
                (n_samples, n_transformers * n_components)

        """
        return np.hstack(
            [
                transformer.transform(x, y)
                for transformer, x in zip(self.transformers, X)
            ]
        )

    def fit_transform(self, X: Iterable[Any], y: Any = None) -> np.ndarray:
        """Fitting & Transformation

        Args:
            X (Iterable[array-like], shape (n_transformers, x_sample, x_length)):
                The input multi-component time series divided by each component into
                multiple arrays.
            y (Any, optional):
                Ignored. Maintained only for API consistency. Defaults to None.

        Returns:
            np.ndarray: [description]
        """
        self.fit(X, y)

        return self.transform(X, y)

    @property
    def indices_(self) -> List[np.ndarray]:
        """Indices of underlying Feature DTW transformers

        Returns:
            List[np.ndarray]: List of indices
        """
        return [transformer.index_ for transformer in self.transformers]

    def add_prototypes(
        self, X: Iterable[Any], indices: Iterable[Union[int, List[int]]]
    ) -> np.ndarray:
        """[summary]

        Args:
            X (Iterable[array-like], shape (n_transformers, x_sample, x_length)):
                The input multi-component time series divided by each component into
                multiple arrays.
            indices (Iterable[Union[int, List[int]]]):
                List of new indices for underlying estimators

        Returns:
            np.ndarray:
                Transformed multi-component time series into a feature space of shape
                (n_samples, n_transformers * n_components)
        """
        return np.hstack(
            [
                transformer.add_protype(x, index)
                for transformer, x, index in zip(self.transformers, X, indices)
            ]
        )

    def remove_prototypes(self, indices: Iterable[Union[int, List[int]]]) -> np.ndarray:
        """Remove prototypes from underlying FDTW transformers

        Args:
            indices (Iterable[Union[int, List[int]]]):
                List of indices to remove for underlying estimators

        Returns:
            np.ndarray:
                Transformed multi-component time series into a feature space of shape
                (n_samples, n_transformers * n_components)
        """
        return np.hstack(
            [
                transformer.remove_prototype(index)
                for transformer, index in zip(self.transformers, indices)
            ]
        )
