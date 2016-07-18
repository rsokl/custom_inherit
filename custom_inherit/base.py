"""http://stackoverflow.com/a/8101118/6592114"""
from abc import abstractmethod, ABCMeta
import sys
__all__ = ["DocInheritorBase"]

if sys.version_info >= (3,0):
    class DocInheritorBase(type):
        def __new__(mcs, class_name, class_bases, class_dict):
            clsdoc = class_dict.get("__doc__", None)

            prnt_cls_doc = None
            for mro_cls in (mro_cls for base in class_bases for mro_cls in base.mro()):
                prnt_cls_doc = mro_cls.__doc__
                if prnt_cls_doc is not None:
                    if prnt_cls_doc == "The most base type":
                        prnt_cls_doc = None
                    break

            class_dict["__doc__"] = mcs.class_doc_inherit(prnt_cls_doc, clsdoc)

            for attr, attribute in class_dict.items():
                if not(attr.startswith("__") and attr.endswith("__")):
                    if isinstance(attribute, (staticmethod, classmethod)):
                        attr_doc = attribute.__func__.__doc__
                    else:
                        attr_doc = attribute.__doc__

                    prnt_attr_doc = None
                    for mro_cls in (mro_cls for base in class_bases for mro_cls in base.mro()
                                    if hasattr(mro_cls, attr)):
                        prnt_attr_doc = getattr(getattr(mro_cls, attr), "__doc__")
                        if prnt_attr_doc is not None:
                            break

                    if isinstance(attribute, (staticmethod, classmethod)):
                        attribute.__func__.__doc__ =  mcs.attr_doc_inherit(prnt_attr_doc, attr_doc)
                    else:
                        attribute.__doc__ = mcs.attr_doc_inherit(prnt_attr_doc, attr_doc)

            return type.__new__(mcs, class_name, class_bases, class_dict)

        @staticmethod
        @abstractmethod
        def class_doc_inherit(prnt_cls_doc, child_doc):
            raise NotImplementedError

        @staticmethod
        @abstractmethod
        def attr_doc_inherit(prnt_attr_doc, child_doc):
            raise NotImplementedError


    ABCDocInheritorBase = type("ABCDocInheritorBase", (ABCMeta, DocInheritorBase), {})



else:
    class DocInheritorBase(type):
        def __new__(mcs, class_name, class_bases, class_dict):
            clsdoc = class_dict.get("__doc__", None)

            prnt_cls_doc = None
            for mro_cls in (mro_cls for base in class_bases for mro_cls in base.mro()):
                prnt_cls_doc = mro_cls.__doc__
                if prnt_cls_doc is not None:
                    break

            class_dict["__doc__"] = mcs.class_doc_inherit(prnt_cls_doc, clsdoc)

            for attr, attribute in class_dict.items():
                if not (attr.startswith("_") and attr.endswith("__")):
                    attr_doc = attribute.__doc__

                    prnt_attr_doc = None
                    for mro_cls in (mro_cls for base in class_bases for mro_cls in base.mro()
                                    if hasattr(mro_cls, attr)):
                        prnt_attr_doc = getattr(getattr(mro_cls, attr), "__doc__")
                        if prnt_attr_doc is not None:
                            break

                    if isinstance(attribute, property):
                        new_prop = property(fget=attribute.fget,
                                            fset=attribute.fset,
                                            fdel=attribute.fdel,
                                            doc=mcs.attr_doc_inherit(prnt_attr_doc, attr_doc))
                        class_dict[attr] = new_prop
                    else:
                        try:
                            attribute.__doc__ = mcs.attr_doc_inherit(prnt_attr_doc, attr_doc)
                        except TypeError:
                            print(attribute)
                            print(attr)
                            print(attribute.__doc__)
            return type.__new__(mcs, class_name, class_bases, class_dict)

        @staticmethod
        @abstractmethod
        def class_doc_inherit(prnt_cls_doc, child_doc):
            raise NotImplementedError

        @staticmethod
        @abstractmethod
        def attr_doc_inherit(prnt_attr_doc, child_doc):
            raise NotImplementedError


    ABCDocInheritorBase = type("ABCDocInheritorBase", (ABCMeta, DocInheritorBase), {})