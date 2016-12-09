from __future__ import absolute_import
from abc import ABCMeta
from .metaclass_base import DocInheritorBase
from .style_store import *
from .decorator_base import DocInheritDecorator
from .style_store import __all__ as all_styles

try:
    basestring
except NameError:
    basestring = str  # Python 2 -> 3 alias


__all__ = ["DocInheritMeta", "doc_inherit", "store", "add_style", "remove_style"]
__version__ = "2.0.1"


def _check_style_function(style_func):
    out = style_func("", "")
    if not (isinstance(out, basestring) or out is None):
        raise TypeError
    return None


class _Store(dict):
    """ A dictionary that stores the styles available for the doc-inheritance metaclass and decorator,
       respectively."""

    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

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
            raise TypeError("The style store only stores callables (callables) of the form: "
                            "\n\tstyle_func(Optional[str], Optional[str]) -> Optional[str]")
        super(_Store, self).__setitem__(style_name, style_func)

    def __getitem__(self, item):
        """ Given a valid style-ID, retrieve a stored style. If a valid function (callable) is
            supplied, return it in place.

            Parameters
            ----------
            item : Union[Any, Callable[Optional[str], Optional[str]], Optional[str]]
                A valid style-ID or style-function."""
        try:
            return super(_Store, self).__getitem__(item)
        except KeyError:
            try:
                _check_style_function(item)
                return item
            except TypeError:
                raise TypeError("Either a valid style name or style-function must be specified")

    def update(self, *args, **kwargs):
        if len(args) > 1:
            raise TypeError("update expected at most 1 arguments, got %d" % len(args))

        for key, value in dict(*args, **kwargs).items():
            self[key] = value

    def setdefault(self, key, value=None):
        if key not in self:
            self[key] = value
        return self[key]

store = _Store([(key, getattr(style_store, key)) for key in style_store.__all__])


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


def DocInheritMeta(style="parent", abstract_base_class=False):
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

    merge_func = store[style]
    metaclass = DocInheritorBase
    metaclass.class_doc_inherit = staticmethod(merge_func)
    metaclass.attr_doc_inherit = staticmethod(merge_func)

    return metaclass if not abstract_base_class else type("abc" + metaclass.__name__, (ABCMeta, metaclass), {})


def doc_inherit(parent, style="parent"):
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
        `doc_inherit` should always be used as the inner-most decorator when being used in
        conjunction with other decorators, such as `@property`, `@staticmethod`, etc."""

    merge_func = store[style]
    decorator = DocInheritDecorator
    decorator.doc_merger = staticmethod(merge_func)
    return decorator(parent)
