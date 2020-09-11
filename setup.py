import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name = "precice-config-visualizer",
    version = "0.1.0",
    author = "The preCICE Developers",
    author_email = "info@precice.org",
    description = "A tool for visualizing a preCICE configuration file as a dot file.",
    license = "GPLv3",
    #url = "http://packages.python.org/an_example_pypi_project",
    packages=[],
    long_description=read('README.md'),
    python_requires=">=3.6",
    install_requires = [
        'lxml',
        'pydot',
    ],
    classifiers = [
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Utilities",
    ],
    scripts=[
        'bin/precice-config-visualizer'
    ],
)
