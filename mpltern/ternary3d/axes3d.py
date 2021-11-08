from mpl_toolkits.mplot3d.axes3d import Axes3D


class TernaryAxes3D(Axes3D):
    name = 'ternary3d'

    def __init__(self, *args, ternary_sum: float = 1.0, **kwargs):
        """3D ternary axes object.

        Parameters
        ----------
        ternary_sum : float, optional
            Constant to which ``t + l + r`` is normalized, by default 1.0
        """
        # Since Matplotlib 3.5.0, `auto_add_to_figure` is "deprecated" but
        # actually causes an error if it is `True`.
        # To avoid this we set `False` to this argument.
        # Since Matplotlib 3.6.0, `auto_add_to_figure` is not necessary to set.
        kwargs.setdefault('auto_add_to_figure', False)
        self.ternary_lim = ternary_sum
        super().__init__(*args, **kwargs)
