from custom_inherit._style_store import parent, numpy, reST, google, numpy_napoleon


def test_parent():
    assert parent("a", "b") == "b"
    assert parent("a", None) == "a"
    assert parent(None, None) is None


def test_numpy():
    def prnt():
        """ first line

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
            ref """
        pass

    def child():
        """ Deprecation Warning
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

    numpy_out = 'first line\n\nDeprecation Warning\n-------------------\ndep\n\nAttributes\n----------\nparams\n    ' \
                'indented\n\nmulti-line\n\nExtended Summary\n----------------\nextended\n\nParameters\n----------\n' \
                'params\n\nReturns\n-------\nreturn\n\nYields\n------\nyield\n\nOther Parameters' \
                '\n----------------\nother\n\nRaises\n------\nraise\n\nSee Also\n--------\nsee\n\n' \
                'Notes\n-----\nnote\n\nReferences\n----------' \
                '\nref\n\nExamples\n--------\nexample'
    assert numpy(None, None) is None
    assert numpy('', '') is None
    assert numpy('valid', None) == 'valid'
    assert numpy(None, 'valid') == 'valid'
    assert numpy(prnt.__doc__, child.__doc__) == numpy_out


def test_reST():

    def prnt2():
        """ Parent's front-matter
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
        """ Child's front-matter
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

    reST_out = "Child's front-matter\ncontinued\n++bad+\n\n+++++++++++\nParent-Only\n+++++++++++\nparams" \
               "\n    indented\n\nmulti-line\n\nShared\n******\nchild-shared\n\nEmpty\n~~~~~\n\n\n##########" \
               "\nChild-Only\n##########\nchild-only"

    assert reST(None, None) == ''
    assert reST('', '') == ''
    assert reST('valid', None) == 'valid'
    assert reST(None, 'valid') == 'valid'
    assert reST(prnt2.__doc__, child2.__doc__) == reST_out


def test_numpy_napoleon():
    def prnt3():
        """ first line

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
            parent's Parameters

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
            ref

            Todo
            ----
            todo

            Yield
            -----
            alias of Yields - parent's"""
        pass

    def child3():
        """ Args
            ----
            alias for Parameters - child's section

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

    out = "first line\n\nAttributes\n----------\nparams\n    indented\n\nmulti-line\n\nMethods\n-------\n" \
          "parent methods\n\nWarning\n-------\nwarnings\n\nParameters\n----------\n" \
          "alias for Parameters - child's section\n\nOther Parameters\n----------------\nother\n\n" \
          "Keyword Arguments\n-----------------\nalias for Keyword Arguments - child's section\n\nReturns" \
          "\n-------\nreturn\n\nYields\n------\nyield\n\nRaises\n------\nraise\n\nNotes\n-----\nnote\n\nWarns" \
          "\n-----\nwarns\n\nSee Also\n--------\nsee\n\nReferences\n----------\nref\n\nTodo\n----\ntodo\n\n" \
          "Examples\n--------\nexample"

    assert numpy_napoleon(None, None) is None
    assert numpy_napoleon('', '') is None
    assert numpy_napoleon('valid', None) == 'valid'
    assert numpy_napoleon(None, 'valid') == 'valid'
    assert numpy_napoleon(prnt3.__doc__, child3.__doc__) == out


def test_google_napoleon():
    def prnt():
        """ first line

            Attributes:
                params
                    - indented

                multi-line

            Methods:
                parent methods


            Keyword Arguments:
                parent's section

            Parameters:
                parent's Parameters

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

    def child():
        """ Args:
                alias for Parameters - child's section

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

    out = "first line\n\nAttributes:\n    params\n        - indented\n\n    multi-line\n\nMethods:\n    " \
          "parent methods\n\nWarning:\n    warnings\n\nParameters:\n    alias for Parameters - child's " \
          "section\n\nOther Parameters:\n    other\n\nKeyword Arguments:\n    alias for Keyword Arguments - child's " \
          "section\n\nReturns:\n    return\n\nYields:\n    yield\n\nRaises:\n    raise\n\nNotes:\n    note\n\n" \
          "Warns:\n    warns\n\nSee Also:\n    see\n\nReferences:\n    ref\n\nTodo:\n    todo\n\nExamples:\n    example"

    assert google(None, None) is None
    assert google('', '') is None
    assert google('valid', None) == 'valid'
    assert google(None, 'valid') == 'valid'
    assert google(prnt.__doc__, child.__doc__) == out
