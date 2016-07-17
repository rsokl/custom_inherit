from collections import OrderedDict
import inspect

__all__ = ["merge_numpy_docs"]

def parse_numpy_doc(doc):
    """ Extract the text from the various sections of a numpy-formatted docstring

        Parameters
        ----------
        doc: Union[str, None]

        Returns
        -------
        Union[str, None]"""

    doc_sections = OrderedDict([("Short Summary", None),
                                ("Deprecation Warning", None),
                                ("Parameters", None),
                                ("Attributes", None),
                                ("Extended Summary", None),
                                ("Parameters", None),
                                ("Returns", None),
                                ("Yields", None),
                                ("Other Parameters", None),
                                ("Raises", None),
                                ("See Also", None),
                                ("Notes", None),
                                ("References", None),
                                ("Examples", None)])

    if doc is None:
        return doc_sections

    doc = inspect.cleandoc(doc)
    lines = iter(doc.splitlines())

    key = "Short Summary"
    body = []
    while True:
        try:
            line = next(lines)
            if line in doc_sections:
                doc_sections[key] = "\n".join(body).rstrip() if body else None
                body = []
                key = line
                next(lines)  # skip section delimiter
            else:
                body.append(line)
        except StopIteration:
            doc_sections[key] = "\n".join(body)
            break

    return doc_sections


def merge_section(key, prnt_sec, child_sec):
    """ Parameters
        ----------
        key: str
        prnt_sec: Union[str, None]
        child_sec: Union[str, None]

        Returns
        -------
        str"""
    if prnt_sec is None and child_sec is None:
        return None

    if key == "Short Summary":
        header = ''
    else:
        header = "\n".join((key, "-".join("" for i in range(len(key))), ""))

    if prnt_sec is None:
        body = child_sec
    elif child_sec is None:
        body = prnt_sec
    else:
        body = child_sec

    return header + body


def merge_doc_sections(prnt_sctns, child_sctns):
    """ Parameters
        ----------
        prnt_sctns: OrderedDict[str, str]
        child_sctns: OrderedDict[str, str]

        Returns
        -------
        str"""
    doc = []
    for key in prnt_sctns:
        sect = merge_section(key, prnt_sctns[key], child_sctns[key])
        if sect is not None:
            doc.append(sect)
    return "\n\n".join(doc) if doc else None


def merge_numpy_docs(prnt_doc, child_doc):
    return merge_doc_sections(parse_numpy_doc(prnt_doc), parse_numpy_doc(child_doc))