from custom_inherit.style_store import parent, numpy

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


numpy_out = 'first line\n\nDeprecation Warning\n-------------------\ndep\n\nAttributes\n----------\nparams\n    ' \
            'indented\n\nmulti-line\n\nExtended Summary\n----------------\nextended\n\nParameters\n----------\n' \
            'params\n\nReturns\n-------\nreturn\n\nYields\n------\nyield\n\nOther Parameters\n----------------\nother' \
            '\n\nRaises\n------\nraise\n\nSee Also\n--------\nsee\n\nNotes\n-----\nnote\n\nReferences\n----------' \
            '\nref \n\nExamples\n--------\nexample'


def test_numpy():
    assert numpy(prnt.__doc__, child.__doc__) == numpy_out

