# LiteBEM
A lightweight BEM solver based on Matthieu Ancellin's refactored Nemoh code (libDelhommeau).

## Installation for Developers
Recommended approach:
- Install the latest version of conda:
  - https://docs.conda.io/en/latest/miniconda.html 
- Open a conda powershell and create a new environment for LiteBEM-related development (e.g. "liteBemDev")
  - `>> conda create --name liteBemDev`
- Install some dependencies within your LiteBEM development environment:
  - `>> conda activate liteBemDev`
  - `>> conda install numpy`
  - `>> conda deactivate liteBemDev`
- Now clone the LiteBEM repo to your preferred location (e.g. "C:/code/")
  - `>> cd C:/code/`
  - `>> git clone https://github.com/dav-og/LiteBEM.git`
- Now install LiteBEM as a developer!
  - `>> cd LiteBEM`
  - `>> python setup.py develop`
