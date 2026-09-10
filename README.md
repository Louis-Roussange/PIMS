# PDF of our work
https://github.com/Louis-Roussange/PIMS/blob/main/Projet_PIMS_2026.pdf 
(PIMS = Projet d'Interaction entre les Mathématiques et la SVT)

# Requirements

To use the envirionment you need to install:

* [Pixi](https://pixi.prefix.dev/latest/installation/)
* [PyMol](https://www.pymol.org/) ( optional )
* If you are on window to use git you need to install [git](https://git-scm.com/install/windows), verify you have git bash installed after this step.


# Download the project

To download the project:

1. Open a terminal (on widows use git bash)
2. Clone the project with the command: `git clone https://github.com/Louis-Roussange/PIMS.git`

( This project was made from the original repository `https://github.com/fauchonj/PIMS.git` )

# Install the environment

You can now open the directory you just created with VSCode. To install the environment:
1. Open a terminal in VSCode (`ctrl+shit+p` and write "Create a new terminal")
2. Run `pixi install`
3. Now every time you want to use python in your terminal do:
   1. `pixi shell`
   2. `python ...`

# Introduction to TDA

In the directory **src/tp_pims** you can find the file **Main_PIMS.ipynb** which is a working jupyter notebook to use TDA on small proteins.

Open this file and on the top right of the file select **Select Kernel**. You should see a line **default(Python 3.14.3 ...)**. Select this line and now you can run the notebook.

# checking

Verify the presence of files inside the directory **data** if it is empty, add a set of protein's datas 
**PIMS_Infos organismes.md** should contain the original dataset of 152 proteins to study

# last instructions

Make sure to follow the instructions described at the beginning of the file **Main_PIMS.ipynb**

# optional

run other directorys like :
**TP_1_PIMS.ipynb**               original directory from fauchonj
**TP_1_PIMS_all_proteins.ipynb**  same directory with answers

**TP_Pipeline gaspard.ipynb**     directory made by Gaspard to try finding Globins among Proteins.
**main_pims_1_gaspard.ipynb**     directory made by Gaspard from TP1

Phylogenetic Trees : 
**arbre_phylo_rlmc.txt**          tree obtained after TDA + RLMC process 

Matrix obtained :
**matrice_wasserstein.txt**            Matrix obtaines after TDA + Wasserstein distances on all dataset.
**matrice_distances_embeddings.csv**   Matrix obtained by using an Ai embedding system instead of TDA



