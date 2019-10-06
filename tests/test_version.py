try:
    _basestring = basestring
except NameError:
    _basestring = str  # Python 2 -> 3 alias


def test_version():
    import custom_inherit

    assert isinstance(custom_inherit.__version__, _basestring)
    assert custom_inherit.__version__
    assert "unknown" not in custom_inherit.__version__
