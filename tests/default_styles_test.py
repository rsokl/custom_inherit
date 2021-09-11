import custom_inherit

from custom_inherit._metaclass_base import new_func_with_doc


def test_parent():
    assert custom_inherit.store["parent"]("a", new_func_with_doc("b")) == "b"
    assert custom_inherit.store["parent"]("a", None) == "a"
    assert custom_inherit.store["parent"](None, None) is None


def test_numpy():
    def prnt(params, other):
        """first line

        Attributes
        ----------
        params
            indented

        multi-line

        Extended Summary
        ----------------
        extended

        Returns
        -------
        return

        Other Parameters
        ----------------
        other

        See Also
        --------
        see

        References
        ----------
        ref"""
        pass

    def child(params):
        """Deprecation Warning
        -------------------
        dep

        Parameters
        ----------
        params

        Yields
        ------
        yield

        Raises
        ------
        raise

        Notes
        -----
        note

        Examples
        --------
        example
        """
        pass

    numpy_out = (
        "first line\n\nDeprecation Warning\n-------------------\ndep\n\nAttributes\n----------\nparams\n    "
        "indented\n\nmulti-line\n\nExtended Summary\n----------------\nextended\n\nParameters\n----------\n"
        "params\n\nReturns\n-------\nreturn\n\nYields\n------\nyield\n\n"
        "Raises\n------\nraise\n\nSee Also\n--------\nsee\n\n"
        "Notes\n-----\nnote\n\nReferences\n----------"
        "\nref\n\nExamples\n--------\nexample"
    )
    assert custom_inherit.store["numpy"](None, None) is None
    assert custom_inherit.store["numpy"]("", new_func_with_doc("")) is None
    assert custom_inherit.store["numpy"]("valid", None) == "valid"
    assert custom_inherit.store["numpy"](None, new_func_with_doc("valid")) == "valid"
    assert custom_inherit.store["numpy"](prnt.__doc__, child) == numpy_out


def test_reST():
    def prnt2():
        """Parent's front-matter
        +++++++++++
        Parent-Only
        +++++++++++
        params
            indented

        multi-line

        Shared
        ******
        parent-shared

        Empty
        ~~~~~"""
        pass

    def child2():
        """Child's front-matter
        continued
        ++bad+
        Shared
        ******
        child-shared

        ##########
        Child-Only
        ##########
        child-only"""
        pass

    reST_out = (
        "Child's front-matter\ncontinued\n++bad+\n\n+++++++++++\nParent-Only\n+++++++++++\nparams"
        "\n    indented\n\nmulti-line\n\nShared\n******\nchild-shared\n\nEmpty\n~~~~~\n\n\n##########"
        "\nChild-Only\n##########\nchild-only"
    )

    assert custom_inherit.store["reST"](None, None) == ""
    assert custom_inherit.store["reST"]("", new_func_with_doc("")) == ""
    assert custom_inherit.store["reST"]("valid", None) == "valid"
    assert custom_inherit.store["reST"](None, new_func_with_doc("valid")) == "valid"
    assert custom_inherit.store["reST"](prnt2.__doc__, child2) == reST_out


def test_numpy_napoleon():
    def prnt(params, other):
        """Parent's short summary

        Parent's extended summary

        Attributes
        ----------
        params
            indented

        multi-line

        Methods
        -------
        parent methods


        Keyword Arguments
        -----------------
        parent's section

        Parameters
        ----------
        params: parent's Parameters

        Returns
        -------
        return

        Other Parameters
        ----------------
        other

        See Also
        --------
        see

        References
        ----------
        ref

        Todo
        ----
        todo

        Yield
        -----
        alias of Yields - parent's"""
        pass

    def child(params):
        """Child's short summary

        Child's extended summary

        Args
        ----
        params: alias for Parameters - child's section

        Keyword Args
        ------------
        alias for Keyword Arguments - child's section

        Yields
        ------
        yield

        Raises
        ------
        raise

        Notes
        -----
        note

        Examples
        --------
        example

        Warns
        -----
        warns

        Warnings
        --------
        warnings
        """
        pass

    out = (
        "Child's short summary\n\nChild's extended summary\n\nAttributes\n----------\n"
        "params\n    indented\n\nmulti-line\n\nMethods\n-------\nparent methods\n\nWarning"
        "\n-------\nwarnings\n\nParameters\n----------\nparams: alias for Parameters - child's section"
        "\n\nKeyword Arguments\n-----------------"
        "\nalias for Keyword Arguments - child's section\n\nReturns\n-------\nreturn\n\nYields"
        "\n------\nyield\n\nRaises\n------\nraise\n\nNotes\n-----\nnote\n\nWarns\n-----\nwarns"
        "\n\nSee Also\n--------\nsee\n\nReferences\n----------\nref\n\nTodo\n----\ntodo\n\nExamples"
        "\n--------\nexample"
    )

    assert custom_inherit.store["numpy_napoleon"](None, None) is None
    assert custom_inherit.store["numpy_napoleon"]("", new_func_with_doc("")) is None
    assert custom_inherit.store["numpy_napoleon"]("valid", None) == "valid"
    assert custom_inherit.store["numpy_napoleon"](None, new_func_with_doc("valid")) == "valid"
    assert custom_inherit.store["numpy_napoleon"](prnt.__doc__, child) == out


def test_methods_section_in_numpy():
    from six import add_metaclass

    from custom_inherit import DocInheritMeta

    # __import__('pudb').set_trace()
    @add_metaclass(metaclass=DocInheritMeta(style="numpy_with_merge"))
    class Parent:
        """Parent summary.

        Methods
        -------
        meth
        """

        pass

    class Child(Parent):
        """Child summary.

        Attributes
        ----------
        a: hello

        """

        pass

    c = Child()
    expected = """Child summary.

Attributes
----------
a: hello

Methods
-------
meth"""
    assert c.__doc__ == expected


def test_google_napoleon():
    def prnt(params, other):
        """first line

        Attributes:
            params
                - indented

            multi-line

        Methods:
            parent methods


        Keyword Arguments:
            parent's section

        Parameters:
            params: parent's Parameters

        Extended Summary:
            extended

        Returns:
            return

        Other Parameters:
            other

        See Also:
            see

        References:
            ref

        Todo:
            todo

        Yield:
            alias of Yields - parent's"""
        pass

    def child(params):
        """
        Args:
            params: alias for Parameters - child's section

        Keyword Args:
            alias for Keyword Arguments - child's section

        Yields:
            yield

        Raises:
            raise

        Notes:
            note

        Examples:
            example

        Warns:
            warns

        Warnings:
            warnings
        """
        pass

    out = (
        "first line\n\nAttributes:\n    params\n        - indented\n\n    multi-line\n\nMethods:\n    "
        "parent methods\n\nWarning:\n    warnings\n\nParameters:\n    params: alias for Parameters - child's "
        "section\n\nKeyword Arguments:\n    alias for Keyword Arguments - child's "
        "section\n\nReturns:\n    return\n\nYields:\n    yield\n\nRaises:\n    raise\n\nNotes:\n    note\n\n"
        "Warns:\n    warns\n\nSee Also:\n    see\n\nReferences:\n    ref\n\nTodo:\n    todo\n\nExamples:\n    example"
    )

    assert custom_inherit.store["google"](None, None) is None
    assert custom_inherit.store["google"]("", new_func_with_doc("")) is None
    assert custom_inherit.store["google"]("valid", None) == "valid"
    assert custom_inherit.store["google"](None, new_func_with_doc("valid")) == "valid"
    assert custom_inherit.store["google"](prnt.__doc__, child) == out


def test_google_with_merge():
    def prnt(params, other):
        """first parent's line

        Attributes:
            params
                - indented

            multi-line

        Methods:
            parent methods

        Keyword Arguments:
            parent's section

        Parameters:
            params: parent's Parameters

        Examples:
            parents's example

        Extended Summary:
            extended

        Returns:
            return

        Other Parameters:
            other

        See Also:
            see

        References:
            ref

        Todo:
            todo

        Yield:
            alias of Yields - parent's"""
        pass

    def child(params):
        """first child's line

        Args:
            params: alias for Parameters - child's section

        Keyword Args:
            alias for Keyword Arguments - child's section

        Yields:
            yield

        Raises:
            raise

        Notes:
            note

        Examples:
            child's example

        Warns:
            warns

        Warnings:
            warnings
        """
        pass

    out = (
        "first child's line\n\nAttributes:\n    params\n        - indented\n\n    "
        "multi-line\n\nMethods:\n    parent methods\n\nWarning:\n    warnings\n\nParameters:\n    "
        "params: alias for Parameters - child's section"
        "\n\nKeyword Arguments:\n    parent's section\n    alias for Keyword Arguments - child's section"
        "\n\nReturns:\n    return\n\nYields:\n    yield\n\nRaises:\n    "
        "raise\n\nNotes:\n    note\n\nWarns:\n    warns\n\nSee Also:\n    see\n\nReferences:\n    "
        "ref\n\nTodo:\n    todo\n\nExamples:\n    child's example"
    )
    assert custom_inherit.store["google_with_merge"](None, None) is None
    assert custom_inherit.store["google_with_merge"]("", new_func_with_doc("")) is None
    assert custom_inherit.store["google_with_merge"]("valid", None) == "valid"
    assert custom_inherit.store["google_with_merge"](None, new_func_with_doc("valid")) == "valid"
    assert custom_inherit.store["google_with_merge"](prnt.__doc__, child) == out


def test_numpy_with_merge():
    def prnt(param, other):
        """first parent's line

        Attributes
        ----------
        parent's params
            indented

        multi-line

        Parameters
        ----------
        params: Parent's param

        Extended Summary
        ----------------
        extended

        Returns
        -------
        return

        Other Parameters
        ----------------
        other

        See Also
        --------
        see

        Examples
        --------
        Parent's example

        References
        ----------
        ref"""
        pass

    def child(params):
        """first child's line

        Deprecation Warning
        -------------------
        dep

        Parameters
        ----------
        params: child's params

        Yields
        ------
        yield

        Raises
        ------
        raise

        Notes
        -----
        note

        Examples
        --------
        child's example
        """
        pass

    numpy_out = (
        "first child's line\n\nDeprecation Warning\n-------------------\ndep\n\nAttributes\n----------"
        "\nparent's params\n    indented\n\nmulti-line\n\nExtended Summary\n----------------\nextended\n"
        "\nParameters\n----------\nparams: child's params\n\nReturns\n-------\nreturn\n\nYields"
        "\n------\nyield\n\nRaises\n------\nraise\n\nSee Also"
        "\n--------\nsee\n\nNotes\n-----\nnote\n\nReferences\n----------\nref\n\nExamples\n--------\n"
        "child's example"
    )
    assert custom_inherit.store["numpy_with_merge"](None, None) is None
    assert custom_inherit.store["numpy_with_merge"]("", new_func_with_doc("")) is None
    assert custom_inherit.store["numpy_with_merge"]("valid", None) == "valid"
    assert custom_inherit.store["numpy_with_merge"](None, new_func_with_doc("valid")) == "valid"
    assert (
        custom_inherit.store["numpy_with_merge"](prnt.__doc__, child)
        == numpy_out
    )


def test_numpy_napoleon_with_merge():
    def prnt(params, other):
        """Parent's short summary

        Parent's extended summary

        Attributes
        ----------
        params
            indented

        multi-line

        Methods
        -------
        parent methods


        Keyword Arguments
        -----------------
        parent's section

        Parameters
        ---------
        params: parent's Parameters

        Returns
        -------
        return

        Other Parameters
        ----------------
        other

        Examples
        --------
        parent's example

        See Also
        --------
        see

        References
        ----------
        ref

        Todo
        ----
        todo

        Yield
        -----
        alias of Yields - parent's"""
        pass

    def child(params):
        """Child's short summary

        Child's extended summary

        Args
        ----
        params: alias for Parameters - child's section

        Keyword Args
        ------------
        alias for Keyword Arguments - child's section

        Yields
        ------
        yield

        Raises
        ------
        raise

        Notes
        -----
        note

        Examples
        --------
        child's example

        Warns
        -----
        warns

        Warnings
        --------
        warnings
        """
        pass

    out = (
        "Child's short summary\n\nChild's extended summary\n\nAttributes\n----------\nparams\n    "
        "indented\n\nmulti-line\n\nMethods\n-------\nparent methods\n\nWarning\n-------\nwarnings\n"
        "\nParameters\n----------\nparams: alias for Parameters - child's section"
        "\n\nKeyword Arguments\n-----------------\n"
        "parent's section\nalias for Keyword Arguments - child's section\n\nReturns\n-------\n"
        "return\n\nYields\n------\nyield\n\nRaises\n------\nraise\n"
        "\nNotes\n-----\nnote\n\nWarns\n-----\nwarns\n\nSee Also\n--------\nsee\n\nReferences\n"
        "----------\nref\n\nTodo\n----\ntodo\n\nExamples\n--------\nchild's example"
    )
    assert custom_inherit.store["numpy_napoleon_with_merge"](None, None) is None
    assert custom_inherit.store["numpy_napoleon_with_merge"]("", new_func_with_doc("")) is None
    assert custom_inherit.store["numpy_napoleon_with_merge"]("valid", None) == "valid"
    assert custom_inherit.store["numpy_napoleon_with_merge"](None, new_func_with_doc("valid")) == "valid"
    assert (
        custom_inherit.store["numpy_napoleon_with_merge"](prnt.__doc__, child)
        == out
    )
