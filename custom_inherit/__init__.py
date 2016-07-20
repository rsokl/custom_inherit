from .style_store import store, abc_store
from .style_store import *

__all__ = ["DocInheritorMeta", "styles"]
__version__ = "1.0.1"
styles = sorted(set(store.keys() + abc_store.keys()))


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

    this_store = store if not abstract_base_class else abc_store

    if style not in this_store:
        raise NotImplementedError("The available inheritance styles are: " + ", ".join(this_store))
    return this_store[style]
