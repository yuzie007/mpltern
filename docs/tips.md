# Tips for the Implementation

## Aim of Taxes

- To use rcParams rather than hard-coded defaults

## Convention in `taxes`

The discussion
[here](https://github.com/marcharper/python-ternary/issues/13)
and
[here](https://github.com/marcharper/python-ternary/issues/18)
may be helpful to understand.

So saying "clockwise" or "counterclockwise" may be not meaningful very much,
because this is essentially just which side the ticks are given for each
ternary axis.

The "permutation" option is NOT planned, because this is what users can easily
manipulate outside `taxes`.
It is something like that you tell Matplotlib to make the option to permute
`x` and `y` for, e.g., the `plot` method, which may not be necessary for most
of the users.

In the vertex-based perspective, existing codes for ternary plots give the
following orders by default:

|Code           |Order of vertices           |
|---------------|----------------------------|
|Plotly         |`T, L, R` (counterclockwise)|
|python-ternary |`R, T, L` (counterclockwise)|
|ggtern         |`L, R, T` (counterclockwise)|
|Ternary        |`T, R, L` (clockwise)       |
|d3-ternary     |`L, R, T` (counterclockwise)|
|PGFPlots       |`T, L, R` (counterclockwise)|
|Venus          |`R, L, T` (clockwise)       |
|ternaryplot.com|`T, L, R` (counterclockwise)|
|JMP            |`L, T, R` (clockwise)       |
|Origin         |`R, T, L` (counterclockwise)|
|Statgraphics   |`T, L, R` (counterclockwise)|

As found, the conterclockwise progress starting from `T` is the most common
for the order of triangle vertices.
(Do not be confused with "conterclockwise" *for ticks* noted above.)
Therefore, `taxes` also follows the most common convention.

## AxesSubplot

`AxesSubplot`などのclassは，静的に定義されているのではなく，
`axes/_subplots.subplot_class_factory`で動的に生成されている．

In Taxes, I define `TernaryAxes` without the suffix `Subplot`.

## Axis

### Label Positions

For the LAxis label, for instance, I would like to put its label at $y = 0.5$
in the `axes` coorindates.
To avoid the overlap with ticklabels, I applied the following way in
`_update_label_position`.

The label should be along the line of $x$ and $y$ with the slope $a$ of 2
in the `axes` coordinates.
The label line should also avoid the overlap with ticklabels, the line should
avoid each `bbox` (x0, y1) of the ticks.

$$
y = a x + b
$$

$$
\tilde{y} = a \tilde{x} + b
$$

Now the 'reference' $\tilde{y}$ is 0.5 (in the `axes` coordinates), while what we want to get is
the corresponding $\tilde{x}$.
By giving the `bbox` (x0, x1) of the ticks to the equation $y = ax + b$,
we can obtain a candidate $\tilde{x}$ as

$$
\tilde{x} = x - \frac{y - \tilde{y}}{a}
$$

Then finally we take the leftmost `x0` and adopt it as the label position.

## Tick

### Markers

matplotlibでは，ticksはTickオブジェクトのリストとして定義されている．ひとつのTickはひとつのtick pointに対応し，tickを示すためのmarkerをもつLines2D, その点に対応するlabel, そしてgridを持つ．

tickはmarkerで示される．傾きをもったtickを示すために，taxesではtupleを利用している．具体的には，in, outの場合は１つの頂点を持ったasteriskとして，inoutの場合は２つの頂点として定義している．

ただし，tupleで作ったmarkerは自動的に大きさが0.5にscaleされてしまう．
一方で，matplotlib defaultのmarkerは，in, outが1, inoutが0.5の大きさを持つ．
`self._size`を保持しつつ`self._tickdir`に応じて適切にmarkersizeをscaleするため，`_get_tick1line`で`scale`を定義して対応している．

### Remove Round-off

We need to define `_get_pixel_distance_along_axis` in e.g. `BAxis`.

## TernaryTick

- Tickから継承できるもの
    - `get_tick_padding`
    - `get_children`
- To be overridden
    - `_get_tick1line`
        - transformをdata coordinateにする必要がある
    - `get_tick2line`
    - `draw`
        - `tick2line.draw`をoffにする
    - `update_position`
        - tickの傾きなどに応じて．．．

## TernaryAxis

- To be ovrerridden
    - `update_label_position`
        - Tickは_update_positionで位置を更新している．

## BAxis, RAxis, LAxis

- To be overridden
    - `_get_label`
        - The default rotation as well as rotation_mode should be overridden
          depending on the axis type.

## Offset Text

例えばy軸の値が非常に大きい場合，matplotlibはある基準点を自動で求めて，そこからの変分をy軸として示すことがある．その時の基準点を示すtextのこと．

Corner labelsを導入する時に利用できるかもしれない．

## fig.colorbar

`fig.colorbar`において，colorbarの位置はylabelを考慮していない．
fraction, padが位置を決める．

## Interactive mode

The buttons in the interactive mode call the following methods:
- `Home` calls `_set_view`
- `Pan/Zoom` calls `drag_pan`
- `Zoom-to-rectangle` calls `_set_view_from_bbox`

So, e.g., if you want to scale the axes for ternary plots according to the
change of (`xmin`, `ymin`, `xmax`, `ymax`), you need to override these methods
to additionally call the rescaling method for the axes for ternary
plots (`_set_ternary_lim_from_xlim_and_ylim`).

If you want to prohibit e.g. `Zoom-to-rectanble`, you need to override e.g.
`can_zoom` to return `False`. (`PolarAxes` does this.)
