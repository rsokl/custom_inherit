try:
    basestring
except NameError:
    basestring = str  # Python 2 -> 3 alias

""" Exposes decorator class."""

__all__ = ["DocInheritDecorator"]


class DocInheritDecorator(object):
    """ A decorator that merges provided parent docstring with the docstring of the decorated
    function/method/property.

    Methods
    -------
    doc_merger(prnt_attr_doc, child_doc)
        Merges the parent and child docstrings into a single docstring.

    Notes
    -----
    When utilized as the inner-most decorator, this decorator can be used on functions decorated functions,
    methods, properties, static methods, class methods, and their abstract counterparts."""

    def __init__(self, prnt_doc):
        """
        Parameters
        ----------
        prnt_doc : Union[str, Any]
            The docstring, or object of which the docstring is utilized as the
            parent docstring during the docstring merge."""
        self.prnt_doc = (
            prnt_doc if isinstance(prnt_doc, basestring) else prnt_doc.__doc__
        )

    def __call__(self, func):
        """
        Parameters
        ----------
        func : FunctionType
            The function/method/property to be decorated

        Returns
        -------
        FunctionType
            The decorated function/method/property whose docstring is given by
            DocInheritDecorator.doc_merger(prnt_attr_doc, child_doc)"""
        func.__doc__ = self.doc_merger(self.prnt_doc, func.__doc__)
        return func

    @staticmethod
    def doc_merger(prnt_attr_doc, child_doc):
        """ Merges the parent and child docstrings into a single docstring.

        Parameters
        ----------
        prnt_attr_doc: Union[None, str]
        child_doc: Union[None, str]

        Raises
        ------
        NotImplementedError"""
        raise NotImplementedError
