from .style_store import store, abc_store
from .style_store import *

__all__ = ["DocInheritorMeta"]


def DocInheritMeta(style="parent", abstract_base_class=False):
    """ Returns the DocInheritor metaclass of the specified style.

        Parameters
        ----------
        style: str, optional (default: 'parent')
            A valid inheritance-scheme style.
        abstract_base_class: bool, optional(default: False)
            If True, the returned metaclass inherits from abc.ABCMeta
        Returns
        -------
        Union[custom_inherit.DocInheritorBase, custom.ABCDocInheritorBase]"""

    this_store = store if not abstract_base_class else abc_store

    if style not in this_store:
        raise NotImplementedError("The available inheritance styles are: " + ", ".join(this_store))
    return this_store[style]
