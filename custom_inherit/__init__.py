from __future__ import absolute_import
from types import FunctionType
from abc import ABCMeta
from .metaclass_base import DocInheritorBase
from .style_store import *

__all__ = ["DocInheritMeta", "store", "add_style", "remove_style"]
__version__ = "1.1.0"


def _construct_style_store():
    _store = {}
    for style_kind in style_store.__all__:
        _style = getattr(style_store, style_kind)
        if isinstance(_style, FunctionType):
            _store[style_kind] = _style
    return _store

store = _construct_style_store()


def add_style(func):
    """ Make available a new function for merging a 'parent' and 'child' docstring.

        Parameters
        ----------
        func: Callable[[Optional[str], Optional[str]], Optional[str]]

        Returns
        -------
        None"""
    assert isinstance(func, FunctionType), "`add_style` must be given a function"
    if func.__name__ not in store:
        store[func.__name__] = func
    else:
        print("The style name {} is already taken".format(func.__name__))
    return None


def remove_style(style):
    """ Remove the specified style from the style store.

        Parameters
        ----------
        style: Union[str, FunctionType]
            The style function, or its name, to be removed

        Returns
        -------
        None"""
    assert isinstance(style, (str, FunctionType)), "`remove_style` must be given a function or its name"

    if isinstance(style, FunctionType):
        style = style.__name__

    if style in store:
        store.pop(style)
    return None


def DocInheritMeta(style="parent", abstract_base_class=False):
    """ Returns the DocInheritor metaclass of the specified style.

        Parameters
        ----------
        style: Union[str, Callable[[str, str], str]], optional (default: 'parent')
            A valid inheritance-scheme style name or function.


        abstract_base_class: bool, optional(default: False)
            If True, the returned metaclass inherits from abc.ABCMeta.

            Thus a class that derives from DocInheritMeta(style="numpy", abstract_base_class=True)
            is an abstract base class, whose derived classes will inherit docstrings
            using the numpy-style inheritance scheme.


        Returns
        -------
        Union[custom_inherit.DocInheritorBase]"""

    if isinstance(style, FunctionType):
        merge_func = style

    else:
        if not store:
            raise NotImplementedError("There are no available inheritance styles")

        if style not in store:
            raise NotImplementedError("The available inheritance styles are: " + ", ".join(store))

        merge_func = store[style]

    metaclass = DocInheritorBase
    metaclass.class_doc_inherit = staticmethod(merge_func)
    metaclass.attr_doc_inherit = staticmethod(merge_func)

    return metaclass if not abstract_base_class else type("abc" + metaclass.__name__, (ABCMeta, metaclass), {})
