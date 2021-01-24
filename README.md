# custom_inherit

[![Automated tests status](https://github.com/rsokl/custom_inherit/workflows/Tests/badge.svg)](https://github.com/rsokl/custom_inherit/actions?query=workflow%3ATests+branch%3Amaster)
[![PyPi version](https://img.shields.io/pypi/v/custom_inherit.svg)](https://pypi.python.org/pypi/custom_inherit)
 [![Conda Version](https://img.shields.io/conda/vn/conda-forge/custom-inherit.svg)](https://anaconda.org/conda-forge/custom-inherit)
[![Python version support](https://img.shields.io/badge/python-2.7,%20%20%203.4%20%20%20--%203.9-blue.svg)](https://img.shields.io/pypi/v/custom_inherit.svg)

## Contents
 - [Overview](#overview)
 - [Basic Usage](#basic-usage)
  - [Inheriting Docstrings Using a Metaclass](#inheriting-docstrings-using-a-metaclass)
  - [Inheriting Docstrings Using a Decorator](#inheriting-docstrings-using-a-decorator)
 - [Advanced Usage (ABCMeta)](#advanced-usage)
 - [Built-in Styles](#built-in-styles)
 - [Making New Inheritance Styles](#making-new-inheritance-styles)
 - [Installation & Getting Started](#installation-and-getting-started)
 - [Documentation](#documentation)

## Overview
The Python package `custom_inherit` provides convenient, light-weight tools for inheriting docstrings in customizeable ways.

### Features
- A metaclass that instructs children to inherit docstrings for their attributes from their parents, using custom docstring inheritance styles. This works for all varieties of methods (instance, static, class) and properties, including abstract ones.
- A decorator that merges a string/docstring with the docstring of the decorated object using custom styles. This can decorate functions as well as all varieties of class attributes.
- Built-in docstring merging styles for popular docstring specifications:
    - [NumPy docstring specification](https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt#docstring-standard)
    - [Napoleon docstring specifications](http://sphinxcontrib-napoleon.readthedocs.io/en/latest/index.html#id1) (for both [Google](http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html#example-google-style-python-docstrings) and [NumPy](http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_numpy.html#example-numpy) styles)
    - Merging based on [reST sections](http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html#sections)
    - Simple inheritance from a parent, if the docstring is not overwritten ([deprecated in Python 3.5](https://docs.python.org/3/library/inspect.html#inspect.getdoc))
- A simple interface for using your own docstring inheritance style.

### Implementation Notes
- These tools are compatible with [Sphinx](http://www.sphinx-doc.org/en/1.5.1/) - the inherited docstrings will be rendered by this package.
- These tools do not obfuscate function signatures or error traceback messages, nor do they affect performance beyond the initial construction process.
- No dependencies.

### Projects That Use `custom_inherit`
- [Toyplot](https://toyplot.readthedocs.io/en/stable/)
- [p2p-project](https://github.com/p2p-today/p2p-project)
- [Data Driven Discovery](https://gitlab.com/datadrivendiscovery)

## Basic Usage
### Inheriting Docstrings Using a Metaclass
`custom_inherit` exposes a  [metaclass](https://docs.python.org/3/reference/datamodel.html#customizing-class-creation), `DocInheritMeta()`, that, when derived from by a class, will automatically mediate docstring inheritance for all subsequent derived classes of that parent. Thus a child's attributes (methods, classmethods, staticmethods, properties, and their abstract counterparts) will inherit documentation from its parent's attribute, and the resulting docstring is synthesized according to a customizable style.

The style of the inheritance scheme can be specified explicitly when passing `DocInheritMeta` its arguments. Here is a simple usage example using the built-in "numpy" style of inheritance:

```python
from custom_inherit import DocInheritMeta

class Parent(metaclass=DocInheritMeta(style="numpy")):
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
(note the special case where the "Raises" section of the parent's method is left out, because the child
 class implements a "Returns" section instead. Jump [ahead](#builtin) for a detailed description
 of the "numpy" style)

Keep in mind that the syntax for deriving from a meta class is slightly different in Python 2:

```python
from custom_inherit import DocInheritMeta

class Parent(object):
   __metaclass__ = DocInheritMeta(style="numpy")
   ...
```

### Inheriting Docstrings Using a Decorator
`custom_inherit` also exposes a decorator capable of mediating docstring inheritance on an individual function (or property, method, etc.) level. In this example, we provide our own custom inheritance style-function on the fly (rather than using a built-in style):

```python
from custom_inherit import doc_inherit

def my_style(prnt_doc, child_doc): return "\n-----".join([prnt_doc, child_doc])

def parent():  # parent can be any object with a docstring, or simply a string itself
   """ docstring to inherit from"""

@doc_inherit(parent, style=my_style)
def child():
   """ docstring to inherit into"""
```

Given the customized (albeit stupid) inheritance style specified in this example, the inherited docsting of `child`, in this instance, will be:

```python
"""docstring to inherit from
  -----
  docstring to inherit into"""
```

## Advanced Usage
A very natural, but more advanced use case for docstring inheritance is to define an [abstract base class](https://docs.python.org/3/library/abc.html#abc.ABCMeta) that has detailed docstrings for its abstract methods/properties. This class can be passed `DocInheritMeta(abstract_base_class=True)`, and it will have inherited from [abc.ABCMeta](https://docs.python.org/3/library/abc.html#abc.ABCMeta), plus all of its derived classes will inherit the docstrings for the methods/properties that they implement:

```python
# Parent is now an abstract base class
class Parent(metaclass=DocInheritMeta(style="numpy", abstract_base_class=True)):
   ...
```

For the "numpy", "google", and "napoleon_numpy" inheritance styles, one then only needs to specify the "Returns" or "Yields" section in the derived class' attribute docstring for it to have a fully-detailed docstring.

Another option is to be able to decide whether to include all special methods, meaning methods that start and
end by "__" such as "__init__" method, or not in the doctstring inheritance process. Such an option can be pass
to the `DocInheritMeta` metaclass constructor:

```python
# Each child class will also merge the special methods' docstring of its parent class
class Parent(metaclass=DocInheritMeta(style="numpy", include_special_methods=True)):
   ...
```

Special methods are not included by default.

## Built-in Styles

Utilize a built-in style by specifying any of the following names (as a string), wherever the `style` parameter is to be specified. The built-in styles are:

- `"parent"`: Wherever the docstring for a child-class' attribute (or for the class itself) is
	`None`, inherit the corresponding docstring from the parent. (Deprecated in Python 3.5)

- `"numpy"`: [NumPy-styled docstrings](https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt#docstring-standard)
        from the parent and child are merged gracefully with nice formatting. The child's docstring sections take precedence
	in the case of overlap.

- `"numpy_with_merge"`: Behaves identically to the "numpy" style, but also merges sections that overlap,
    instead of only keeping the child's section. All sections are concerned except sections "Short Summary",
    "Extended Summary", "Deprecation Warning" and "Examples" for which the "numpy" style behaviour applies.

- `"google"`: Google-styled docstrings from the parent and child are merged gracefully
	with nice formatting. The child's docstring sections take precedence in the case of overlap.
	This adheres to the [napoleon specification for the Google style](http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html#example-google-style-python-docstrings).

- `"google_with_merge"`: Behaves identically to the "google" style, but also merges sections that overlap,
    instead of only keeping the child's section. All sections are concerned except sections "Short Summary",
    "Example" and "Examples" (or coresponding aliases) for which the 'google' style applies.

- `"numpy_napoleon"`: NumPy-styled docstrings from the parent and child are merged gracefully
	with nice formatting. The child's docstring sections take precedence in the case of overlap.
	This adheres to the [napoleon specification for the NumPy style](http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_numpy.html#example-numpy).

- `"numpy_napoleon_with_merge"`: Behaves identically to the 'numpy_napoleon' style, but also merges sections
    that overlap, instead of only keeping the child's section. All sections are concerned except sections
    "Short Summary", "Example" and "Examples" (or coresponding aliases) for which the 'numpy_napoleon' style
    behaviour applies.

- `"reST"`: reST-styled docstrings from the parent and child are merged gracefully
	with nice formatting. Docstring sections are specified by
	[reST section titles](http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html#sections).
	The child's docstring sections take precedence in the case of overlap.

For the `numpy`, `numpy_with_merge`, `numpy_napoleon`, `numpy_napoleon_with_merge`, `google` and `google_with_merge` styles, if the parent's docstring contains a "Raises" section and the child's docstring implements a "Returns" or a "Yields" section instead, then the "Raises" section is not included in the resulting docstring. This is to accomodate for the relatively common use case in which an abstract method/property raises `NotImplementedError`. Child classes that implement this method/property clearly will not raise this. Of course, any "Raises" section that is explicitly included in the child's docstring will appear in the resulting docstring.

Detailed documentation and example cases for the default styles can be found [here](https://github.com/meowklaski/custom_inherit/blob/master/custom_inherit/_style_store.py)

## Making New Inheritance Styles
Implementing your inheritance style is simple.

- Provide an inheritance style on the fly wherever a style parameter is specified:
    - Supply any function of the form: `func(prnt_doc: str, child_doc: str) -> str`

- Log an inheritance style, and refer to it by name wherever a style parameter is specified, using either:
    - `custom_inherit.store["my_style"] = func`
    - `custom_inherit.add_style("my_style", func)`.

## Installation and Getting Started
Install via pip:

```
    pip install custom_inherit
```
Install via conda:

```
    conda install -c conda-forge custom-inherit
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
from custom_inherit import DocInheritMeta, doc_inherit, store
# print(store) shows you the available styles
```

## Documentation
Documentation is available via `help(custom_inherit)`.

```python
custom_inherit.DocInheritMeta(style="parent", abstract_base_class=False):
    """ A metaclass that merges the respective docstrings of a parent class and of its child, along with their
        properties, methods (including classmethod, staticmethod, decorated methods).

        Parameters
        ----------
        style: Union[Hashable, Callable[[str, str], str]], optional (default: "parent")
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
        function/method based on the specified style and the corresponding attribute of `parent`.

        Parameters
        ----------
        parent : Union[str, Any]
            The object whose docstring, is utilized as the parent docstring
	    during the docstring merge. Or, a string can be provided directly.

        style : Union[Hashable, Callable[[str, str], str]], optional (default: "parent")
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
        style: Hashable
            The inheritance-scheme style ID to be removed."""


custom_inherit.add_style(style_name, style_func):
    """ Make available a new function for merging a 'parent' and 'child' docstring.

        Parameters
        ----------
        style_name : Hashable
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
