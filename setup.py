#!/usr/bin/env python
# coding: utf-8

import os
from numpy.distutils.core import Extension
from setuptools import setup

########################
#  Fortran extensions  #
########################

# Delhommeau_source = [
#         "libDelhommeau/green_functions/Delhommeau_f90/constants.f90",
#         "libDelhommeau/green_functions/Delhommeau_f90/old_Prony_decomposition.f90",
#         "libDelhommeau/green_functions/Delhommeau_f90/Green_Rankine.f90",
#         "libDelhommeau/green_functions/Delhommeau_f90/Initialize_Green_wave.f90",
#         "libDelhommeau/green_functions/Delhommeau_f90/Green_wave.f90",
#         "libDelhommeau/green_functions/Delhommeau_f90/matrices.f90",
#     ]

# Delhommeau_extension = Extension(
#     name="libDelhommeau.green_functions.Delhommeau_f90",
#     sources=Delhommeau_source,
#     extra_compile_args=['-O2', '-fopenmp', '-cpp'],
#     extra_f90_compile_args=['-O2', '-fopenmp', '-cpp'],
#     extra_link_args=['-fopenmp'],
#     # Uncomment the following lines to get more verbose output from f2py.
#     define_macros=[
#         ('F2PY_REPORT_ATEXIT', 1),
#         ('F2PY_REPORT_ON_ARRAY_COPY', 1),
#     ],
# )

# XieDelhommeau_extension = Extension(
#     name="libDelhommeau.green_functions.XieDelhommeau_f90",
#     sources=Delhommeau_source,
#     extra_compile_args=['-O2', '-fopenmp', '-cpp', '-DXIE_CORRECTION'],
#     extra_f90_compile_args=['-O2', '-fopenmp', '-cpp', '-DXIE_CORRECTION'],
#     extra_link_args=['-fopenmp'],
#     # Uncomment the following lines to get more verbose output from f2py.
#     define_macros=[
#         ('F2PY_REPORT_ATEXIT', 1),
#         ('F2PY_REPORT_ON_ARRAY_COPY', 1),
#     ],
# )

# ########################################################
# #  Read version number and other info in __about__.py  #
# ########################################################

# base_dir = os.path.dirname(__file__)
# src_dir = os.path.join(base_dir, "capytaine")

# about = {}
# with open(os.path.join(src_dir, "__about__.py")) as f:
#     exec(f.read(), about)

##########
#  Main  #
##########

if __name__ == "__main__":
    setup(name = 'LiteBEM',
          version = '0.1',
          description = 'A lightweight BEM solver based on Matthieu Ancellin`s refactored Nemoh code (libDelhommeau)',
          author = 'David Ogden',
          license = 'Apache-2.0',
          url = 'https://github.com/dav-og/liteBEM',
          packages = ['litebem'] # 'libDelhommeau', 'libDelhommeau.green_functions'],
          # install_requires = ['numpy', 'scipy'], # 'pandas', 'xarray'
          # entry_points={
          #     'console_scripts': [
          #         'capytaine=capytaine.ui.cli:main',
          #     ],
          # },
          # ext_modules=[Delhommeau_extension, XieDelhommeau_extension],
          )
