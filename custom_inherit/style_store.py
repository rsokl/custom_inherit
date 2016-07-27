from __future__ import absolute_import
from .doc_parse_tools import merge_numpy_docs

""" Docstring inheritance-style implementations.

    To implement your own inheritance file, simply write a function that fits the template:

            def your_style(prnt_doc, child_doc):
                ''' Merges parent and child docstrings

                    Parameters
                    ----------
                    prnt_cls_doc: Optional[str]
                    child_doc: Optional[str]

                    Returns
                    ------
                    Optional[str]
                        The merged docstring that will be utilized.'''
                return final_docstring

    and log this using `custom_inherit.add_style(your_style)`. To permanently save your function,
    define your function within custom_inherit/style_store.py, and log it in custom_inherit.style_store.__all__.
    Your style will then be available as 'your_style' (i.e. whatever you named the function).


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
                    "Yields" section instead. In this instance, the "Raises" section will not appear in the
                    inherited docstring.

                    Example:
                        parent-attribute's docstring:

                            ''' Parent's line

                                Parameters
                                ----------
                                x: int
                                    blah-x
                                y: Union[None, int]
                                    blah-y

                                Raises
                                -------
                                NotImplemented Error'''

                        docstring for corresponding attribute of child:

                            ''' Child's line

                                Returns
                                -------
                                int

                                Notes
                                -----
                                notes blah blah'''

                        docstring that is ultimately inherited by child's attribute:

                            ''' Child's line

                                Parameters
                                ----------
                                x: int
                                    blah-x
                                y: Union[None, int]
                                    blah-y

                                Returns
                                -------
                                int

                                Notes
                                -----
                                notes blah blah'''
"""

# All built-in styles must be logged in the __all__ field.
__all__ = ["parent", "numpy"]


def parent(prnt_doc, child_doc):
    return child_doc if child_doc is not None else prnt_doc


def numpy(prnt_doc, child_doc):
    return merge_numpy_docs(prnt_doc, child_doc)
