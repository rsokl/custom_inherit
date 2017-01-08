from __future__ import absolute_import
from ._doc_parse_tools import merge_numpy_docs, merge_rest_docs

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
    define your function within custom_inherit/_style_store.py, and log it in custom_inherit.style_store.__all__.
    Your style will then be available as 'your_style' (i.e. whatever you named the function).
"""

# All built-in styles must be logged in the __all__ field.
__all__ = ["parent", "numpy", "reST"]


def parent(prnt_doc, child_doc):
    """ Wherever the docstring for a child-class' attribute (or for the class itself) is
        `None`, inherit the corresponding docstring from the parent.

        *NOTE* As of Python 3.5, this is the default behavior of the built-in function
        inspect.getdoc, and thus this style is deprecated Python 3.(>=5). """
    return child_doc if child_doc is not None else prnt_doc


def numpy(prnt_doc, child_doc):
    """ The numpy-styled docstrings from the parent and child are merged gracefully
        with nice formatting.

        Specifically, any docstring section that appears in the parent's docstring that
        is not present in the child's is inherited. Otherwise, the child's docstring
        section is utilized. An exception to this is if the parent docstring contains a
        "Raises" section, but the child's attribute's docstring contains a "Returns" or
        "Yields" section instead. In this instance, the "Raises" section will not appear in the
        inherited docstring.

        Any whitespace that can be uniformly removed from a docstring's second line and onwards is
        removed. Sections in the resulting docstring will be separated by a single blank line.

        For details on the numpy docstring style, see:
        https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt

        Example:
            - parent's docstring:

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

            - child's docstring:

                ''' Child's line

                    Returns
                    -------
                    int

                    Notes
                    -----
                    notes blah blah'''

            - docstring that is ultimately inherited:

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
                    notes blah blah'''"""
    return merge_numpy_docs(prnt_doc, child_doc)


def reST(prnt_doc, child_doc):
    """ Merge two reST-style docstrings into a single docstring.

        Given the reST-style docstrings from a parent and child's attributes, merge the docstring
        sections such that the child's section is used, wherever present, otherwise the parent's
        section is used.

        Sections are delimited by any type of section title. For more details, see:
        http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html#sections

        Any whitespace that can be uniformly removed from a docstring's second line and onwards is
        removed. Sections in the resulting docstring will be separated by a single blank line.

        Any whitespace that can be uniformly removed from a docstring's second line and onwards is
        removed. Sections will be separated by a single blank line.

        Example:
          parent - ''' Header1
                       -------
                       parent's content for Header 1
                           - indented material
                       Header2
                       ~~~~~~~
                       content for Header2'''

          child -  ''' Front-matter
                       ~~~~~~~~~
                       NewHeader
                       ~~~~~~~~~
                       content for NewHeader

                       Header2
                       +++++++
                       child's content for Header2'''

          merged - ''' Front-matter

                       Header1
                       -------
                       content for Header 1
                           - indented material

                       Header2
                       +++++++
                       child's content for Header2

                       ~~~~~~~~~
                       NewHeader
                       ~~~~~~~~~
                       content for NewHeader '''
            """
    return merge_rest_docs(prnt_doc, child_doc)