"""Copyed from matplotlib 3.1.1"""


def _check_in_list(values, **kwargs):
    """
    For each *key, value* pair in *kwargs*, check that *value* is in *_values*;
    if not, raise an appropriate ValueError.

    Examples
    --------
    >>> cbook._check_in_list(["foo", "bar"], arg=arg, other_arg=other_arg)
    """
    for k, v in kwargs.items():
        if v not in values:
            raise ValueError(
                "{!r} is not a valid value for {}; supported values are {}"
                .format(v, k, ', '.join(map(repr, values))))
