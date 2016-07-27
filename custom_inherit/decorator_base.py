from functools import wraps


class DocInheritDecorator(object):
    def __init__(self, prnt_doc):
        self.prnt_doc = prnt_doc if isinstance(prnt_doc, str) else prnt_doc.__doc__

    def __call__(self, func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            return func(*args, **kwargs)
        wrapped.__doc__ = self.doc_merger(self.prnt_doc, func.__doc__)
        return wrapped

    @staticmethod
    def doc_merger(prnt_attr_doc, child_doc):
        """ Merge the docstrings of method or property from parent class and the corresponding
            attribute of its child.

            Parameters
            ----------
            prnt_cls_doc: Union[None, str]
            child_doc: Union[None, str]

            Raises
            ------
            NotImplementedError

            Notes
            -----
            This works for properties, methods, static methods, class methods, and
            decorated methods/properties."""
        raise NotImplementedError
