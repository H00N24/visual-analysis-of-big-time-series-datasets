# Master's Thesis: Visual analysis of big time series datasets


```
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
make cython-fastdtw
pip install -e .
```

```
python -m ipykernel install --user --name masters-thesis --display-name "Master's Thesis"
```

```
nbdime extensions --enable --sys-prefix
nbdime config-git --enable
```