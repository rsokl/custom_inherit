"""http://stackoverflow.com/a/8101118/6592114"""
from abc import abstractmethod, ABCMeta
import sys

""" Exposes abstract base meta class to be inherited by inheritance-style meta classes.

    This metaclass merges the respective docstrings of a parent class and its child, and their
    properties, methods (includeingclassmethod, staticmethod, decorated methods)

    This merge-style must be implemented via the static methods `class_doc_inherit`
    and `attr_doc_inherit`. See custom_inherit/style_store.py for such implementations."""

__all__ = ["DocInheritorBase", "ABCDocInheritorBase"]

if sys.version_info >= (3, 0):  # Python 3
    class DocInheritorBase(type):
        def __new__(mcs, class_name, class_bases, class_dict):
            clsdoc = class_dict.get("__doc__", None)

            # inherit class docstring
            prnt_cls_doc = None
            for mro_cls in (mro_cls for base in class_bases for mro_cls in base.mro()):
                prnt_cls_doc = mro_cls.__doc__
                if prnt_cls_doc is not None:
                    if prnt_cls_doc == "The most base type":
                        prnt_cls_doc = None
                    break

            class_dict["__doc__"] = mcs.class_doc_inherit(prnt_cls_doc, clsdoc)

            # inherit method/property docstring
            for attr, attribute in class_dict.items():
                if not(attr.startswith("__") and attr.endswith("__")):

                    if isinstance(attribute, (staticmethod, classmethod)):
                        attribute = attribute.__func__

                    prnt_attr_doc = None
                    for mro_cls in (mro_cls for base in class_bases for mro_cls in base.mro()
                                    if hasattr(mro_cls, attr)):
                        prnt_attr_doc = getattr(getattr(mro_cls, attr), "__doc__")
                        if prnt_attr_doc is not None:
                            break

                    attribute.__doc__ = mcs.attr_doc_inherit(prnt_attr_doc, attribute.__doc__)

            return type.__new__(mcs, class_name, class_bases, class_dict)

        @staticmethod
        @abstractmethod
        def class_doc_inherit(prnt_cls_doc, child_doc):
            """ Merge the docstrings of a parent class and its child.

                Parameters
                ----------
                prnt_cls_doc: Union[None, str]
                child_doc: Union[None, str]

                Raises
                ------
                NotImplementedError"""
            raise NotImplementedError

        @staticmethod
        @abstractmethod
        def attr_doc_inherit(prnt_attr_doc, child_doc):
            """ Merge the docstrings of method or property from parent class and the corresponding
                attribute of its child.

                Parameters
                ----------
                prnt_cls_doc: Union[None, str]
                child_doc: Union[None, str]

                Raises
                ------
                NotImplementedError

                Notes
                -----
                This works for properties, methods, static methods, class methods, and
                decorated methods/properties."""
            raise NotImplementedError


    ABCDocInheritorBase = type("ABCDocInheritorBase", (ABCMeta, DocInheritorBase), {})


else:  # Python 2
    class DocInheritorBase(type):
        def __new__(mcs, class_name, class_bases, class_dict):
            clsdoc = class_dict.get("__doc__", None)

            # inherit class docstring
            prnt_cls_doc = None
            for mro_cls in (mro_cls for base in class_bases for mro_cls in base.mro()):
                prnt_cls_doc = mro_cls.__doc__
                if prnt_cls_doc is not None:
                    break

            class_dict["__doc__"] = mcs.class_doc_inherit(prnt_cls_doc, clsdoc)

            # inherit method/property docstring
            for attr, attribute in class_dict.items():
                if not (attr.startswith("_") and attr.endswith("__") or isinstance(attribute, type)):
                    child_attr = attribute if not isinstance(attribute, (staticmethod,
                                                                         classmethod)) else attribute.__func__
                    prnt_attr_doc = None
                    for mro_cls in (mro_cls for base in class_bases for mro_cls in base.mro()
                                    if hasattr(mro_cls, attr)):
                        prnt_attr_doc = getattr(getattr(mro_cls, attr), "__doc__")
                        if prnt_attr_doc is not None:
                            break

                    # property.__doc__ is read-only in Python 2; unpack and initialize new property
                    if isinstance(attribute, property):
                        new_prop = property(fget=attribute.fget,
                                            fset=attribute.fset,
                                            fdel=attribute.fdel,
                                            doc=mcs.attr_doc_inherit(prnt_attr_doc, child_attr.__doc__))
                        class_dict[attr] = new_prop
                    else:
                        child_attr.__doc__ = mcs.attr_doc_inherit(prnt_attr_doc, child_attr.__doc__)

            return type.__new__(mcs, class_name, class_bases, class_dict)

        @staticmethod
        @abstractmethod
        def class_doc_inherit(prnt_cls_doc, child_doc):
            """ Merge the docstrings of a parent class and its child.

                Parameters
                ----------
                prnt_cls_doc: Union[None, str]
                child_doc: Union[None, str]

                Raises
                ------
                NotImplementedError"""
            raise NotImplementedError

        @staticmethod
        @abstractmethod
        def attr_doc_inherit(prnt_attr_doc, child_doc):
            """ Merge the docstrings of method or property from parent class and the corresponding
                attribute of its child.

                Parameters
                ----------
                prnt_cls_doc: Union[None, str]
                child_doc: Union[None, str]

                Raises
                ------
                NotImplementedError

                Notes
                -----
                This works for properties, methods, static methods, class methods, and
                decorated methods/properties."""
            raise NotImplementedError


    ABCDocInheritorBase = type("ABCDocInheritorBase", (ABCMeta, DocInheritorBase), {})
