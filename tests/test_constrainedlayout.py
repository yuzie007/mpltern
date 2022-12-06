import matplotlib.pyplot as plt
from matplotlib.testing.decorators import image_comparison

import mpltern


@image_comparison(["constrained_layout1"], extensions=["pdf"], style="mpl20")
def test_constrained_layout1():
    plt.rcParams['text.kerning_factor'] = 6

    fig = plt.figure(constrained_layout=True)
    ax = fig.add_subplot(projection="ternary")
    ax.set_title("Title")
    ax.set_tlabel("Top" * 3)
    ax.set_llabel("Left" * 3)
    ax.set_rlabel("Right" * 3)
