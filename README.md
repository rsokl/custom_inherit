# custom_inherit

## Contents
 - [Overview](#overview)
 - [Basic Usage](#basic)
 - [Advanced Usage](#advanced)

## Overview<a name="overview"\a>
The Python package custom_inherit provides the capability for a class to inherit docstrings from its parents in customizable ways. For instance, the built-in "numpy" inheritance style will merge [numpy-formatted docstrings](https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt#docstring-standard)
sections of the parent's and child's respective docstrings in a nice way.   

## Basic Usage<a name="basic"\a>
custom_inherit exposes a  [metaclass](https://docs.python.org/3/reference/datamodel.html#customizing-class-creation), `DocInheritMeta()`, that, when used as a base metaclass in some parent class, will automatically handle all docstring inheritance for all subsequent derived classes - and their properties, methods, static methods, class methods, and decorated methods (**whew**).

The style of the inheritance scheme can be set explicitly when providing initializing `DocInheritMeta`. Here is a simple usage example using the "numpy" style of inheritance:

```python
   from abc import abstractmethod
   from custom_inherit import DocInheritMeta

   class Parent(metaclass=DocInheritMeta(style="numpy")) # Python 3 syntax for meta class inheritance
       def meth(self, x, y=None):
           """ Parameters
               ----------
               x: int
                  blah-x
               y: Optional[int]
                  blah-y
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
         blah-y

      Returns
      -------
      int

      Notes
      -----
      Some notes here."""
```
(note that the "Raises" section of the parent's method is left out, because the child
 class implements a "Returns" section)

## Advanced Usage<a name="advanced" \a>
A very natural, but more advanced use case for docstring inheritance is to define an [abstract base class](https://docs.python.org/3/library/abc.html#abc.ABCMeta) that has detailed docstrings for its abstract methods/properties. This class can inherit from `DocInheritMeta(abstract_base_class=True)`, and it will both have inherited from [abc.ABCMeta]([abstract base class](https://docs.python.org/3/library/abc.html#abc.ABCMeta), and all of its derived classes will inherit the docstrings for the methods/properties that they implement. As shown in the example above, for the "numpy" inheritance style, one then only needs to specify the "Returns" or "Yields" section in the derived class' docstring for it to have a fully-detailed docstring.
