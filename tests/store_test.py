""" Tests behavior of custom_inherit._Store """

from pytest import raises

from custom_inherit import _Store, _style_store, store


def bad_style_sig1(x, y, z):
    return None


def bad_style_sig2(x):
    return None


def bad_style_type(x, y):
    return float(x)


def bad_style_type2(x, y):
    return 1


def good_style1(x, y):
    return ",".join((x, y))


def good_style2(x, y):
    return None


def test_Store():
    _store = _Store()
    with raises(TypeError):
        _store[bad_style_sig1]

    with raises(TypeError):
        _store["bad_style"] = bad_style_sig1

    with raises(TypeError):
        _store[bad_style_sig2]

    with raises(TypeError):
        _store[bad_style_type]

    with raises(TypeError):
        _store[bad_style_type2]

    assert _store[good_style1] == good_style1
    assert _store[good_style2] == good_style2

    _store["test_style"] = good_style1
    assert _store["test_style"] == good_style1

    _store = _Store(test_style=good_style1)
    assert _store._store == dict(test_style=good_style1)

    assert _store.pop("test_style") == good_style1
    assert _store._store == dict()


def test_store():
    assert isinstance(store, _Store)
    assert set(store.items()) == set(
        (key, getattr(_style_store, key)) for key in _style_store.__all__
    )
    assert "parent" in store.keys()
    assert "numpy" in store.keys()
