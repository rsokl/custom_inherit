from .base import DocInheritorBase, ABCDocInheritorBase
from .doc_parse_tools import merge_numpy_docs

""" Docstring inheritance-style implementations.

    The built-in styles are:
        - numpy: The numpy-styled docstrings of the parent and child are merged gracefully.

            Specifically, any docstring section that appears in the parent's docstring that
            is not present in the child's is inherited. Otherwise, the child's docstring
            section is utilized. An exception to this is if the parent docstring contains a
            "Raises" section, but the child's attribute's docstring contains a "Returns" or
            "Yields" section. In this instance, the "Raises" section will not appear in the
            inherited docstring.

            Example:
                parent-attribute's method:
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
        return _f(prnt_cls_doc, child_cls_doc)

    @staticmethod
    def attr_doc_inherit(prnt_attr_doc, child_attr_doc):
        return _f(prnt_attr_doc, child_attr_doc)


class MergeNumpy(DocInheritorBase):
    name = "numpy"

    @staticmethod
    def class_doc_inherit(prnt_cls_doc, child_cls_doc):
        return merge_numpy_docs(prnt_cls_doc, child_cls_doc)

    @staticmethod
    def attr_doc_inherit(prnt_attr_doc, child_attr_doc):
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
        return _f(prnt_cls_doc, child_cls_doc)

    @staticmethod
    def attr_doc_inherit(prnt_attr_doc, child_attr_doc):
        return _f(prnt_attr_doc, child_attr_doc)


class ABCMergeNumpy(ABCDocInheritorBase):
    name = "numpy"

    @staticmethod
    def class_doc_inherit(prnt_cls_doc, child_cls_doc):
        return merge_numpy_docs(prnt_cls_doc, child_cls_doc)

    @staticmethod
    def attr_doc_inherit(prnt_attr_doc, child_attr_doc):
        return merge_numpy_docs(prnt_attr_doc, child_attr_doc)

abc_store = {ABCInheritParent.name: ABCInheritParent,
             ABCMergeNumpy.name: ABCMergeNumpy}