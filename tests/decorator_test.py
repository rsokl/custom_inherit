from abc import ABCMeta, abstractmethod, abstractproperty
from inspect import getdoc, ismethod
from types import FunctionType, MethodType

from six import add_metaclass

from custom_inherit import doc_inherit

try:
    from inspect import signature
except ImportError:
    from inspect import getargspec as signature


def style(x, y):
    return "valid"


@add_metaclass(ABCMeta)
class Kid(object):
    @classmethod
    @doc_inherit("", style=style)
    def clsmthd(cls):
        """"""
        pass

    @staticmethod
    @doc_inherit("", style=style)
    def static():
        """"""
        pass

    @property
    @doc_inherit("", style=style)
    def prop(self):
        """"""
        return None

    @abstractmethod
    @doc_inherit("", style=style)
    def absmthd(self):
        """"""
        pass

    @abstractproperty
    @doc_inherit("", style=style)
    def absproperty(self):
        """"""
        return None


class Kid2(object):
    @doc_inherit("", style=style)
    def method(self, x, y=None):
        """"""
        pass


def test_sideeffect():
    def f(x, y=None, **kwargs):
        return None

    assert f == doc_inherit("")(f)
    assert signature(f) == signature(doc_inherit("")(f))


def test_function():
    @doc_inherit("", style=style)
    def f(x, y=None, **kwargs):
        return None

    assert getdoc(f) == "valid"


def test_args_filter():
    def parent(foo):
        """
        Args:
            foo: bar
        """

    @doc_inherit(parent, style="google_with_merge")
    def child(x):
        """
        Args:
            x: X
        """

    assert child.__doc__ == "Parameters:\n    x: X"

def test_method():
    assert isinstance(Kid2().method, MethodType)
    assert getdoc(Kid2.method) == "valid"


def test_classmethod():
    assert ismethod(Kid.clsmthd) and Kid.clsmthd.__self__ is Kid
    assert getdoc(Kid.clsmthd) == "valid"


def test_staticmethod():
    assert isinstance(Kid.static, FunctionType)
    assert getdoc(Kid.static) == "valid"


def test_property():
    assert isinstance(Kid.prop, property)
    assert getdoc(Kid.prop) == "valid"


def test_abstract_method():
    assert "absmthd" in Kid.__abstractmethods__
    assert getdoc(Kid.absmthd) == "valid"


def test_abstract_property():
    assert "absproperty" in Kid.__abstractmethods__
    assert getdoc(Kid.absproperty) == "valid"
