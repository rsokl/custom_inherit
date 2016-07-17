from .base import DocInheritorBase
from .doc_parse_tools import merge_numpy_docs

def f(prnt_doc, child_doc):
    return child_doc if child_doc is not None else prnt_doc


class InheritParent(DocInheritorBase):
    name = "parent"

    @staticmethod
    def class_doc_inherit(prnt_cls_doc, child_cls_doc):
        return f(prnt_cls_doc, child_cls_doc)

    @staticmethod
    def attr_doc_inherit(prnt_attr_doc, child_attr_doc):
        return f(prnt_attr_doc, child_attr_doc)


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