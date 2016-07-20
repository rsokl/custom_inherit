from distutils.core import setup
from setuptools import find_packages

setup(name='custom_inherit',
      version='1.0',
      description='A Python package that provides customized docstring inheritance\
       schemes between derived classes and their parents.',
      author='@meowklaski',
      url='https://www.python.org/sigs/distutils-sig/',
      packages=find_packages(),
      license="MIT"
      )
