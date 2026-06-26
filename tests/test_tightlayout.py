import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.testing.decorators import image_comparison

import mpltern

mpl_version = tuple(int(_) for _ in mpl.__version__.split('.'))
tol = 20.0 if mpl_version >= (3, 11) else 0.0


@image_comparison(["tight_layout1"], extensions=["pdf"], tol=tol, style="mpl20")
def test_tight_layout1():
    plt.rcParams['text.kerning_factor'] = 6

    fig = plt.figure(tight_layout=True)
    ax = fig.add_subplot(projection="ternary")
    ax.set_title("Title")
    ax.set_tlabel("Top" * 3)
    ax.set_llabel("Left" * 3)
    ax.set_rlabel("Right" * 3)
