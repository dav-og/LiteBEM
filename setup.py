from os import name
import setuptools
from numpy.distutils.core import setup, Extension

delhommeauSources = ["src/litebem/solver/green_functions/delhommeau_f90/constants.f90",
                     "src/litebem/solver/green_functions/delhommeau_f90/old_Prony_decomposition.f90",
                     "src/litebem/solver/green_functions/delhommeau_f90/Green_Rankine.f90",
                     "src/litebem/solver/green_functions/delhommeau_f90/Initialize_Green_wave.f90",
                     "src/litebem/solver/green_functions/delhommeau_f90/Green_wave.f90",
                     "src/litebem/solver/green_functions/delhommeau_f90/matrices.f90"]

delhommeauExtension = Extension(name="litebem.solver.green_functions.delhommeau_f90",
                                sources=delhommeauSources,
                                extra_f90_compile_args=['-fpp'])

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name = 'litebem',
    version="1.0.2",
    author = 'mancellin, dav-og, dunc-lamb',
    license = 'Apache-2.0',
    description = 'A lightweight, Apache 2.0 distribution of Matthieu Ancellin`s Capytaine BEM code.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url = 'https://github.com/dav-og/liteBEM',
    install_requires = ['pytest', 'numpy', 'scipy', 'pandas', 'xarray'],
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering"
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    ext_modules=[delhommeauExtension],
    python_requires=">=3.0",
)