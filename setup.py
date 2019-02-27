

try:
    from setuptools import setup, Extension
    setup, Extension
except ImportError:
    from distutils.core import setup
    from distutils.extension import Extension
    setup, Extension

import os
import re
import sys

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()

vre = re.compile("__version__ = \"(.*?)\"")
m = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "pyDbn.py")).read()
version = vre.findall(m)[0]


setup(
    name="pyDbn",
    version=version,
    description="Dynamic Bayesian Network",
    long_description=open("README.md").read(),
    author="Julius Hülsmann",
    author_email="huelsmann@campus.tu-berlin.de",
    url="https://github.com/juliusHuelsmann/pydbn",
    py_modules=["pyDbn"],
    package_data={"": ["LICENSE.rst"]},
    include_package_data=True,
    install_requires=[
        "numpy",
        "matplotlib",
        "daft"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GPLv2",
        "Operating System :: Linux",
        "Programming Language :: Python",
    ],
)
