from __future__ import absolute_import

from collections import OrderedDict
from inspect import cleandoc

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

    napoleon_sections = [
        "Short Summary",
        "Attributes",
        "Methods",
        "Warning",
        "Note",
        "Parameters",
        "Other Parameters",
        "Keyword Arguments",
        "Returns",
        "Yields",
        "Raises",
        "Warns",
        "See Also",
        "References",
        "Todo",
        "Example",
        "Examples",
    ]

    aliases = {
        "Args": "Parameters",
        "Arguments": "Parameters",
        "Keyword Args": "Keyword Arguments",
        "Return": "Returns",
        "Warnings": "Warning",
        "Yield": "Yields",
    }

    doc_sections = OrderedDict([(key, None) for key in napoleon_sections])

    if not doc:
        return doc_sections

    assert style in ("google", "numpy")

    doc = cleandoc(doc)
    lines = iter(doc.splitlines())

    key = "Short Summary"
    body = []
    while True:
        try:
            line = next(lines).rstrip()
            header = (
                line
                if style == "numpy"
                else (line[:-1] if line.endswith(":") else line)
            )
            if header and (header in doc_sections or header in aliases):
                doc_sections[aliases.get(key, key)] = (
                    "\n".join(body).rstrip() if body else None
                )
                body = []
                key = header
                if style == "numpy":
                    next(lines)  # skip section delimiter
            else:
                body.append(line)
        except StopIteration:
            doc_sections[aliases.get(key, key)] = "\n".join(body)
            break
    return doc_sections


def merge_section(key, prnt_sec, child_sec, style, merge_within_sections=False):
    """ Synthesize a output napoleon docstring section.

    Parameters
    ----------
    key: str
        The napoleon-section being merged.
    prnt_sec: Optional[str]
        The docstring section from the parent's attribute.
    child_sec: Optional[str]
        The docstring section from the child's attribute.
    Returns
    -------
    Optional[str]
        The output docstring section."""

    napoleon_sections_that_cant_merge = [
        "Short Summary",
        "Example",
        "Examples",
    ]

    if prnt_sec is None and child_sec is None:
        return None

    assert style in ("google", "numpy")

    if key == "Short Summary":
        header = ""
    else:
        if style == "numpy":
            header = "\n".join((key, "".join("-" for i in range(len(key))), ""))
        else:
            header = "\n".join((key + ":", ""))
    if merge_within_sections and key not in napoleon_sections_that_cant_merge:
        if child_sec is None:
            body = prnt_sec
        elif prnt_sec is None:
            body = child_sec
        else:
            body = '\n'.join((prnt_sec, child_sec))
    else:
        body = prnt_sec if child_sec is None else child_sec

    return header + body


def merge_all_sections(prnt_sctns, child_sctns, style, merge_within_sections=False):
    """ Merge the doc-sections of the parent's and child's attribute into a single docstring.

    Parameters
    ----------
    prnt_sctns: OrderedDict[str, Union[None,str]]
    child_sctns: OrderedDict[str, Union[None,str]]

    Returns
    -------
    str
        Output docstring of the merged docstrings."""
    doc = []

    prnt_only_raises = prnt_sctns["Raises"] and not (
        prnt_sctns["Returns"] or prnt_sctns["Yields"]
    )
    if prnt_only_raises and (child_sctns["Returns"] or child_sctns["Yields"]):
        prnt_sctns["Raises"] = None

    for key in prnt_sctns:
        sect = merge_section(
            key,
            prnt_sctns[key],
            child_sctns[key],
            style,
            merge_within_sections=merge_within_sections
        )
        if sect is not None:
            doc.append(sect)
    return "\n\n".join(doc) if doc else None


def merge_numpy_napoleon_docs(prnt_doc=None, child_doc=None, merge_within_sections=False):
    """ Merge two numpy-style docstrings into a single docstring, according to napoleon docstring sections.

    Given the numpy-style docstrings from a parent and child's attributes, merge the docstring
    sections such that the child's section is used, wherever present, otherwise the parent's
    section is used.

    Any whitespace that can be uniformly removed from a docstring's second line and onwards is
    removed. Sections will be separated by a single blank line.

    Aliased docstring sections are normalized. E.g Args, Arguments -> Parameters

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
    style = "numpy"
    return merge_all_sections(
        parse_napoleon_doc(prnt_doc, style),
        parse_napoleon_doc(child_doc, style),
        style,
        merge_within_sections=merge_within_sections
    )


def merge_google_napoleon_docs(prnt_doc=None, child_doc=None, merge_within_sections=False):
    """ Merge two google-style docstrings into a single docstring, according to napoleon docstring sections.

        Given the google-style docstrings from a parent and child's attributes, merge the docstring
    sections such that the child's section is used, wherever present, otherwise the parent's
    section is used.

    Any whitespace that can be uniformly removed from a docstring's second line and onwards is
    removed. Sections will be separated by a single blank line.

    Aliased docstring sections are normalized. E.g Args, Arguments -> Parameters

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
    style = "google"
    return merge_all_sections(
        parse_napoleon_doc(prnt_doc, style),
        parse_napoleon_doc(child_doc, style),
        style,
        merge_within_sections=merge_within_sections
    )
