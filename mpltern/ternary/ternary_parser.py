import numpy as np

import matplotlib as mpl


def _get_xy(ax, this, trans):
    t, l, r = this
    tlr = np.column_stack((t, l, r))
    if trans == ax.transTernaryAxes:
        trans_xy = ax.transAxes
        x, y = ax.transAxesProjection.transform(tlr).T
    else:
        trans_xy = ax.transData
        x, y = ax.transProjection.transform(tlr).T
    return x, y, trans_xy


def _parse_ternary_single(f):
    """
    Parse ternary data from the first 3 arguments.
    """
    def parse(ax, *args, **kwargs):
        trans = kwargs.pop('transform', None)
        # If no `args` are given, return an empty list like Matplotlib
        # by calling the superclass method via `f`.
        if not args or (trans is not None and trans.input_dims == 2):
            kwargs['transform'] = trans
            return f(ax, *args, **kwargs)
        else:
            this, args = args[:3], args[3:]
            x, y, kwargs['transform'] = _get_xy(ax, this, trans)
            args = (x, y, *args)
            return f(ax, *args, **kwargs)

    return parse


def _parse_ternary_multiple(f):
    """
    Parse ternary data from each set of 3 (or 4 for format strings) arguments.
    """
    def move_data_to_args(*args, **kwargs):
        # Process the 'data' kwarg.
        data = kwargs.pop("data", None)
        if data is not None:
            args = [mpl._replacer(data, arg) for arg in args]
            # Ternary data w/ or w/o a format string
            if len(args) not in [3, 4]:
                raise ValueError(
                    "The number of positional arguments with data must be "
                    "3 or 4 in Mpltern due to ambiguity of arguments; use "
                    "multiple plotting calls instead")
        return args, kwargs

    def parse(ax, *args, **kwargs):
        trans = kwargs.pop('transform', None)
        # If no `args` are given, return an empty list like Matplotlib
        # by calling the superclass method via `f`.
        if not args or (trans is not None and trans.input_dims == 2):
            kwargs['transform'] = trans
            return f(ax, *args, **kwargs)
        else:
            args, kwargs = move_data_to_args(*args, **kwargs)

            # Repeatedly grab (t, l, r) or (t, l, r, format) from the front of
            # args and convert it to (x, y) or (x, y, format)
            replaced = ()
            while args:
                this, args = args[:3], args[3:]
                x, y, kwargs['transform'] = _get_xy(ax, this, trans)
                replaced += (x, y)
                if args and isinstance(args[0], str):
                    replaced += args[0],  # Format string
                    args = args[1:]
            args = replaced
            return f(ax, *args, **kwargs)

    return parse


def _parse_ternary_vector(f):
    """
    Parse ternary data from the first 6 arguments.
    """
    def parse(ax, *args, **kwargs):
        trans = kwargs.pop('transform', None)
        # If no `args` are given, return an empty list like Matplotlib
        # by calling the superclass method via `f`.
        if not args or (trans is not None and trans.input_dims == 2):
            kwargs['transform'] = trans
            return f(ax, *args, **kwargs)
        else:
            tlr0, args = args[:3], args[3:]
            tlr1, args = args[:3], args[3:]
            tlr0 = np.asarray(tlr0)
            tlr1 = np.asarray(tlr1)
            tlr1 += tlr0
            x0, y0, kwargs['transform'] = _get_xy(ax, tlr0, trans)
            x1, y1, kwargs['transform'] = _get_xy(ax, tlr1, trans)
            dx = x1 - x0
            dy = y1 - y0
            args = (x0.item(), y0.item(), dx.item(), dy.item(), *args)
            return f(ax, *args, **kwargs)

    return parse


def _parse_ternary_vector_field(f):
    """
    Parse ternary data from the first 6 arguments.
    """
    def parse(ax, *args, **kwargs):
        trans = kwargs.pop('transform', None)
        # If no `args` are given, return an empty list like Matplotlib
        # by calling the superclass method via `f`.
        if not args or (trans is not None and trans.input_dims == 2):
            kwargs['transform'] = trans
            return f(ax, *args, **kwargs)
        else:
            tlr0, args = args[:3], args[3:]
            tlr1, args = args[:3], args[3:]
            tlr0 = np.asarray(tlr0)
            tlr1 = np.asarray(tlr1)
            tlr1 += tlr0
            x0, y0, kwargs['transform'] = _get_xy(ax, tlr0, trans)
            x1, y1, kwargs['transform'] = _get_xy(ax, tlr1, trans)
            dx = x1 - x0
            dy = y1 - y0
            args = (x0, y0, dx, dy, *args)
            return f(ax, *args, **kwargs)

    return parse
