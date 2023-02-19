"""
======================
Dirichlet distribution
======================
"""
import matplotlib.pyplot as plt
from mpltern.datasets import get_dirichlet_pdfs

fig = plt.figure(figsize=(10.8, 8.8))
fig.subplots_adjust(
    left=0.1,
    right=0.9,
    bottom=0.1,
    top=0.9,
    wspace=0.5,
    hspace=0.5,
)

alphas = ((1.5, 1.5, 1.5), (5.0, 5.0, 5.0), (1.0, 2.0, 2.0), (2.0, 4.0, 8.0))
for i, alpha in enumerate(alphas):
    ax = fig.add_subplot(2, 2, i + 1, projection="ternary")
    t, l, r, v = get_dirichlet_pdfs(n=61, alpha=alpha)
    cmap = "Blues"
    shading = "gouraud"
    cs = ax.tripcolor(t, l, r, v, cmap=cmap, shading=shading, rasterized=True)
    ax.tricontour(t, l, r, v, colors="k", linewidths=0.5)

    ax.set_tlabel("$x_1$")
    ax.set_llabel("$x_2$")
    ax.set_rlabel("$x_3$")

    ax.taxis.set_label_position("tick1")
    ax.laxis.set_label_position("tick1")
    ax.raxis.set_label_position("tick1")

    ax.set_title("${\\mathbf{\\alpha}}$ = " + str(alpha))

    cax = ax.inset_axes([1.05, 0.1, 0.05, 0.9], transform=ax.transAxes)
    colorbar = fig.colorbar(cs, cax=cax)
    colorbar.set_label("PDF", rotation=270, va="baseline")

plt.show()
