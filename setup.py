from __future__ import absolute_import
from distutils.core import setup
from setuptools import find_packages
import custom_inherit

ver = custom_inherit.__version__
setup(
    name="custom_inherit",
    version=ver,
    description="A Python package that provides customized docstring inheritance\
       schemes between derived classes and their parents.",
    author="@rsokl",
    author_email="rsoklaski@gmail.com",
    url="https://github.com/rsokl/custom_inherit",
    download_url="https://github.com/rsokl/custom_inherit/tarball/" + ver,
    packages=find_packages(),
    license="MIT",
)
