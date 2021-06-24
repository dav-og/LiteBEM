# LiteBEM
A lightweight, Apache 2.0 distribution of Matthieu Ancellin's Capytaine BEM code.

## Requirements
  - Conda is recommended for managing your Python distribution, dependencies and environment:
    - https://docs.conda.io/en/latest/miniconda.html 
    - Current development efforts are based on Python 3.9

## Installation for Developers
Recommended approach:

- Open a conda powershell and create a new environment for LiteBEM-related development (e.g. "liteBemDev")
  ```shell
  > conda create --name liteBemDev
  ```
- Install numpy (numpy's f2py is required to compile Fortran code) within your LiteBEM development environment:
  ```shell
  > conda activate liteBemDev
  > conda install numpy
  ```
  - **TODO:** Other dependencies can be defined in `setup(install_requires=[])` in `setup.py`
- Clone the LiteBEM repo to your preferred location (e.g. "C:/code/")
  ```shell
  > cd C:/code/
  > git clone https://github.com/dav-og/LiteBEM.git
  ```
- Install LiteBEM as a developer!
  ```shell
  > cd LiteBEM
  > python setup.py develop
  ```

## Run Tests

- Make sure `pytest` is installed in your working environment:
  ```shell
  (liteBemDev) > conda list
  ```
  - if its not installed then do:
    ```shell
    (liteBemDev) > conda install pytest
    ```

- Navigate to `LiteBEM/tests/unit` and run:
  ```shell
  (liteBemDev) > pytest unit_tests.py
  ```
