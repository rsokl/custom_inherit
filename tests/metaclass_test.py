from abc import ABCMeta, abstractmethod, abstractproperty
from inspect import getdoc, ismethod
from types import FunctionType, MethodType

from six import add_metaclass

from custom_inherit import DocInheritMeta

try:
    from inspect import signature
except ImportError:
    from inspect import getargspec as signature


def style(x, y):
    return "valid"


""" With ABC"""


@add_metaclass(DocInheritMeta(style=style, abstract_base_class=True))
class Parent(object):
    def method(self, x, y=None):
        """"""
        pass

    @classmethod
    def clsmthd(cls):
        """"""
        pass

    @staticmethod
    def static():
        """"""
        pass

    @property
    def prop(self):
        """"""
        return None

    @abstractmethod
    def absmthd(self):
        """"""
        pass

    @abstractproperty
    def absproperty(self):
        """"""
        return None


class Kid(Parent):
    def __init__(self):
        """kid"""
        pass

    def kid_method(self):
        """kid"""
        pass

    def method(self, x, y=None):
        pass

    @classmethod
    def clsmthd(cls):
        pass

    @staticmethod
    def static():
        pass

    @property
    def prop(self):
        return None

    def absmthd(self):
        pass

    @property
    def absproperty(self):
        return None


def test_abc():
    assert isinstance(Parent, ABCMeta)
    assert isinstance(Kid, ABCMeta)


def test_sideeffect():
    assert getdoc(Kid.kid_method) == "kid"
    assert signature(Kid.method) == signature(Parent.method)


def test_special_method():
    # by default, Kid.__init__ docstring should not inherit from its parent
    assert isinstance(Kid().__init__, MethodType)
    assert getdoc(Kid.__init__) == "kid"


def test_method():
    assert isinstance(Kid().method, MethodType)
    assert getdoc(Kid.method) == "valid"


def test_classmethod():
    assert ismethod(Kid.clsmthd) and Kid.clsmthd.__self__ is Kid
    assert getdoc(Kid.clsmthd) == "valid"


def test_staticmethod():
    assert isinstance(Kid().static, FunctionType)
    assert getdoc(Kid.static) == "valid"


def test_property():
    assert isinstance(Kid.prop, property)
    assert getdoc(Kid.prop) == "valid"


def test_abstract_method():
    assert "absmthd" in Parent.__abstractmethods__
    assert getdoc(Kid.absmthd) == "valid"


def test_abstract_property():
    assert "absproperty" in Parent.__abstractmethods__
    assert getdoc(Kid.absproperty) == "valid"


""" Without ABC"""


@add_metaclass(DocInheritMeta(style=style))
class Parent2(object):
    def method(self, x, y=None):
        """"""
        pass

    @classmethod
    def clsmthd(cls):
        """"""
        pass

    @staticmethod
    def static():
        """"""
        pass

    @property
    def prop(self):
        """"""
        return None


class Kid2(Parent2):
    def __init__(self):
        """kid"""
        pass

    def kid_method(self):
        """kid"""
        pass

    def method(self, x, y=None):
        pass

    @classmethod
    def clsmthd(cls):
        pass

    @staticmethod
    def static():
        pass

    @property
    def prop(self):
        return None


def test_sideeffect2():
    assert getdoc(Kid2.kid_method) == "kid"
    assert signature(Kid2.method) == signature(Parent.method)


def test_special_method2():
    # by default, Kid.__init__ docstring should not inherit from its parent
    assert isinstance(Kid2().__init__, MethodType)
    assert getdoc(Kid2.__init__) == "kid"


def test_method2():
    assert isinstance(Kid2().method, MethodType)
    assert getdoc(Kid2.method) == "valid"


def test_classmethod2():
    assert ismethod(Kid2.clsmthd) and Kid2.clsmthd.__self__ is Kid2
    assert getdoc(Kid2.clsmthd) == "valid"


def test_staticmethod2():
    assert isinstance(Kid2.static, FunctionType)
    assert getdoc(Kid2.static) == "valid"


def test_property2():
    assert isinstance(Kid2.prop, property)
    assert getdoc(Kid2.prop) == "valid"


def test_class_docstring():
    @add_metaclass(DocInheritMeta(style="numpy"))
    class Parent(object):
        """
        Parent class.

        Returns
        -------
        foo
        """

    class Mixin(object):
        """
        This is mixin which does something.

        """

    class Child(Mixin, Parent):
        """
        Attributes
        ----------
        bar
        """

    assert (
        getdoc(Child)
        == "This is mixin which does something.\n\nAttributes\n----------\nbar\n\nReturns\n-------\nfoo"
    )


def test_class_docstring_merge_hierarchy_numpy():
    @add_metaclass(DocInheritMeta(style="numpy_with_merge"))
    class GrandParent(object):
        """GrandParent.

        Attributes
        ----------
        foo
        """

    class Parent(GrandParent):
        """
        Attributes
        ----------
        bar
        """

    class Child(Parent):
        pass

    assert (
        getdoc(Child)
        == "GrandParent.\n\nAttributes\n----------\nfoo\nbar"
    )


def test_class_docstring_merge_hierarchy_google():
    @add_metaclass(DocInheritMeta(style="google_with_merge"))
    class GrandParent(object):
        """GrandParent.

        Args:
            foo
        """

    class Parent(GrandParent):
        """
        Args:
            bar
        """

    class Child(Parent):
        pass

    assert (
        getdoc(Child)
        == "GrandParent.\n\nParameters:\n    foo\n    bar"
    )


""" Include special method option"""

@add_metaclass(DocInheritMeta(style=style, include_special_methods=True))
class Parent3(object):
    def __init__(self):
        """"""
        pass

class Kid3(Parent3):
    def __init__(self):
        """kid"""
        pass

def test_special_method3():
    # __init__ docstring should inherit from Parent3
    assert isinstance(Kid3().__init__, MethodType)
    assert getdoc(Kid3.__init__) == "valid"
