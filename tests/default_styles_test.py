from custom_inherit._style_store import parent, numpy, reST, google, numpy_napoleon

def test_parent():
    assert parent("a", "b") == "b"
    assert parent("a", None) == "a"
    assert parent(None, None) is None


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
            'params\n\nReturns\n-------\nreturn\n\nYields\n------\nyield\n\nOther Parameters\n----------------\nother' \
            '\n\nRaises\n------\nraise\n\nSee Also\n--------\nsee\n\nNotes\n-----\nnote\n\nReferences\n----------' \
            '\nref\n\nExamples\n--------\nexample'


def test_numpy():
    assert numpy(None, None) is None
    assert numpy('', '') is None
    assert numpy('valid', None) == 'valid'
    assert numpy(None, 'valid') == 'valid'
    assert numpy(prnt.__doc__, child.__doc__) == numpy_out


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


def test_reST():
    assert reST(None, None) == ''
    assert reST('', '') == ''
    assert reST('valid', None) == 'valid'
    assert reST(None, 'valid') == 'valid'
    assert reST(prnt2.__doc__, child2.__doc__) == reST_out


