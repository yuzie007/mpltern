# Tips for the Implementation

## Aim of Taxes

- To use rcParams rather than hard-coded defaults

## Convention in `taxes`

In a ternary plot, three variables which sum to a constant (`S`) 
```t + l + r = S (= 1 in taxes by default)``` is projected onto a
two-dimensional triangle.
Each variable is associated with each corner of the triangle, and the scaled
distance to the corner from its opposite side.

There may be two kinds of perspectives to read a ternary plot; the
"corner-based" and the "side-based" perspectives.
The `taxes` code adopts the "corner-based" perspective.
In this perspective, each of the three variables is associated with a corner of
the triangle, and the position in the triangle is given as the scaled distance
to the corner from its opposite side, as already written above.
In `taxes`, the order of the variables is `T (top) → L (left) → R (right)`
(counterclockwise).

In `taxes`, by default, the ticks are shown to the left side of the triangle
with seeing the corresponding corner upward.
You can put the ticks to the opposite sides by `ax.opposite_ticks(True)`.
Notice that, although the tick positions are changed, still a point in the
triangle corresponds to the same composition.

![](corner_based_1.svg)

![](corner_based_2.svg)

Some people read a ternary plot with the "side-based" perspective like the
figure below. In this perspective, we must also specify if the ticks proceed
in a clockwise or a counterclockwise manner.
*Be careful that a point in the triangle corresponds to different compositions
between the clockwise and the counterclockwise manners*, which could be
confusing.
This also means a position for a side does not immediately associated with the
value of the corresponding variable in the "side-based" perspective.
In `taxes`, therefore, the "corner-based" perspective is adopted.

![](side_based_ccw.svg)

![](side_based_cw.svg)

The discussion
[here](https://github.com/marcharper/python-ternary/issues/13)
and
[here](https://github.com/marcharper/python-ternary/issues/18)
may be also helpful to understand.

## Convention in other software

In the corner-based perspective, [existing codes](alternatives.md) for ternary
plots give the following orders by default:

|Code           |Order of triangle corners|Ticks    |
|---------------|-------------------------|---------|
|Plotly         |`T → L → R` (CCW)        |CW       |
|python-ternary |`R → T → L` (CCW)        |CCW      |
|ggtern         |`L → R → T` (CCW)        |CCW      |
|Ternary (R)    |`T → R → L` (CW)         |CW       |
|d3-ternary     |`L → R → T` (CCW)        |CW       |
|PGFPlots       |`T → L → R` (CCW)        |CCW      |
|Veusz          |`R → L → T` (CW)         |CCW      |
|ternaryplot.com|`T → L → R` (CCW)        |CW       |
|JMP            |`L → T → R` (CW)         |CW       |
|Origin         |`R → T → L` (CCW)        |CCW      |
|Statgraphics   |`T → L → R` (CCW)        |CCW      |

As found, the majority is

- `T → L → R` (CCW) for the order of triangle corners
- CCW for the ticks progress

The `taxes` code decides to follow this convention.

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
