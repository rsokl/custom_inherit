def test_version():
    import custom_inherit

    assert isinstance(custom_inherit.__version__, str)
    assert custom_inherit.__version__
    assert "unknown" not in custom_inherit.__version__
