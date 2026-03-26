# Requirements

To use the envirionment you need to install:

* [Pixi](https://pixi.prefix.dev/latest/installation/)
* [PyMol](https://www.pymol.org/)
* If you are on window to use git you need to install [git](https://git-scm.com/install/windows), verify you have git bash installed after this step.


# Download the project

To download the project:

1. Open a terminal (on widows use git bash)
2. Clone the project with the command: `git clone https://github.com/fauchonj/PIMS.git`

# Install the environment

You can now open the directory you just created with VSCode. To install the environment:
1. Open a terminal in VSCode (`ctrl+shit+p` and write "Create a new terminal")
2. Run `pixi install`
3. Now every time you want to use python in your terminal do:
   1. `pixi shell`
   2. `python ...`

# Introduction to TDA

In the directory **src/tp_pims** you can find the file **TP_1_PIMS.ipynb** which is a working jupyter notebook to use TDA on small proteins.

Open this file and on the top right of the file select **Select Kernel**. You should see a line **default(Python 3.14.3 ...)**. Select this line and now you can run the notebook.