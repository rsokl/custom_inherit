"""This module handles sections with items."""

import inspect
import re
from collections import OrderedDict

try:
    from textwrap import indent
except ImportError:
    # for Python < 3.3
    def indent(text, padding):
        return "".join(padding + line for line in text.splitlines(True))

try:
    from inspect import getfullargspec
except ImportError:
    # for python 2.7
    from inspect import getargspec as getfullargspec


_RE_PATTERN_ITEMS = re.compile(r"(\**\w+)(.*?)(?:$|(?=\n\**\w+))", flags=re.DOTALL)

_STYLE_TO_PADDING = {
    "numpy": "",
    "google": " " * 4,
}

_ARGS_SECTION_NAMES = {
    "Parameters",
    "Other Parameters",
    "Args",
    "Arguments",
}

SECTION_NAMES = _ARGS_SECTION_NAMES | {
    "Attributes",
    "Methods",
    "Keyword Args",
    "Keyword Arguments",
}


def _render(body, style):
    """Render the items of a section.

    Parameters
    ----------
    body: OrderedDict[str, Optional[str]]
        The items of a section.
    style: str
        The doc style.

    Returns
    -------
    str
    """
    padding = _STYLE_TO_PADDING[style]
    section = []
    for key, value in body.items():
        section += [indent("{}{}".format(key, value), padding)]
    return "\n".join(section)


def set_defaults(doc_sections):
    """Set the defaults for the sections with items in place.

    Parameters
    ----------
    doc_sections: OrderedDict[str, Optional[str]]
    """
    for section_name in SECTION_NAMES:
        doc_sections[section_name] = OrderedDict()


def parse(doc_sections):
    """Parse the sections with items in place.

    Parameters
    ----------
    doc_sections: OrderedDict[str, Optional[str]]
    """
    for section_name in SECTION_NAMES:
        section_content = doc_sections[section_name]
        if section_content:
            doc_sections[section_name] = OrderedDict(
                _RE_PATTERN_ITEMS.findall(inspect.cleandoc(section_content))
            )


def merge(child_func, section_name, prnt_sec, child_sec, merge_within_sections, style):
    """Merge the doc-sections of the parent's and child's attribute with items.

    Parameters
    ----------
    child_func: FunctionType
        The child function which doc is being merged.
    prnt_sec: OrderedDict[str, str]
    child_sec: OrderedDict[str, str]
    merge_within_sections: bool
        Wheter to merge the items.
    style: str
        The doc style.

    Returns
    -------
    OrderedDict[str, str]
        The merged items.
    """
    if merge_within_sections:
        body = prnt_sec.copy()
        body.update(child_sec)
    else:
        body = prnt_sec if not child_sec else child_sec

    if section_name in _ARGS_SECTION_NAMES:
        args, varargs, varkw = getfullargspec(child_func)[:3]

        if "self" in args:
            args.remove("self")

        all_args = set(args)

        for number, other_args in enumerate((varargs, varkw)):
            if other_args is not None:
                all_args.add("{}{}".format("*"*(number+1), other_args))

        # Remove the documented arguments that are not actual arguments.
        for arg in set(body) - all_args:
            del body[arg]

    body = _render(body, style)
    return body
