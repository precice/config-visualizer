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
    install_requires = [
        'lxml',
        'pydot',
        'seaborn'
    ],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    scripts=[
        'bin/precice-config-visualizer'
    ],
)
