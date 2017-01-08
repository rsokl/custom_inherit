from __future__ import absolute_import
from .numpy_parse_tools import merge_all_sections

from collections import OrderedDict
import inspect

__all__ = ["merge_google_napoleon_docs", "merge_numpy_napoleon_docs"]


def parse_napoleon_doc(doc, style):
    """ Extract the text from the various sections of a numpy-formatted docstring.

        Parameters
        ----------
        doc: Union[str, None]
            The docstring to parse.

        style: str
            'google' or 'numpy'

        Returns
        -------
        OrderedDict[str, Union[None,str]]
            The extracted numpy-styled docstring sections."""

    napoleon_sections = ["Short Summary", "Attributes", "Methods", "Warning", "Note", "Parameters", "Other Parameters",
                         "Keyword Arguments", "Returns", "Yields", "Raises", "Warns", "See Also", "References", "Todo",
                         "Example", "Examples"]

    aliases = {"Args": "Parameters", "Arguments": "Parameters", "Keyword Args": "Keyword Arguments",
               "Return": "Returns", "Warnings": "Warning", "Yield": "Yields"}

    doc_sections = OrderedDict([(key, None) for key in napoleon_sections])

    if not doc:
        return doc_sections

    assert style in ("google", "numpy")

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
                if style == "numpy":
                    next(lines)  # skip section delimiter
            else:
                body.append(line)
        except StopIteration:
            doc_sections[key] = "\n".join(body)
            break

    return doc_sections


def merge_section(key, prnt_sec, child_sec, style):
    """ Synthesize a output numpy docstring section.

        Parameters
        ----------
        key: str
            The numpy-section being merged.
        prnt_sec: Optional[str]
            The docstring section from the parent's attribute.
        child_sec: Optional[str]
            The docstring section from the child's attribute.
        Returns
        -------
        Optional[str]
            The output docstring section."""
    if prnt_sec is None and child_sec is None:
        return None

    assert style in ("google", "numpy")

    if key == "Short Summary":
        header = ''
    else:
        if style == "numpy":
            header = "\n".join((key, "".join("-" for i in range(len(key))), ""))
        else:
            header = "\n".join((key, ""))

    body = prnt_sec if child_sec is None else child_sec

    return header + body


def merge_numpy_napoleon_docs(prnt_doc=None, child_doc=None):
    """ Merge two numpy-style docstrings into a single docstring, according to napoleon docstring sections.

        Given the numpy-style docstrings from a parent and child's attributes, merge the docstring
        sections such that the child's section is used, wherever present, otherwise the parent's
        section is used.

        Any whitespace that can be uniformly removed from a docstring's second line and onwards is
        removed. Sections will be separated by a single blank line.

        Parameters
        ----------
        prnt_doc: Optional[str]
            The docstring from the parent.
        child_doc: Optional[str]
            The docstring from the child.

        Returns
        -------
        Union[str, None]
            The merged docstring. """
    merge_all_sections(parse_napoleon_doc(prnt_doc, "numpy"), parse_napoleon_doc(child_doc, "numpy"))


def merge_google_napoleon_docs(prnt_doc=None, child_doc=None):
    """ Merge two google-style docstrings into a single docstring, according to napoleon docstring sections.

        Given the google-style docstrings from a parent and child's attributes, merge the docstring
        sections such that the child's section is used, wherever present, otherwise the parent's
        section is used.

        Any whitespace that can be uniformly removed from a docstring's second line and onwards is
        removed. Sections will be separated by a single blank line.

        Parameters
        ----------
        prnt_doc: Optional[str]
            The docstring from the parent.
        child_doc: Optional[str]
            The docstring from the child.

        Returns
        -------
        Union[str, None]
            The merged docstring. """
    merge_all_sections(parse_napoleon_doc(prnt_doc, "google"), parse_napoleon_doc(child_doc, "google"))
