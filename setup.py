import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'LiteBEM',
    version="0.0.1",
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
        "Operating System :: POSIX :: Linux",
        "Topic :: Scientific/Engineering"
    ],
    package_dir={"": "litebem"},
    packages=setuptools.find_packages(where="litebem"),
    python_requires=">=3.0",
)