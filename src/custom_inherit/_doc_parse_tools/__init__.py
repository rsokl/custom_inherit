from __future__ import absolute_import

from .napoleon_parse_tools import (merge_google_napoleon_docs,
                                   merge_numpy_napoleon_docs)
from .numpy_parse_tools import merge_numpy_docs
from .rest_parse_tools import merge_rest_docs

__all__ = [
    "merge_numpy_docs",
    "merge_rest_docs",
    "merge_numpy_napoleon_docs",
    "merge_google_napoleon_docs",
]
