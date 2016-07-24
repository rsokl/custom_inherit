### 1.1.0
- Users no longer need to write a separate abstract base class version of their custom styles. This is now built on the fly within `DocInheritMeta`.

- Styles need only be logged in `custom_inherit.style_store.__all__` for the style to become available for use.

- The "numpy" inheritance style was updated to accommodate for situations in which method docstrings contain both "Raises" and "Returns"/"Yields" sections. 