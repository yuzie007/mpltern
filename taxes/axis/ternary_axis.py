from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from matplotlib.axis import XAxis


class TernaryAxis(XAxis):
    def __init__(self, taxes, pickradius=15):
        self.taxes = taxes
        axes = self.taxes.get_axes()
        super(TernaryAxis, self).__init__(axes, pickradius)
