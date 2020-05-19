from __future__ import absolute_import as _absolute_import

from abc import ABCMeta as _ABCMeta

from ._decorator_base import DocInheritDecorator as _DocInheritDecorator
from ._metaclass_base import DocInheritorBase as _DocInheritorBase
from . import _style_store
from ._style_store import (
    google, numpy, numpy_napoleon, parent, reST,
    google_with_merge, numpy_napoleon_with_merge, numpy_with_merge
)
from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions

try:
    _basestring = basestring
except NameError:
    _basestring = str  # Python 2 -> 3 alias


__all__ = ["DocInheritMeta", "doc_inherit", "store", "add_style", "remove_style"]


def _check_style_function(style_func):
    out = style_func("", "")
    if not isinstance(out, _basestring) and out is not None:
        raise TypeError
    return None


class _Store(object):
    """ A dictionary-like object that stores the styles available for the doc-inheritance metaclass and decorator,
   respectively.

   Only callable objects with the signature: f(Optional[str], Optional[str]) -> Optional[str]
   can be stored. If f is a valid callable, then _Store()[f] -> f."""

    def __init__(self, *args, **kwargs):
        self._store = dict()
        self.update(*args, **kwargs)

    def __repr__(self):
        return repr(self._store)

    def __str__(self):
        out_str = "The available stored styles are: "
        styles = "\n".join("\t- " + style for style in sorted(self.keys()))
        return "\n".join((out_str, styles))

    def __setitem__(self, style_name, style_func):
        """ Make available a new function for merging a 'parent' and 'child' docstring.

        Parameters
        ----------
        style_name : Any
            The identifier of the style being logged
        style_func: Callable[[Optional[str], Optional[str]], Optional[str]]
            The style function that merges two docstrings into a single docstring."""
        try:
            _check_style_function(style_func)
        except TypeError:
            raise TypeError(
                "The style store only stores callables of the form: "
                "\n\tstyle_func(Optional[str], Optional[str]) -> Optional[str]"
            )
        self._store[style_name] = style_func

    def __getitem__(self, item):
        """ Given a valid style-ID, retrieve a stored style. If a valid function (callable) is
        supplied, return it in place.

        Parameters
        ----------
        item : Union[Any, Callable[Optional[str], Optional[str]], Optional[str]]
            A valid style-ID or style-function."""
        try:
            return self._store[item]
        except KeyError:
            try:
                _check_style_function(item)
                return item
            except (TypeError, ValueError):
                raise TypeError(
                    "Either a valid style name or style-function must be specified"
                )

    def keys(self):
        """  D.keys() -> a set-like object providing a view on D's keys"""
        return self._store.keys()

    def pop(self, *args):
        """ D.pop(k[,d]) -> v, remove specified key and return the corresponding value.
        If key is not found, d is returned if given, otherwise KeyError is raised. """
        if len(args) < 3:
            return self._store.pop(*args)
        else:
            raise TypeError(
                "pop expected at most 2 arguments, got {}".format(len(args))
            )

    def update(self, *args, **kwargs):
        """ D.update([E, ]**F) -> None.  Update D from dict/iterable E and F.
        If E is present and has a .keys() method, then does:  for k in E: D[k] = E[k]"""
        if len(args) > 1:
            raise TypeError("update expected at most 1 arguments, got %d" % len(args))

        for key, value in dict(*args, **kwargs).items():
            self[key] = value

    def values(self):
        """ D.values() -> an object providing a view on D's values."""
        return self._store.values()

    def items(self):
        """ D.items() -> a set-like object providing a view on D's items"""
        return self._store.items()

store = _Store([(key, getattr(_style_store, key)) for key in _style_store.__all__])


def add_style(style_name, style_func):
    """ Make available a new function for merging a 'parent' and 'child' docstring.

    Parameters
    ----------
    style_name : Any
        The identifier of the style being logged
    style_func: Callable[[Optional[str], Optional[str]], Optional[str]]
        The style function that merges two docstrings into a single docstring."""
    store[style_name] = style_func


def remove_style(style):
    """ Remove the specified style from the style store.

    Parameters
    ----------
    style: Any
        The inheritance-scheme style ID to be removed."""
    if style in store:
        store.pop(style)


def DocInheritMeta(style="parent", abstract_base_class=False, include_special_methods=False):
    """ A metaclass that merges the respective docstrings of a parent class and of its child, along with their
    properties, methods (including classmethod, staticmethod, decorated methods).

    Parameters
    ----------
    style: Union[Any, Callable[[str, str], str]], optional (default: "parent")
        A valid inheritance-scheme style ID or function that merges two docstrings.

    abstract_base_class: bool, optional(default: False)
        If True, the returned metaclass inherits from abc.ABCMeta.

        Thus a class that derives from DocInheritMeta(style="numpy", abstract_base_class=True)
        will be an abstract base class, whose derived classes will inherit docstrings
        using the numpy-style inheritance scheme.

    include_special_methods: bool, optional (defaul: False)
        Wether special methods of class (i.e. starting en ending with "__") are included in the docstring
        inheritance process.


    Returns
    -------
    custom_inherit.DocInheritorBase"""

    merge_func = store[style]
    metaclass = _DocInheritorBase
    metaclass.include_special_methods = include_special_methods
    metaclass.class_doc_inherit = staticmethod(merge_func)
    metaclass.attr_doc_inherit = staticmethod(merge_func)

    return (
        metaclass
        if not abstract_base_class
        else type("abc" + metaclass.__name__, (_ABCMeta, metaclass), {})
    )


def doc_inherit(parent, style="parent"):
    """ Returns a function/method decorator that, given `parent`, updates the docstring of the decorated
    function/method based on the specified style and the corresponding attribute of `parent`.

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
    `doc_inherit` should always be used as the inner-most decorator when being used in
    conjunction with other decorators, such as `@property`, `@staticmethod`, etc."""

    merge_func = store[style]
    decorator = _DocInheritDecorator
    decorator.doc_merger = staticmethod(merge_func)
    return decorator(parent)
