from __future__ import absolute_import
from collections import OrderedDict
import inspect

def parse_rest_doc(doc):
    """ Extract the headers, delimiters, and text from reST-formatted docstrings.

        Parameters
        ----------
        doc: Union[str, None] """

    if not doc:
        return OrderedDict()

    doc = inspect.cleandoc(doc)