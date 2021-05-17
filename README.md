# Master's Thesis: Visual Analysis of Big Time Series Datasets
This repository contains all source codes for my master thesis,
*Visual Analysis of Big Time Series Datasets*, including our implementation of the
*Feature DTW transformation* and the *Multi-Component Feature DTW transformation*.


The structure of this repository is:
* `notebooks` - Jupyter notebooks with all of our tests and implementation of our analytic pipeline
* `src/feature_dtw` - source codes for Feature DTW package
* `results` - Results from our tests on UCR datasets in CSV format
* `thesis `- LaTeX source codes of the thesis's text

## Feature DTW Package
This package contains Python implementation of *Feature DTW* transformation [[1]](#1) and its prototyped version [[2]](#2).

Our implementation is following the well-known [Scikit-learn] transformer API.
### Installation
Firstly we clone our repository:
```
$ git clone https://github.com/H00N24/visual-analysis-of-big-time-series-datasets.git visual-analysis
$ cd visual-analysis
```

Our package is working for Python 3.8 and above. To install our package simply use
```
$ pythom3.8 -m pip install .
```
We highly recommend to use a virtual environment for installing and testing our package.

Once our package is installed try:
```
$ python -c "import feature_dtw; print(feature_dtw.__version__)"
1.0.0
```
### Example Usage
```python
import numpy as np
import pandas as pd
from dtaidistance import dtw

from feature_dtw import FeatureDTWTransformer, MultiComponentFDTWTransformer
```

#### Time Series Dataset
```python
ts_dataset = np.array(
    [
        [17, 21, 30, 2, 10],
        [16, 15, 4, 3, 9],
        [19, 43, 14, 41, 43],
        [46, 3, 38, 29, 19],
        [18, 10, 16, 36, 6],
        [29, 19, 2, 26, 9],
        [8, 41, 10, 13, 44],
        [7, 38, 34, 20, 20],
    ]
)
```

#### Feature DTW transformation
```python
fdtw = FeatureDTWTransformer(
    n_components=2,
    metric=dtw.distance,
    metric_param=dict(window=2, use_pruning=True),
    random_state=42,
)

fdtw.fit_transform(ts_dataset)
```
Out:
```
array([[16.03121954, 22.93468988],
       [ 0.        , 21.88606863],
       [56.0357029 , 42.96510212],
       [50.53711507, 28.26658805],
       [30.91924967, 19.87460691],
       [21.88606863,  0.        ],
       [45.16635916, 46.08687449],
       [39.89987469, 35.65108694]])
```

#### Multi-Component Time Series Dataset
```python
comp_1 = np.array(
    [
        [40, 21, 9, 41, 45],
        [27, 35, 10, 23, 35],
        [5, 28, 0, 8, 43],
        [47, 14, 38, 14, 12],
        [38, 25, 20, 36, 20],
        [27, 41, 30, 47, 26],
        [20, 25, 30, 8, 13],
        [33, 24, 24, 16, 40],
    ]
)

comp_2 = np.array(
    [
        [46, 40, 7, 27, 3, 44, 38],
        [3, 17, 1, 44, 23, 17, 11],
        [40, 15, 47, 26, 14, 26, 9],
        [4, 46, 25, 3, 4, 40, 13],
        [43, 0, 28, 24, 36, 46, 27],
        [18, 41, 5, 19, 6, 33, 42],
        [9, 4, 2, 37, 39, 18, 15],
        [41, 26, 35, 26, 35, 38, 16],
    ]
)

comp_3 = np.array(
    [
        [18, 27, 12],
        [11, 30, 25],
        [9, 36, 14],
        [33, 1, 9],
        [7, 24, 47],
        [48, 2, 18],
        [24, 31, 48],
        [15, 46, 12],
    ]
)
```
#### Multi-Component Feature DTW Transformation
```python
mcfdtw = MultiComponentFDTWTransformer(
    n_transformers=[
        FeatureDTWTransformer(n_components=3, metric="euclidean", random_state=42),
        FeatureDTWTransformer(
            n_components=2,
            metric=dtw.distance,
            metric_param=dict(window=2, use_pruning=True),
            random_state=42,
        ),
        FeatureDTWTransformer(n_components=3, metric="chebyshev", random_state=42),
    ]
)

mcfdtw.fit_transform([comp_1, comp_2, comp_3])
```
Out:
```
array([[28.10693865, 37.50999867,  0.        , 66.12866247,         inf,
        13.        , 30.        ,  0.        ],
       [ 0.        , 33.06055051, 28.10693865,  0.        , 52.87721627,
         0.        , 37.        , 13.        ],
       [30.3644529 , 57.99137867, 49.47726751, 41.        , 46.87216658,
        11.        , 39.        ,  9.        ],
       [47.27578661, 49.77951386, 52.50714237, 53.09425581, 39.49683532,
        29.        , 15.        , 26.        ],
       [26.73948391, 25.17935662, 28.12472222, 56.57738064, 36.18010503,
        22.        , 41.        , 35.        ],
       [33.06055051,  0.        , 37.50999867, 52.87721627,  0.        ,
        37.        ,  0.        , 30.        ],
       [35.4682957 , 44.66542287, 54.49770637, 15.03329638, 54.19409562,
        23.        , 30.        , 36.        ],
       [20.66397832, 38.96151948, 30.5450487 , 51.33225107, 47.0637865 ,
        16.        , 44.        , 19.        ]])
```



## Set-up the Work Environment
In this section we will provide guide to set-up your work environment.

We are using [Nix], [direnv], and [Poetry],
to maintain a fully reproducible environment. We highly recommend to use these tools.
#### With Nix, direnv, and Poetry
If you have both [Nix] and [direnv] available you can simply use:
```
$ direnv allow
```
[direnv] uses the `.envrc` file and prepares the full work environment.

or without [direnv]:
```
$ nix-shell
$ poetry install
```

#### Without Recommended Tools
```
$ python3.8 -m venv .venv
$ pip install -r requirements.txt -r requirements-dev.txt
$ pip install .
```

### Jupyter Kernel
We are using [Jupyter] for all of our testing and data science work. As we are using python
virtual environment we have to set-up new IPython kernel pointing towards our virtual environment.
```
python -m ipykernel install --user --name masters-thesis --display-name "Master's Thesis"
```

## References
<a id="1">[1]</a>  Kate, Rohit. (2015). Using dynamic time warping distances as features for improved time series classification. Data Mining and Knowledge Discovery. 30. 10.1007/s10618-015-0418-x.

<a id="2">[2]</a> Brian Kenji Iwana, Volkmar Frinken, Kaspar Riesen, Seiichi Uchida,
Efficient temporal pattern recognition by means of dissimilarity space embedding with discriminative prototypes,
Pattern Recognition, Volume 64, 2017, Pages 268-276, ISSN 0031-3203,
https://doi.org/10.1016/j.patcog.2016.11.013.
(https://www.sciencedirect.com/science/article/pii/S0031320316303739)


The complete bibliography of my master's thesis is listed in `thesis/bib/`.

## BibTeX
```
@MastersThesis{Kurákthesis,
    AUTHOR = "KURÁK, Ondrej",
    TITLE = "Visual Analysis of Big Time Series Datasets [online]",
    YEAR = " [cit. 2021-05-17]",
    TYPE = "Master's thesis",
    SCHOOL = "Masaryk University, Faculty of Informatics, Brno",
    SUPERVISOR = "Barbora Kozlíková",
    URL = "Available from WWW <https://is.muni.cz/th/zd4lj/>",
}
```

[Nix]: https://nixos.org/
[Poetry]: https://python-poetry.org/
[direnv]: https://direnv.net/
[Jupyter]: https://jupyter.org/
[Scikit-learn]: https://scikit-learn.org/stable/

