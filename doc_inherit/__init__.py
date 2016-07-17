from .style_store import store
from  .style_store import *

__all__ = ["DocInheritor"]


def DocInheritor(style="parent"):
    if style not in store:
        raise NotImplementedError("The available inheritance styles are: " + ", ".join(store))
    return store[style]