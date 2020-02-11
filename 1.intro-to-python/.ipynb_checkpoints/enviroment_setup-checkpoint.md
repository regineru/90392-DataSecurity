# Setting up environment

1. download anaconda via https://www.anaconda.com/download

2. create a conda environment
```shell
$ conda create --name eads python=3.6
```
3. activate environment
```shell
$ conda activate eads
```

4. install python  packages
```shell
$ conda install scipy
$ conda install -c bioconda bitstring
```

5. install JupyterLab and its extension
```shell
$ conda install -c conda-forge jupyterlab
$ conda install nodejs
$ jupyter labextension install @lckr/jupyterlab_variableinspector
$ jupyter labextension install @jupyterlab/toc
$ jupyter labextension install @aquirdturtle/collapsible_headings
```