# LiteBEM
A lightweight, Apache 2.0 distribution of Matthieu Ancellin's Capytaine BEM code.

## Requirements
  - Conda is recommended for managing your Python distribution, dependencies and environment:
    - https://docs.conda.io/en/latest/miniconda.html 
    - current development efforts are based on Python 3.9
  - Microsoft Visual Studio is required for linking the fortran binaries
    - https://visualstudio.microsoft.com/downloads/
    - during installation check the box to include **"Desktop development with C++"**
  - Intel oneAPI HPC toolkit is required for compiling the fortran binaries (you do not need the base kit)
    - https://www.intel.com/content/www/us/en/developer/tools/oneapi/hpc-toolkit-download.html
    - install to the default file location
  - create **"LIB"** environment variable to point towards the intel directory for compiler ".lib" files
    - if oneAPI is installed to the default location, assign the LIB user variable a value of: "C:\Program Files (x86)\Intel\oneAPI\compiler\2022.1.0\windows\compiler\lib\intel64_win"
    - if oneAPI is installed to a different location then adjust the path above as necessary

## Installation for Users
Recommended approach:

- Open the anaconda powershell and create a new environment for the LiteBEM project (e.g. "liteBemProject")
  ```shell
  > conda create --name liteBemProject python
  ```
- Install LiteBEM from PyPI by entering the following command within your new environment
-   ```shell
    > conda activate liteBemProject
    > python -m pip install litebem
    ```

## Installation for Developers
Recommended approach:

- Open the anaconda powershell and create a new environment for LiteBEM-related development (e.g. "liteBemDev")
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
