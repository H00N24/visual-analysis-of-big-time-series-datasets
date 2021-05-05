# Master's Thesis: Visual analysis of big time series datasets


```
python3 -m venv .venv
. .venv/bin/activate
pip install pystan==2.19.1.1
pip install -r requirements.txt -r requirements-dev.txt
make cython-fastdtw
pip install -e .
```

```
python -m ipykernel install --user --name masters-thesis --display-name "Master's Thesis"
```

```
jupyter contrib nbextension install --sys-prefix
jupyter nbextension enable jupyter-black-master/jupyter-black
```


```
nbdime extensions --enable --sys-prefix
nbdime config-git --enable
jupyter labextension install @jupyter-widgets/jupyterlab-manager
```
