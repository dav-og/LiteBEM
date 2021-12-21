# LiteBEM
A lightweight, Apache 2.0 distribution of Matthieu Ancellin's Capytaine BEM code.

## Requirements
  - Conda is recommended for managing your Python distribution, dependencies and environment:
    - https://docs.conda.io/en/latest/miniconda.html 
    - Current development efforts are based on Python 3.9

## Installation for Users (Linux Only)
Recommended approach:

- Open a conda powershell and create a new environment for the LiteBEM project (e.g. "liteBemProject")
  ```shell
  > conda create --name liteBemProject python
  ```
- Install LiteBEM from PyPI by entering the following command within your new environment
-   ```shell
    > conda activate liteBemProject
    > python -m pip install LiteBEM
    ```

## Installation for Developers (Linux Only)
Recommended approach:

- Open a conda powershell and create a new environment for LiteBEM-related development (e.g. "liteBemDev")
  ```shell
  > conda create --name liteBemDev python
  ```
- Install numpy (numpy's f2py is required to compile Fortran code) within your LiteBEM development environment:
  ```shell
  > conda activate liteBemDev
  > pip install numpy
  ```
- Clone the LiteBEM repo to your preferred location (e.g. "C:/code/")
  ```shell
  > cd C:/code/
  > git clone https://github.com/dav-og/LiteBEM.git
  ```
- Install LiteBEM as a developer!
  ```shell
  > cd LiteBEM
  > python setup.py build_ext
  > pip install -e .
  ```
- Be sure to check setup.py => install_requires = [...] to ensure that your environment has all required packages installed. You can check your environment's packages using:
  ```shell
  > conda list
  ```
  - If any packages are missing simply install them using:
    ```shell
    > pip install <package name>
    ```

## Run Tests

- Make sure `pytest` is installed in your working environment:
  ```shell
  (liteBemDev) > conda list
  ```
  - if its not installed then do:
    ```shell
    (liteBemDev) > pip install pytest
    ```

- Navigate to `LiteBEM` and run:
  ```shell
  (liteBemDev) > pytest tests/unit/preprocessor_unit_tests.py
  (liteBemDev) > pytest tests/unit/solver_unit_tests.py
  ```

## Tutorials

- For a tutorial on how to use LiteBEM, it is currently recommended that users utilize [Capytaine's documentation](https://ancell.in/capytaine/latest/user_manual/tutorial.html), as it remains largely consistent with LiteBEM
