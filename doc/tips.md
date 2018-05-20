# Tips for the Implementation

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
