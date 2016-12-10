### 2.0.2
- custom_inherit.store no longer inherits from `dict`. Fixes bug in which `store.update` could be used
to circumvent the type-checking that the store enforces.

### 2.0.1
- Numpy-style section delimiters was fixed so that they are the appropriate length, and thus compatible with the numpy-style for sphinx.

- `doc_inherit` was refactored so that the signature of the decorated  function is now preserved in Python(< 3.4). This was not an issue for newer versions of Python.

### 2.0.0
- A decorator, `doc_inherit` is now available for mediating docstring inheritance for a single function/method.property/etc.

- inheritance style functions can now be supplied directly to `style` arguments.

- Styles are now all managed through `custom_inherit.store`

- It is no longer necessary for users to implement styles by subclassing base inheritance classes from this package.

### 1.1.0
- Users no longer need to write a separate abstract base class version of their custom styles. This is now built on the fly within `DocInheritMeta`.

- Styles need only be logged in `custom_inherit.style_store.__all__` for the style to become available for use.

- The "numpy" inheritance style was updated to accommodate for situations in which method docstrings contain both "Raises" and "Returns"/"Yields" sections. 
