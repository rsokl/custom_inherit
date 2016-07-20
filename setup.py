from distutils.core import setup
from setuptools import find_packages
import custom_inherit

setup(name='custom_inherit',
      version=custom_inherit.__version__,
      description='A Python package that provides customized docstring inheritance\
       schemes between derived classes and their parents.',
      author='@meowklaski',
      author_email="rsoklaski@gmail.com",
      url='https://github.com/meowklaski/custom_inherit/'+custom_inherit.__version__,
      packages=find_packages(),
      license="MIT"
      )
