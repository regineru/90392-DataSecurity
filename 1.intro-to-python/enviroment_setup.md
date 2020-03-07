# Setting up environment

1. download anaconda via https://www.anaconda.com/download and install it. If you need, the anaconda documentation (https://docs.anaconda.com/anaconda/install/) provides a step by step guide for the installation on any platform.


2. If you are on Windows, you just open **Anaconda Prompt**. On Linux or macOS open a **Terminal** and activate the base conda envirnment: 
```
$ conda activate base
```


3. create a new conda environment with name eads
```
$ conda create --name eads python=3.7
```


4. activate environment
```
$ conda activate eads
```


5. install python  packages
```
$ conda install -c anaconda scipy
$ conda install -c conda-forge matplotlib
```


6. install JupyterLab and its extension
```
$ conda install -c conda-forge jupyterlab==1.2.6
$ conda install nodejs
$ jupyter labextension install @lckr/jupyterlab_variableinspector
$ jupyter labextension install @jupyterlab/toc
$ jupyter labextension install @aquirdturtle/collapsible_headings
```


7. start JupyterLab:
```
$ jupyter lab
```