# custom_inherit

## Contents
 - [Overview](#overview)
 - [Basic Usage](#basic)
  - [Inheriting Docstrings Using a Metaclass](#meta)
  - [Inheriting Docstrings Using a Decorator](#dec)
 - [Advanced Usage](#advanced)
 - [Built-in Styles](#builtin)
 - [Making New inheritance Styles](#new)
 - [Installation & Getting Started](#install)
 - [Documentation](#doc)

## Overview<a name="overview"\a>
The Python package `custom_inherit` provides the capability for a class or a function (or method, property, ...) to inherit docstrings from a parents in customizable ways. For instance, the built-in "numpy" inheritance style will merge a parent's and child's respective docstrings in a nice way, based on their [numpy-style docstring sections](https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt#docstring-standard).

This package has been tested (and works) in both Python 2.7 and Python 3.5.

## Basic Usage<a name="basic"\a>
### Inheriting Docstrings Using a Metaclass<a name="meta"\a>
`custom_inherit` exposes a  [metaclass](https://docs.python.org/3/reference/datamodel.html#customizing-class-creation), `DocInheritMeta()`, that, when derived from by a class, will automatically mediate docstring inheritance for all subsequent derived classes of that parent, and their properties, methods, static methods, class methods, abstract methods, and decorated methods (**whew**).

The style of the inheritance scheme can be specified explicitly when passing `DocInheritMeta` its arguments. Here is a simple usage example using the built-in "numpy" style of inheritance:

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
 class implements a "Returns" section. Jump [ahead](#builtin) for a detailed description
 of the "numpy" style)

Keep in mind that the syntax for deriving from a meta class is slightly different in Python 2:

```python
   from custom_inherit import DocInheritMeta

   class Parent(object)
      __metaclass__ = metaclass=DocInheritMeta(style="numpy")
      ...
```

### Inheriting Docstrings Using a Decorator<a name="dec" \a>
`custom_inherit` also exposes a decorator capable of mediating docstring inheritance on an individual function (or property, method, etc.) level. In this example, we provide our own custom inheritance style-function on the fly (rather than using a built-in style):

```python
   from custom_inherit import doc_inherit

   def my_style(prnt_doc, child_doc): return "out-doc"

   def parent():
	   """ docstring to inherit from"""

   @doc_inherict(parent, style=my_style)
   def child():
       """ docstring to inherit into"""
```

Given the customized (although trivial) inheritance style specified in this example, the inherited docsting of `child`, in this instance, will be:

```python
   "out-doc"
```

## Advanced Usage<a name="advanced" \a>
A very natural, but more advanced use case for docstring inheritance is to define an [abstract base class](https://docs.python.org/3/library/abc.html#abc.ABCMeta) that has detailed docstrings for its abstract methods/properties. This class can be passed `DocInheritMeta(abstract_base_class=True)`, and it will have inherited from [abc.ABCMeta](https://docs.python.org/3/library/abc.html#abc.ABCMeta), plus all of its derived classes will inherit the docstrings for the methods/properties that they implement:

```python
   # Parent is now an abstract base class
   class Parent(metaclass=DocInheritMeta(style="numpy", abstract_base_class=True)):
      ...
```

As shown in the example above, for the "numpy" inheritance style, one then only needs to specify the "Returns" or "Yields" section in the derived class' docstring for it to have a fully-detailed docstring.

## Built-in Styles<a name="builtin" \a>

The built-in styles are:

    - parent:   Wherever the docstring for a child-class' attribute (or for the class itself) is
                `None`, inherit the corresponding docstring from the parent.

                *NOTE* As of Python 3.5, this is the default behavior of the built-in function
                inspect.getdoc, and thus this style is effectively deprecated Python 3.(>=5).

    - numpy:    The numpy-styled docstrings from the parent and child are merged gracefully
                with nice formatting.

                Specifically, any docstring section that appears in the parent's docstring that
                is not present in the child's is inherited. Otherwise, the child's docstring
                section is utilized. An exception to this is if the parent docstring contains a
                "Raises" section, but the child's attribute's docstring contains a "Returns" or
                "Yields" section instead. In this instance, the "Raises" section will not appear
				in the inherited docstring.

## Making New Inheritance Styles<a name="new" \a>
Implementing your inheritance style is simple. Wherever a style parameter is to be specified, one may supply a function of the form `func(prnt_doc: str, child_doc: str) -> str`, which merges the docstrings of the
parent with that of the child to produce an output string.

Alternatively, one may log the style in the dictionary `custom_inherit.store`. I.e. `custom_inherit.store["my_style"] = func` or `custom_inherit.add_style("my_style", func)`. Having done this, your logged function may now be referred to by name whever a style parameter is specified.

Lastly, one can add custom inheritance functions to `custom_inherit/style_store.py`. This will permanently log the custom inheritance function as a built-in style.

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
Documentation is available via `help(custom_inherit)`.

```python
custom_inherit.DocInheritMeta(style="parent", abstract_base_class=False)
    """ Returns the DocInheritor metaclass of the specified style.

        Parameters
        ----------
        style: Union[Any, Callable[[str, str], str]], optional (default: "parent")
            A valid inheritance-scheme style ID or function that merges two docstrings.

        abstract_base_class: bool, optional(default: False)
            If True, the returned metaclass inherits from abc.ABCMeta.

            Thus a class that derives from DocInheritMeta(style="numpy", abstract_base_class=True)
            will be an abstract base class, whose derived classes will inherit docstrings
            using the numpy-style inheritance scheme.


        Returns
        -------
        custom_inherit.DocInheritorBase"""


custom_inherit.doc_inherit(parent, style="parent"):
    """ Returns a function/method decorator that, given `parent`, updates the docstring of the decorated
        function/method based on the specified style and `parent`.

        Parameters
        ----------
        parent : Union[str, Any]
            The docstring, or object of which the docstring is utilized as the
            parent docstring during the docstring merge.

        style : Union[Any, Callable[[str, str], str]], optional (default: "parent")
            A valid inheritance-scheme style ID or function that merges two docstrings.

        Returns
        -------
        custom_inherit.DocInheritDecorator


        Notes
        -----
        `doc_inherit` should always be the inner-most decorator when being used in
        conjunction with other decorators, such as `@property`, `@staticmethod`, etc."""


custom_inherit.remove_style(style):
    """ Remove the specified style from the style store.

        Parameters
        ----------
        style: Any
            The inheritance-scheme style ID to be removed."""


custom_inherit.add_style(style_name, style_func):
    """ Make available a new function for merging a 'parent' and 'child' docstring.

        Parameters
        ----------
        style_name : Any
            The identifier of the style being logged
        style_func: Callable[[Optional[str], Optional[str]], Optional[str]]
            The style function that merges two docstrings into a single docstring."""
```

### Go Back To:
 - [Overview](#overview)
 - [Basic Usage](#basic)
 - [Advanced Usage](#advanced)
 - [Built-in Styles](#builtin)
 - [Making New inheritance Styles](#new)
 - [Installation & Getting Started](#install)
 - [Documentation](#doc)