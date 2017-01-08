from __future__ import absolute_import
from collections import OrderedDict
import inspect

__all__ = []


def parse_napoleon_doc(doc, type):
    """ Extract the text from the various sections of a numpy-formatted docstring.

        Parameters
        ----------
        doc: Union[str, None]

        Returns
        -------
        OrderedDict[str, Union[None,str]]
            The extracted numpy-styled docstring sections."""

    assert type in ("google", "numpy")

    napoleon_sections = ["Short Summary", "Attributes", "Methods", "Warning", "Note", "Parameters", "Other Parameters",
                         "Keyword Arguments", "Returns", "Yields", "Raises", "Warns", "See Also", "References", "Todo",
                         "Example", "Examples"]

    aliases = {"Args": "Parameters", "Arguments": "Parameters", "Keyword Args": "Keyword Arguments",
               "Return": "Returns", "Warnings": "Warning", "Yield": "Yields"}

    doc_sections = OrderedDict([(key, None) for key in napoleon_sections])

    if not doc:
        return doc_sections

    doc = inspect.cleandoc(doc)
    lines = iter(doc.splitlines())

    key = "Short Summary"
    body = []
    while True:
        try:
            line = next(lines)
            if line in doc_sections or aliases:
                doc_sections[aliases.get(key, key)] = "\n".join(body).rstrip() if body else None
                body = []
                key = line
                next(lines)  # skip section delimiter
            else:
                body.append(line)
        except StopIteration:
            doc_sections[key] = "\n".join(body)
            break

    return doc_sections

