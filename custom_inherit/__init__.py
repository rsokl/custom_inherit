from __future__ import absolute_import
from abc import ABCMeta
from .base import DocInheritorBase
from .style_store import *


__all__ = ["DocInheritMeta", "styles"]
__version__ = "1.1.0"

store = {}
for style_kind in style_store.__all__:
    style = getattr(style_store, style_kind)
    try:
        store[str(style.name)] = style
    except AttributeError:
        print("The style metaclass '{}' must have an attribute 'name'".format(style.__name__))
        pass

styles = sorted(store.keys())


def DocInheritMeta(style="parent", abstract_base_class=False):
    """ Returns the DocInheritor metaclass of the specified style.

        Parameters
        ----------
        style: str, optional (default: 'parent')
            A valid inheritance-scheme style.

            See custom_inherit.styles for a list of available styles.

        abstract_base_class: bool, optional(default: False)
            If True, the returned metaclass inherits from abc.ABCMeta.

            Thus a class that derives from DocInheritMeta(style="numpy", abstract_base_class=True)
            is an abstract base class, whose derived classes will inherit docstrings
            using the numpy-style inheritance scheme.


        Returns
        -------
        Union[custom_inherit.DocInheritorBase, custom.ABCDocInheritorBase]"""

    if style not in store:
        raise NotImplementedError("The available inheritance styles are: " + ", ".join(store))
    metaclass = store[style]
    return metaclass if not abstract_base_class else type("abc" + metaclass.__name__, (ABCMeta, metaclass), {})
