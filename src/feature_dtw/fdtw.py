from typing import Any, Callable, List, Optional, Union

import numpy as np
from sklearn.base import TransformerMixin
from sklearn.metrics import pairwise_distances
from sklearn.utils import check_array, check_random_state


class FeatureDTWTransformer(TransformerMixin):
    def __init__(
        self,
        n_components: int = 30,
        copy_prototypes: bool = True,
        metric: Union[str, Callable[[Any, Any], float]] = "euclidean",
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

        raw_data = self.__check_array(X)

        self._shape = raw_data.shape

        rnd = check_random_state(self.random_state)

        self.index_ = rnd.choice(self._shape[0], self.n_components, replace=False)

        self.prototypes_ = np.array(raw_data[self.index_], copy=self.copy_prototypes)

        return self

    def transform(self, X: Any, y: Any = None) -> np.ndarray:
        raw_data = self.__check_array(X)

        self.distances_ = pairwise_distances(
            raw_data,
            self.prototypes_,
            metric=self.metric,
            n_jobs=self.n_jobs,
            **self.metric_param
        )

        return self.distances_

    def add_protype(self, index: Union[int, List[int]], X: Any) -> np.ndarray:

        if isinstance(index, int):
            index = [index]

        mask = ~np.isin(index, self.index_)

        new_index = np.array(index)[mask]

        raw_data = self.__check_array(X)

        new_prototypes = raw_data[new_index]

        self.distances_ = np.hstack(
            (
                self.distances_,
                pairwise_distances(
                    raw_data,
                    new_prototypes,
                    metric=self.metric,
                    n_jobs=self.n_jobs,
                    **self.metric_param
                ),
            )
        )

        self.prototypes_ = np.vstack((self.prototypes_, new_prototypes))
        self.index_ = np.append(self.index_, new_index)

        return self.distances_

    def remove_prototype(self, index: Union[int, List[int]]) -> np.ndarray:
        if isinstance(index, int):
            index = [index]

        mask = ~np.isin(self.index_, index)

        self.index_ = self.index_[mask]
        self.prototypes_ = self.prototypes_[mask]
        self.distances_ = self.distances_[:, mask]

        return self.distances_

    def __check_array(self, X: Any) -> np.ndarray:
        return check_array(
            X, accept_sparse=False, dtype="numeric", force_all_finite="allow-nan"
        )
