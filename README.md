# custom_inherit

## Contents
 - [Overview](#overview)
 - [Basic Usage](#basic)

## Overview<a name="overview"\a>
The Python package custom_inherit provides the capability for a class to inherit docstrings from its parents in customizable ways. For instance, the built-in "numpy" inheritance style will merge [numpy-formatted docstrings](https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt#docstring-standard)
the sections of the parent's and child's docstrings in a nice way.   

## Basic Usage<a name="basic"\a>
The package provides users with a [metaclass](https://docs.python.org/3/reference/datamodel.html#customizing-class-creation), `DocInheritMeta()`, that, when used as a base metaclass in some parent class, will automatically handle all docstring inheritance for all subsequent derived classes - and their properties, methods, static methods, class methods, and decorated methods (**whew**).

The style of the inheritance scheme can be set explicitly when providing initializing `DocInheritMeta`. Here is a simple usage example using the "numpy" style of inheritance:
    ```python
       from abc import abstractmethod
       from custom_inherit import DocInheritMeta

       class Parent(metaclass=DocInheritMeta(style="numpy")) # Python 3 syntax
           # __metaclass__ = DocInheritMeta(style="numpy") # Python 2 syntax
           @abstracmethod
           def meth(self, x, y=None):
               """ Parameters
                   ----------
                   x: int
                      blah-x
                   y: Optional[int]

                   Raises
                   ------
                   NotImplementedError"""
                   raise NotImplementedError

        class Child(Parent):
            def meth(self, x, y=None):
                """ Method description

                    Returns
                    -------
                    int

                    Notes
                    -----
                    Some notes here."""
                return 0
    ```
Because we specified `style="numpy"` in `DocInheritMeta`, the inherited docstring of `Child.meth` will be:

      ```python
        """ Method description

            Parameters
            ----------
            x: int
               blah-x
            y: Optional[int]

            Returns
            -------
            int

            Notes
            -----
            Some notes here."""
      ```
