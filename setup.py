from __future__ import absolute_import
from distutils.core import setup
from setuptools import find_packages
import versioneer

setup(
    name="custom_inherit",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    package_dir={"": "src"},
    packages=find_packages(where="src", exclude=["tests", "tests.*"]),
    description="A Python package that provides customized docstring inheritance\
       schemes between derived classes and their parents.",
    author="@rsokl",
    author_email="rsoklaski@gmail.com",
    url="https://github.com/rsokl/custom_inherit",
    download_url="https://github.com/rsokl/custom_inherit/tarball/" + versioneer.get_version(),
    license="MIT",
)
