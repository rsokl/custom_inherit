from __future__ import absolute_import

from abc import abstractproperty
from types import FunctionType, MethodType

""" Exposes abstract base meta class to be inherited by inheritance-style meta classes.

    This metaclass merges the respective docstrings of a parent class and its child, and their
    properties, methods (including classmethod, staticmethod, decorated methods)

    This merge-style must be implemented via the static methods `class_doc_inherit`
    and `attr_doc_inherit`. See custom_inherit/_style_store.py for such implementations."""

__all__ = ["DocInheritorBase"]


class DocInheritorBase(type):
    """ A metaclass that merges the respective docstrings of a parent class and of its child, along with their
    properties, methods (including classmethod, staticmethod, decorated methods).

    This merge-style must be implemented via the static methods `class_doc_inherit`
    and `attr_doc_inherit`, which are set within `custom_inherit.DocInheritMeta`."""

    include_special_methods = False

    def __new__(mcs, class_name, class_bases, class_dict):
        # inherit class docstring: the docstring is constructed by traversing
        # the mro for the class and merging their docstrings, with each next
        # docstring as serving as the 'parent', and the accumulated docstring
        # serving as the 'child'
        this_doc = class_dict.get("__doc__", None)
        for mro_cls in (mro_cls for base in class_bases for mro_cls in base.mro()):
            prnt_cls_doc = mro_cls.__doc__
            if prnt_cls_doc is not None:
                if prnt_cls_doc == "The most base type":
                    prnt_cls_doc = None
            this_doc = mcs.class_doc_inherit(prnt_cls_doc, this_doc)

        class_dict["__doc__"] = this_doc

        # inherit docstring for method, static-method, class-method, abstract-method, decorated-method, and property
        for attr, attribute in class_dict.items():
            is_doc_type = isinstance(
                attribute,
                (FunctionType, MethodType, classmethod, staticmethod, property),
            )
            if (
                (attr.startswith("__") and attr.endswith("__") and not mcs.include_special_methods) or
                not is_doc_type
            ):
                continue

            is_static_or_class = isinstance(attribute, (staticmethod, classmethod))
            child_attr = attribute if not is_static_or_class else attribute.__func__

            prnt_attr_doc = None
            for mro_cls in (
                mro_cls
                for base in class_bases
                for mro_cls in base.mro()
                if hasattr(mro_cls, attr)
            ):
                prnt_attr_doc = getattr(mro_cls, attr).__doc__

                if prnt_attr_doc is not None:
                    break

            if prnt_attr_doc is None:
                continue

            doc = mcs.attr_doc_inherit(prnt_attr_doc, child_attr.__doc__)
            try:
                child_attr.__doc__ = doc
            # property.__doc__ is read-only in Python 2 (TypeError), 3.3 - 3.4 (AttributeError)
            except (TypeError, AttributeError) as err:
                if type(child_attr) in (property, abstractproperty):
                    new_prop = property(
                        fget=child_attr.fget,
                        fset=child_attr.fset,
                        fdel=child_attr.fdel,
                        doc=doc,
                    )
                    if isinstance(child_attr, abstractproperty):
                        new_prop = abstractproperty(new_prop)
                    class_dict[attr] = new_prop
                else:
                    raise type(err)(err)

        return type.__new__(mcs, class_name, class_bases, class_dict)

    @staticmethod
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
    def attr_doc_inherit(prnt_attr_doc, child_doc):
        """ Merge the docstrings of method or property from parent class and the corresponding
        attribute of its child.

        Parameters
        ----------
        prnt_attr_doc: Union[None, str]
        child_doc: Union[None, str]

        Raises
        ------
        NotImplementedError

        Notes
        -----
        This works for properties, methods, static methods, class methods, and
        decorated methods/properties."""
        raise NotImplementedError
