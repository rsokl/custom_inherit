# custom_inherit

## Contents
 - [Overview](#overview)
 - [Basic Usage](#basic)
 - [Advanced Usage](#advanced)
 - [Built-in Styles](#builtin)
 - [Making New inheritance Styles](#new)
 - [Installation & Getting Started](#install)
 - [Documentation](#doc)

## Overview<a name="overview"\a>
The Python package custom_inherit provides the capability for a class to inherit docstrings from its parents in customizable ways. For instance, the built-in "numpy" inheritance style will merge [numpy-formatted docstrings](https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt#docstring-standard)
sections of the parent's and child's respective docstrings in a nice way.

This package has been tested (and works) in both Python 2.7 and Python 3.5.  

## Basic Usage<a name="basic"\a>
custom_inherit exposes a  [metaclass](https://docs.python.org/3/reference/datamodel.html#customizing-class-creation), `DocInheritMeta()`, that, when used as inherited by some parent class, will automatically handle all docstring inheritance for all subsequent derived classes of that parent, and their properties, methods, static methods, class methods, and decorated methods (**whew**).

The style of the inheritance scheme can be set explicitly when passing `DocInheritMeta` its arguments. Here is a simple usage example using the "numpy" style of inheritance:

```python
   from custom_inherit import DocInheritMeta

   class Parent(metaclass=DocInheritMeta(style="numpy"))
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
A very natural, but more advanced use case for docstring inheritance is to define an [abstract base class](https://docs.python.org/3/library/abc.html#abc.ABCMeta) that has detailed docstrings for its abstract methods/properties. This class can be passed `DocInheritMeta(abstract_base_class=True)`, and it will have inherited from [abc.ABCMeta](https://docs.python.org/3/library/abc.html#abc.ABCMeta), plus all of its derived classes will inherit the docstrings for the methods/properties that they implement.

As shown in the example above, for the "numpy" inheritance style, one then only needs to specify the "Returns" or "Yields" section in the derived class' docstring for it to have a fully-detailed docstring.

## Built-in Styles<a name="builtin" \a>

The built-in styles are:

    - parent:   Wherever the docstring for a child-class' attribute (or for the class itself) is
                `None`, inherit the corresponding docstring from the parent.

                *NOTE* As of Python 3.5, this is the default behavior of the built-in function
                inspect.getdoc, and thus this style is deprecated Python 3.(>=5).

    - numpy:    The numpy-styled docstrings from the parent and child are merged gracefully
                with nice formatting.

                Specifically, any docstring section that appears in the parent's docstring that
                is not present in the child's is inherited. Otherwise, the child's docstring
                section is utilized. An exception to this is if the parent docstring contains a
                "Raises" section, but the child's attribute's docstring contains a "Returns" or
                "Yields" section instead. In this instance, the "Raises" section will not appear in the inherited docstring.

## Making New inheritance Styles<a name="new" \a>
Implementing your inheritance style is simple. In custom_inherit/style_store.py,
simply define a class that derives from `DocInheritorBase` (`ABCDocInheritorBase` for the abc-version), and implement the two static methods:

- ` class_doc_inherit(prnt_cls_doc, child_cls_doc)`

   - Merge the docstrings of a parent class and its child.

- `attr_doc_inherit(prnt_attr_doc, child_attr_doc)`

  - Merge the docstrings of method or property from parent class and the corresponding attribute of its child.

then register the style's name and the style in the dictionary `store` (`abc_store` for the abc version) in the same file. Then you are ready to use your style with `DocInheritMeta(style="whatever_you_named_it")`.

## Installation & Getting Started<a name="install" \a>
Install via pip:

```
    pip install custom_inherit`
```

or

Download/clone this repository, go to its directory, and install custom_inherit by typing in your command line:

```
    python setup.py install
```

If, instead, you want to install the package with links, so that edits you make to the code take
effect immediately within your installed version of custom_inherit, type:

```
    python setup.py develop
```

and then get started with

```python
   from custom_inherit import DocInheritMeta
```

## Documentation<a name="doc" \a>
```python
custom_inherit.DocInheritMeta(style="parent", abstract_base_class=False)
    """ Returns the DocInheritor metaclass of the specified style.

        Parameters
        ----------
        style: str, optional (default: 'parent')
            A valid inheritance-scheme style.
        abstract_base_class: bool, optional (default: False)
            If True, the returned metaclass inherits from abc.ABCMeta.

            Thus a class that derives from DocInheritMeta( abstract_base_class=True)

        Returns
        -------
        Union[custom_inherit.DocInheritorBase, custom.ABCDocInheritorBase]"""
```

### Go Back To:
 - [Overview](#overview)
 - [Basic Usage](#basic)
 - [Advanced Usage](#advanced)
 - [Built-in Styles](#builtin)
 - [Making New inheritance Styles](#new)
 - [Installation & Getting Started](#install)
 - [Documentation](#doc)
