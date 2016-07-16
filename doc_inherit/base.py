"""http://stackoverflow.com/a/8101118/6592114"""

from abc import ABCMeta, abstractmethod, abstractstaticmethod
#
# def class_doc_inherit


class DocInheritorBase(type):
    def __new__(meta, name, bases, clsdict):

        clsdoc = clsdict.get("__doc__", None)

        prnt_cls_doc = None
        for mro_cls in (mro_cls for base in bases for mro_cls in base.mro()):
            prnt_cls_doc = mro_cls.__doc__
            if prnt_cls_doc is not None:
                break
        clsdict["__doc__"] = meta.class_doc_inherit(prnt_cls_doc, clsdoc)

        for attr, attribute in clsdict.items():

            if not(attr.startswith("__") and attr.endswith("__")):
                attr_doc = attribute.__doc__

                prnt_attr_doc = None
                for mro_cls in (mro_cls for base in bases for mro_cls in base.mro()
                                if hasattr(mro_cls, attr)):
                    prnt_attr_doc = getattr((getattr(mro_cls, attr), "__doc__"))
                    if prnt_attr_doc is not None:
                        break

                attribute.__doc__ = meta.attr_doc_inherit(prnt_attr_doc, attr_doc)

        return type.__new__(meta, name, bases, clsdict)

    @staticmethod
    @abstractmethod
    def class_doc_inherit(prnt_cls_doc, child_doc):
        raise NotImplementedError


    @staticmethod
    @abstractmethod
    def attr_doc_inherit(prnt_attr_doc, child_doc):
        raise NotImplementedError



class DocDoc(DocInheritorBase):

    @staticmethod
    def class_doc_inherit(prnt_cls_doc, child_doc):
        return "hi"


    @staticmethod
    def attr_doc_inherit(prnt_attr_doc, child_doc):
        return "attr"+child_doc
