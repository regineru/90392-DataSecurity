# Setting up environment

Here are the instruction to install and set up everything you need for the lab.

1. Download the latest version of miniconda from here https://docs.conda.io/en/latest/miniconda.html and install it by following the instraction in https://conda.io/projects/conda/en/latest/user-guide/install/index.html where you can find a step by step guide for any platform: Windows, Linux or macOS.


2. If you are on either Windows or macOS, when installation is finished, you should find the **Anaconda Prompt** in the list of your programs. The opening of Anaconda Prompt should automatically enable the conda base environment. Otherwise, if you are on Linux, to activate the conda base environment you need to open a **Terminal** and run the following command: 
```
$ conda activate base
```


3. Now you can create a new conda environment named `eads` (that stands for elements of applied data security) by running the following command in the same Anaconda Prompt window or terminal:
```
$ conda create --name eads
```


4. Once created, you need to activate the environment:
```
$ conda activate eads
```


5. Now, you can install some python packages:
```
$ conda install scipy
$ conda install matplotlib
$ conda install pycryptodomex
```


6. Then, you need to install JupyterLab as well as some of its useful extensions:
```
$ conda install jupyterlab
$ conda install ipympl
$ conda install nodejs
$ jupyter labextension install @jupyter-widgets/jupyterlab-manager
$ jupyter labextension install @jupyterlab/toc
$ jupyter labextension install @aquirdturtle/collapsible_headings
```


7. Finally you can start JupyterLab:
```
$ jupyter lab
```

## Opening JupyterLab 

Next time you want to open JupyterLab, you just need to:

1. open a Terminal or Anaconda Prompt


2. activate the `eads` environment
```
$ conda activate eads
```


3. start JupyterLab
```
$ jupyter lab
```

