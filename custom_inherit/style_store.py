from __future__ import absolute_import
from .base import DocInheritorBase, ABCDocInheritorBase
from .doc_parse_tools import merge_numpy_docs

""" Docstring inheritance-style implementations.

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


__all__ = ["InheritParent", "MergeNumpy"]


def _f(prnt_doc, child_doc):
    return child_doc if child_doc is not None else prnt_doc


# --------------------------
# Meta class styles
# --------------------------

class InheritParent(DocInheritorBase):
    name = "parent"

    @staticmethod
    def class_doc_inherit(prnt_cls_doc, child_cls_doc):
        """ Parameters
            ----------
            prnt_cls_doc: Union[None, str]
            child_cls_doc: : Union[None, str]

            Returns
            -------
            Union[None, str]"""
        return _f(prnt_cls_doc, child_cls_doc)

    @staticmethod
    def attr_doc_inherit(prnt_attr_doc, child_attr_doc):
        """ Parameters
            ----------
            prnt_cls_doc: Union[None, str]
            child_cls_doc: : Union[None, str]

            Returns
            -------
            Union[None, str]"""
        return _f(prnt_attr_doc, child_attr_doc)


class MergeNumpy(DocInheritorBase):
    name = "numpy"

    @staticmethod
    def class_doc_inherit(prnt_cls_doc, child_cls_doc):
        """ Parameters
            ----------
            prnt_cls_doc: Union[None, str]
            child_cls_doc: : Union[None, str]

            Returns
            -------
            Union[None, str]"""
        return merge_numpy_docs(prnt_cls_doc, child_cls_doc)

    @staticmethod
    def attr_doc_inherit(prnt_attr_doc, child_attr_doc):
        """ Parameters
            ----------
            prnt_cls_doc: Union[None, str]
            child_cls_doc: : Union[None, str]

            Returns
            -------
            Union[None, str]"""
        return merge_numpy_docs(prnt_attr_doc, child_attr_doc)

store = {InheritParent.name: InheritParent,
         MergeNumpy.name: MergeNumpy}



# --------------------------
# Abstract base meta class styles
# --------------------------


class ABCInheritParent(ABCDocInheritorBase):
    name = "parent"

    @staticmethod
    def class_doc_inherit(prnt_cls_doc, child_cls_doc):
        """ Parameters
            ----------
            prnt_cls_doc: Union[None, str]
            child_cls_doc: : Union[None, str]

            Returns
            -------
            Union[None, str]"""
        return _f(prnt_cls_doc, child_cls_doc)

    @staticmethod
    def attr_doc_inherit(prnt_attr_doc, child_attr_doc):
        """ Parameters
            ----------
            prnt_cls_doc: Union[None, str]
            child_cls_doc: : Union[None, str]

            Returns
            -------
            Union[None, str]"""
        return _f(prnt_attr_doc, child_attr_doc)


class ABCMergeNumpy(ABCDocInheritorBase):
    name = "numpy"

    @staticmethod
    def class_doc_inherit(prnt_cls_doc, child_cls_doc):
        """ Parameters
            ----------
            prnt_cls_doc: Union[None, str]
            child_cls_doc: : Union[None, str]

            Returns
            -------
            Union[None, str]"""
        return merge_numpy_docs(prnt_cls_doc, child_cls_doc)

    @staticmethod
    def attr_doc_inherit(prnt_attr_doc, child_attr_doc):
        """ Parameters
            ----------
            prnt_cls_doc: Union[None, str]
            child_cls_doc: : Union[None, str]

            Returns
            -------
            Union[None, str]"""
        return merge_numpy_docs(prnt_attr_doc, child_attr_doc)

abc_store = {ABCInheritParent.name: ABCInheritParent,
             ABCMergeNumpy.name: ABCMergeNumpy}