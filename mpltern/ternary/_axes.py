import numpy as np

import matplotlib.cbook as cbook
import matplotlib.collections as mcoll
import matplotlib.colors as mcolors
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import matplotlib.transforms as mtransforms
from matplotlib import _api
from mpltern._ternary_parsers import (
    parse_ternary_single,
    parse_ternary_multiple,
    parse_ternary_vector,
)
from mpltern import hexbin_helpers
from mpltern import tribin_helpers
from mpltern.ternary._base import TernaryAxesBase


class TernaryAxes(TernaryAxesBase):
    """
    A ternary graph projection, where the input dimensions are *t*, *l*, *r*.
    The plot starts from the top and goes anti-clockwise.
    """
    name = 'ternary'

    text = parse_ternary_single(TernaryAxesBase.text)

    def axtline(self, x=0, ymin=0, ymax=1, **kwargs):
        """
        Add a equi-t line across the axes.

        Parameters
        ----------
        x : float, default: 0
            x position in data coordinates of the equi-t line.

        ymin : float, default: 0
            Should be between 0 and 1, 0 being one end of the plot, 1 the
            other of the plot.

        ymax : float, default: 1
            Should be between 0 and 1, 0 being one end of the plot, 1 the
            other of the plot.

        Returns
        -------
        `~matplotlib.lines.Line2D`

        Other Parameters
        ----------------
        **kwargs
            Valid keyword arguments are `.Line2D` properties, except for
            'transform':

            %(Line2D:kwdoc)s

        See Also
        --------
        axtspan : Add a equi-t span across the axis.
        """
        if "transform" in kwargs:
            raise ValueError(
                "'transform' is not allowed as a kwarg;"
                + "axtline generates its own transform.")
        trans = self.get_taxis_transform(which='grid')
        l = mlines.Line2D([x, x], [ymin, ymax], transform=trans, **kwargs)
        self.add_line(l)
        return l

    def axlline(self, x=0, ymin=0, ymax=1, **kwargs):
        """
        Add a equi-l line across the axes.

        Parameters
        ----------
        x : float, default: 0
            x position in data coordinates of the equi-l line.

        ymin : float, default: 0
            Should be between 0 and 1, 0 being one end of the plot, 1 the
            other of the plot.

        ymax : float, default: 1
            Should be between 0 and 1, 0 being one end of the plot, 1 the
            other of the plot.

        Returns
        -------
        `~matplotlib.lines.Line2D`

        Other Parameters
        ----------------
        **kwargs
            Valid keyword arguments are `.Line2D` properties, except for
            'transform':

            %(Line2D:kwdoc)s

        See Also
        --------
        axlspan : Add a equi-l span across the axis.
        """
        if "transform" in kwargs:
            raise ValueError(
                "'transform' is not allowed as a kwarg;"
                + "axlline generates its own transform.")
        trans = self.get_laxis_transform(which='grid')
        l = mlines.Line2D([x, x], [ymin, ymax], transform=trans, **kwargs)
        self.add_line(l)
        return l

    def axrline(self, x=0, ymin=0, ymax=1, **kwargs):
        """
        Add a equi-r line across the axes.

        Parameters
        ----------
        x : float, default: 0
            x position in data coordinates of the equi-r line.

        ymin : float, default: 0
            Should be between 0 and 1, 0 being one end of the plot, 1 the
            other of the plot.

        ymax : float, default: 1
            Should be between 0 and 1, 0 being one end of the plot, 1 the
            other of the plot.

        Returns
        -------
        `~matplotlib.lines.Line2D`

        Other Parameters
        ----------------
        **kwargs
            Valid keyword arguments are `.Line2D` properties, except for
            'transform':

            %(Line2D:kwdoc)s

        See Also
        --------
        axrspan : Add a equi-r span across the axis.
        """
        if "transform" in kwargs:
            raise ValueError(
                "'transform' is not allowed as a kwarg;"
                + "axrline generates its own transform.")
        trans = self.get_raxis_transform(which='grid')
        l = mlines.Line2D([x, x], [ymin, ymax], transform=trans, **kwargs)
        self.add_line(l)
        return l

    def axline(self, xy1, xy2=None, *, slope=None, **kwargs):
        k = 'transform'
        if k in kwargs and kwargs[k].input_dims == 2:
            return super().axline(xy1, xy2, slope=slope, **kwargs)

        if k in kwargs and kwargs[k] == self.transTernaryAxes:
            trans = self.transAxesProjection
            trans_xy = self.transAxes
        else:
            trans = self.transProjection
            trans_xy = None

        tlr1 = xy1
        tlr2 = xy2

        xy1 = trans.transform(tlr1)
        if xy2 is not None:
            xy2 = trans.transform(tlr2)
        if slope is not None:
            slope = np.asarray(slope)
            if slope.size != 3:
                raise ValueError("'slope' must be of length 3")
            xy3 = trans.transform(tlr1 + np.asarray(slope))
            dx = xy3[0] - xy1[0]
            dy = xy3[1] - xy1[1]
            if np.allclose(dx, 0.0):
                slope = np.inf
            else:
                slope = dy / dx

        if k in kwargs:
            kwargs['transform'] = trans_xy

        return super().axline(xy1, xy2, slope=slope, **kwargs)

    def axtspan(self, xmin, xmax, ymin=0, ymax=1, **kwargs):
        """
        Add a span for the bottom coordinate.

        Parameters
        ----------
        xmin : float
               Lower limit of the top span in data units.
        xmax : float
               Upper limit of the top span in data units.
        ymin : float, optional, default: 0
               Lower limit of the span from end to end in relative
               (0-1) units.
        ymax : float, optional, default: 1
               Upper limit of the span from end to end in relative
               (0-1) units.

        Returns
        -------
        `~matplotlib.patches.Polygon`

        Other Parameters
        ----------------
        **kwargs : `~matplotlib.patches.Polygon` properties

        %(Polygon:kwdoc)s

        See Also
        --------
        axlspan : Add a span for the left coordinate.
        axrspan : Add a span for the right coordinate.
        """
        trans = self.get_taxis_transform(which='grid')
        verts = (xmin, ymin), (xmin, ymax), (xmax, ymax), (xmax, ymin)
        p = mpatches.Polygon(verts, **kwargs)
        p.set_transform(trans)
        self.add_patch(p)
        return p

    def axlspan(self, xmin, xmax, ymin=0, ymax=1, **kwargs):
        """
        Add a span for the left coordinate.

        Parameters
        ----------
        xmin : float
               Lower limit of the left span in data units.
        xmax : float
               Upper limit of the left span in data units.
        ymin : float, optional, default: 0
               Lower limit of the span from end to end in relative
               (0-1) units.
        ymax : float, optional, default: 1
               Upper limit of the span from end to end in relative
               (0-1) units.

        Returns
        -------
        `~matplotlib.patches.Polygon`

        Other Parameters
        ----------------
        **kwargs : `~matplotlib.patches.Polygon` properties

        %(Polygon:kwdoc)s

        See Also
        --------
        axtspan : Add a span for the top coordinate.
        axrspan : Add a span for the right coordinate.
        """
        trans = self.get_laxis_transform(which='grid')
        verts = (xmin, ymin), (xmin, ymax), (xmax, ymax), (xmax, ymin)
        p = mpatches.Polygon(verts, **kwargs)
        p.set_transform(trans)
        self.add_patch(p)
        return p

    def axrspan(self, xmin, xmax, ymin=0, ymax=1, **kwargs):
        """
        Add a span for the right coordinate.

        Parameters
        ----------
        xmin : float
               Lower limit of the right span in data units.
        xmax : float
               Upper limit of the right span in data units.
        ymin : float, optional, default: 0
               Lower limit of the span from end to end in relative
               (0-1) units.
        ymax : float, optional, default: 1
               Upper limit of the span from end to end in relative
               (0-1) units.

        Returns
        -------
        `~matplotlib.patches.Polygon`

        Other Parameters
        ----------------
        **kwargs : `~matplotlib.patches.Polygon` properties

        %(Polygon:kwdoc)s

        See Also
        --------
        axtspan : Add a span for the top coordinate.
        axlspan : Add a span for the left coordinate.
        """
        trans = self.get_raxis_transform(which='grid')
        verts = (xmin, ymin), (xmin, ymax), (xmax, ymax), (xmax, ymin)
        p = mpatches.Polygon(verts, **kwargs)
        p.set_transform(trans)
        self.add_patch(p)
        return p

    plot = parse_ternary_multiple(TernaryAxesBase.plot)
    scatter = parse_ternary_multiple(TernaryAxesBase.scatter)

    def hexbin(self, t, l, r, C=None, gridsize=100, bins=None,
               xscale='linear', yscale='linear', extent=None,
               cmap=None, norm=None, vmin=None, vmax=None,
               alpha=None, linewidths=None, edgecolors='face',
               reduce_C_function=np.mean, mincnt=None, marginals=False,
               **kwargs):
        """
        Make a 2D hexagonal binning plot of points *t*, *l*, *r*.

        If *C* is *None*, the value of the hexagon is determined by the number
        of points in the hexagon. Otherwise, *C* specifies values at the
        coordinate (t[i], l[i], r[i]).
        For each triangle, these values are reduced using *reduce_C_function*.

        Parameters
        ----------
        t, l, r : array-like
            The data positions. *t*, *l*, and *r* must be of the same length.

        C : array-like, optional
            If given, these values are accumulated in the bins. Otherwise,
            every point has a value of 1. Must be of the same length as *t*,
            *l*, and *r*.

        gridsize : int, default: 100
            Number of hexagons in one direction between min and max.
            In mpltern, all the three directions have the same gridsize.

        bins : 'log' or int or sequence, default: None
            Discretization of the hexagon values.

            - If *None*, no binning is applied; the color of each hexagon
              directly corresponds to its count value.
            - If 'log', use a logarithmic scale for the colormap.
              Internally, :math:`log_{10}(i+1)` is used to determine the
              hexagon color. This is equivalent to ``norm=LogNorm()``.
            - If an integer, divide the counts in the specified number
              of bins, and color the hexagons accordingly.
            - If a sequence of values, the values of the lower bound of
              the bins to be used.

        xscale : {'linear', 'log'}, default: 'linear'
            Ignored in mpltern and always linear scales on all three axes.

        yscale : {'linear', 'log'}, default: 'linear'
            Ignored in mpltern and always linear scales on all three axes.

        mincnt : int > 0, default: *None*
            If not *None*, only display cells with more than *mincnt*
            number of points in the cell.

        marginals : bool, default: *False*
            Ignored in mpltern.

        extent : 6-tuple of float, default: *None*
            The limits of the bins (tmin, tmax, lmin, lmax, rmin, rmax).
            The default assigns the limits based on *tlim*, *llim*, *rlim*.

        Returns
        -------
        `~matplotlib.collections.PolyCollection`
            A `.PolyCollection` defining the hexagonal bins.

            - `.PolyCollection.get_offsets` contains a Mx2 array containing
              the x, y positions of the M hexagon centers.
            - `.PolyCollection.get_array` contains the values of the M
              hexagons.

        Other Parameters
        ----------------
        %(cmap_doc)s

        %(norm_doc)s

        %(vmin_vmax_doc)s

        alpha : float between 0 and 1, optional
            The alpha blending value, between 0 (transparent) and 1 (opaque).

        linewidths : float, default: *None*
            If *None*, defaults to 1.0.

        edgecolors : {'face', 'none', *None*} or color, default: 'face'
            The color of the hexagon edges. Possible values are:

            - 'face': Draw the edges in the same color as the fill color.
            - 'none': No edges are drawn. This can sometimes lead to unsightly
              unpainted pixels between the hexagons.
            - *None*: Draw outlines in the default color.
            - An explicit color.

        reduce_C_function : callable, default: `numpy.mean`
            The function to aggregate *C* within the bins. It is ignored if
            *C* is not given. This must have the signature::

                def reduce_C_function(C: array) -> float

            Commonly used functions are:

            - `numpy.mean`: average of the points
            - `numpy.sum`: integral of the point values
            - `numpy.amax`: value taken from the largest point

        data : indexable object, optional
            DATA_PARAMETER_PLACEHOLDER

        **kwargs : `~matplotlib.collections.PolyCollection` properties
            All other keyword arguments are passed on to `.PolyCollection`:

            %(PolyCollection:kwdoc)s

        See Also
        --------
        tribin : 2D histogram triangular bins
        """
        self._process_unit_info(
            [("t", t), ("l", l), ("r", r)], kwargs, convert=False)

        t, l, r, C = cbook.delete_masked_points(t, l, r, C)

        # Count the number of data in each hexagon
        t = np.asarray(t, float)
        l = np.asarray(l, float)
        r = np.asarray(r, float)

        t, l, r = _normalize_tlr(t, l, r, self.ternary_sum)

        if extent is not None:
            tmin, tmax, lmin, lmax, rmin, rmax = extent
        else:
            tmin, tmax = self.get_tlim()
            lmin, lmax = self.get_llim()
            rmin, rmax = self.get_rlim()

        # number of hexagons
        n = (gridsize + 1) * (gridsize + 2) // 2

        st, sl, sr, it, il, ir = hexbin_helpers.calc_ternary_indices(
            t, l, r, gridsize, (tmin, tmax, lmin, lmax, rmin, rmax))

        # flat indices, plus one so that out-of-range points go to position 0.
        indices = hexbin_helpers.ternary_to_serial(gridsize, it, il, ir) + 1

        if C is None:  # [1:] drops out-of-range points.
            counts = np.bincount(indices, minlength=1 + n)[1:]
            accum = counts.astype(float)
            if mincnt is not None:
                accum[accum < mincnt] = np.nan
        else:
            # store the C values in a list per hexagon index
            Cs = [[] for _ in range(1 + n)]
            for i in range(len(C)):
                Cs[indices[i]].append(C[i])
            if mincnt is None:
                mincnt = 0
            accum = np.array(
                [reduce_C_function(acc) if len(acc) >= mincnt else np.nan
                 for acc in Cs[1:]],  # [1:] drops out-of-range points.
                float)

        good_idxs = ~np.isnan(accum)

        _ = hexbin_helpers.serial_to_ternary(gridsize, np.arange(n))
        offsets = np.array(_).T.astype(float)

        # remove accumulation bins with no data
        offsets = offsets[good_idxs, :]
        accum = accum[good_idxs]

        # scale into [0, 1]
        offsets /= gridsize

        # scale into the given extent
        offsets_c = 1.0 - offsets
        offsets[..., 0] = offsets_c[..., 0] * tmin + offsets[..., 0] * tmax
        offsets[..., 1] = offsets_c[..., 1] * lmin + offsets[..., 1] * lmax
        offsets[..., 2] = offsets_c[..., 2] * rmin + offsets[..., 2] * rmax

        polygon = [st, sl, sr] * np.array([
            [-1.0 / 3, -1.0 / 3, +2.0 / 3],
            [+1.0 / 3, -2.0 / 3, +1.0 / 3],
            [+2.0 / 3, -1.0 / 3, -1.0 / 3],
            [+1.0 / 3, +1.0 / 3, -2.0 / 3],
            [-1.0 / 3, +2.0 / 3, -1.0 / 3],
            [-2.0 / 3, +1.0 / 3, +1.0 / 3],
        ]) + (tmax, lmin, rmin)

        if linewidths is None:
            linewidths = [1.0]

        polygon = self.transProjection.transform(polygon)
        offsets = self.transProjection.transform(offsets)

        # shift the reference polygon at (tmax, lmin, rmin) to the origin
        polygon -= offsets[0]

        if True:
            # While `offset_transform` is introduced since `matplotlib>=3.6.0`,
            # here an alias `transOffset` is used for backword compatibility.
            # see matplotlib/matplotlib#21965
            collection = mcoll.PolyCollection(
                [polygon],
                edgecolors=edgecolors,
                linewidths=linewidths,
                offsets=offsets,
                transOffset=mtransforms.AffineDeltaTransform(self.transData),
            )

        # Set normalizer if bins is 'log'
        if bins == 'log':
            if norm is not None:
                _api.warn_external("Only one of 'bins' and 'norm' arguments "
                                   f"can be supplied, ignoring bins={bins}")
            else:
                norm = mcolors.LogNorm(vmin=vmin, vmax=vmax)
                vmin = vmax = None
            bins = None

        # autoscale the norm with current accum values if it hasn't been set
        if norm is not None:
            if norm.vmin is None and norm.vmax is None:
                norm.autoscale(accum)

        if bins is not None:
            if not np.iterable(bins):
                minimum, maximum = min(accum), max(accum)
                bins -= 1  # one less edge than bins
                bins = minimum + (maximum - minimum) * np.arange(bins) / bins
            bins = np.sort(bins)
            accum = bins.searchsorted(accum)

        collection.set_array(accum)
        collection.set_cmap(cmap)
        collection.set_norm(norm)
        collection.set_alpha(alpha)
        collection.update(kwargs)  # matplotlib/matplotlib#22451
        collection._scale_norm(norm, vmin, vmax)

        # add the collection last
        self.add_collection(collection, autolim=False)
        return collection

    def tribin(self, t, l, r, C=None, gridsize=100, bins=None,
               xscale='linear', yscale='linear', extent=None,
               cmap=None, norm=None, vmin=None, vmax=None,
               alpha=None, linewidths=None, edgecolors='face',
               reduce_C_function=np.mean, mincnt=None, marginals=False,
               **kwargs):
        """
        Make a 2D triangular binning plot of points *t*, *l*, *r*.

        If *C* is *None*, the value of the triangle is determined by the number
        of points in the triangle. Otherwise, *C* specifies values at the
        coordinate (t[i], l[i], r[i]).
        For each triangle, these values are reduced using *reduce_C_function*.

        Parameters
        ----------
        t, l, r : array-like
            The data positions. *t*, *l*, and *r* must be of the same length.

        C : array-like, optional
            If given, these values are accumulated in the bins. Otherwise,
            every point has a value of 1. Must be of the same length as *t*,
            *l*, and *r*.

        gridsize : int, default: 100
            Number of triangles in one direction between min and max.
            In mpltern, all the three directions have the same gridsize.

        bins : 'log' or int or sequence, default: None
            Discretization of the hexagon values.

            - If *None*, no binning is applied; the color of each triangle
              directly corresponds to its count value.
            - If 'log', use a logarithmic scale for the colormap.
              Internally, :math:`log_{10}(i+1)` is used to determine the
              triangle color. This is equivalent to ``norm=LogNorm()``.
            - If an integer, divide the counts in the specified number
              of bins, and color the triangles accordingly.
            - If a sequence of values, the values of the lower bound of
              the bins to be used.

        xscale : {'linear', 'log'}, default: 'linear'
            Ignored in mpltern and always linear scales on all three axes.

        yscale : {'linear', 'log'}, default: 'linear'
            Ignored in mpltern and always linear scales on all three axes.

        mincnt : int > 0, default: *None*
            If not *None*, only display cells with more than *mincnt*
            number of points in the cell.

        marginals : bool, default: *False*
            Ignored in mpltern.

        extent : 6-tuple of float, default: *None*
            The limits of the bins (tmin, tmax, lmin, lmax, rmin, rmax).
            The default assigns the limits based on *tlim*, *llim*, *rlim*.

        Returns
        -------
        `~matplotlib.collections.PolyCollection`
            A `.PolyCollection` defining the triangular bins.

            - `.PolyCollection.get_offsets` contains a Mx2 array containing
              the x, y positions of the M triangle centers.
            - `.PolyCollection.get_array` contains the values of the M
              triangles.

        Other Parameters
        ----------------
        %(cmap_doc)s

        %(norm_doc)s

        %(vmin_vmax_doc)s

        alpha : float between 0 and 1, optional
            The alpha blending value, between 0 (transparent) and 1 (opaque).

        linewidths : float, default: *None*
            If *None*, defaults to 1.0.

        edgecolors : {'face', 'none', *None*} or color, default: 'face'
            The color of the triangle edges. Possible values are:

            - 'face': Draw the edges in the same color as the fill color.
            - 'none': No edges are drawn. This can sometimes lead to unsightly
              unpainted pixels between the triangles.
            - *None*: Draw outlines in the default color.
            - An explicit color.

        reduce_C_function : callable, default: `numpy.mean`
            The function to aggregate *C* within the bins. It is ignored if
            *C* is not given. This must have the signature::

                def reduce_C_function(C: array) -> float

            Commonly used functions are:

            - `numpy.mean`: average of the points
            - `numpy.sum`: integral of the point values
            - `numpy.amax`: value taken from the largest point

        data : indexable object, optional
            DATA_PARAMETER_PLACEHOLDER

        **kwargs : `~matplotlib.collections.PolyCollection` properties
            All other keyword arguments are passed on to `.PolyCollection`:

            %(PolyCollection:kwdoc)s

        See Also
        --------
        hexbin : 2D histogram hexagonal bins
        """
        self._process_unit_info(
            [("t", t), ("l", l), ("r", r)], kwargs, convert=False)

        t, l, r, C = cbook.delete_masked_points(t, l, r, C)

        # Count the number of data in each triangle
        t = np.asarray(t, float)
        l = np.asarray(l, float)
        r = np.asarray(r, float)

        t, l, r = _normalize_tlr(t, l, r, self.ternary_sum)

        if extent is not None:
            tmin, tmax, lmin, lmax, rmin, rmax = extent
        else:
            tmin, tmax = self.get_tlim()
            lmin, lmax = self.get_llim()
            rmin, rmax = self.get_rlim()

        # number of triangles
        n = gridsize ** 2

        st, sl, sr, it, il, ir = tribin_helpers.calc_ternary_indices(
            t, l, r, gridsize, (tmin, tmax, lmin, lmax, rmin, rmax))

        # flat indices, plus one so that out-of-range points go to position 0.
        indices = tribin_helpers.ternary_to_serial(gridsize, it, il, ir) + 1

        if C is None:  # [1:] drops out-of-range points.
            counts = np.bincount(indices, minlength=1 + n)[1:]
            accum = counts.astype(float)
            if mincnt is not None:
                accum[accum < mincnt] = np.nan
        else:
            # store the C values in a list per hexagon index
            Cs = [[] for _ in range(1 + n)]
            for i in range(len(C)):
                Cs[indices[i]].append(C[i])
            if mincnt is None:
                mincnt = 0
            accum = np.array(
                [reduce_C_function(acc) if len(acc) >= mincnt else np.nan
                 for acc in Cs[1:]],  # [1:] drops out-of-range points.
                float)

        good_idxs = ~np.isnan(accum)

        _ = tribin_helpers.serial_to_ternary(gridsize, np.arange(n))
        offsets = np.array(_).T.astype(float)

        # remove accumulation bins with no data
        offsets = offsets[good_idxs, :]
        accum = accum[good_idxs]

        polygons = np.repeat(offsets[:, None, :], 3, axis=1)

        # number of upward triangles
        nup = gridsize * (gridsize + 1) // 2

        # upward triangles
        polygons[:nup, 0, :] += [1, 0, 0]
        polygons[:nup, 1, :] += [0, 1, 0]
        polygons[:nup, 2, :] += [0, 0, 1]

        # downward triangles
        polygons[nup:, 0, :] += [0, 1, 1]
        polygons[nup:, 1, :] += [1, 0, 1]
        polygons[nup:, 2, :] += [1, 1, 0]

        # scale into [0, 1]
        polygons /= gridsize

        # scale into the given extent
        polygons_c = 1.0 - polygons
        polygons[..., 0] = polygons_c[..., 0] * tmin + polygons[..., 0] * tmax
        polygons[..., 1] = polygons_c[..., 1] * lmin + polygons[..., 1] * lmax
        polygons[..., 2] = polygons_c[..., 2] * rmin + polygons[..., 2] * rmax

        if linewidths is None:
            linewidths = [1.0]

        polygons = polygons.reshape(-1, 3)
        polygons = self.transProjection.transform(polygons)
        polygons = polygons.reshape(-1, 3, 2)

        collection = mcoll.PolyCollection(
            polygons,
            edgecolors=edgecolors,
            linewidths=linewidths,
        )

        # Set normalizer if bins is 'log'
        if bins == 'log':
            if norm is not None:
                _api.warn_external("Only one of 'bins' and 'norm' arguments "
                                   f"can be supplied, ignoring bins={bins}")
            else:
                norm = mcolors.LogNorm(vmin=vmin, vmax=vmax)
                vmin = vmax = None
            bins = None

        # autoscale the norm with current accum values if it hasn't been set
        if norm is not None:
            if norm.vmin is None and norm.vmax is None:
                norm.autoscale(accum)

        if bins is not None:
            if not np.iterable(bins):
                minimum, maximum = min(accum), max(accum)
                bins -= 1  # one less edge than bins
                bins = minimum + (maximum - minimum) * np.arange(bins) / bins
            bins = np.sort(bins)
            accum = bins.searchsorted(accum)

        collection.set_array(accum)
        collection.set_cmap(cmap)
        collection.set_norm(norm)
        collection.set_alpha(alpha)
        collection.update(kwargs)  # matplotlib/matplotlib#22451
        collection._scale_norm(norm, vmin, vmax)

        # add the collection last
        self.add_collection(collection, autolim=False)
        return collection

    arrow = parse_ternary_vector(TernaryAxesBase.arrow)
    quiver = parse_ternary_vector(TernaryAxesBase.quiver)
    barbs = parse_ternary_vector(TernaryAxesBase.barbs)
    fill = parse_ternary_multiple(TernaryAxesBase.fill)
    hist2d = parse_ternary_single(TernaryAxesBase.hist2d)
    tricontour = parse_ternary_single(TernaryAxesBase.tricontour)
    tricontourf = parse_ternary_single(TernaryAxesBase.tricontourf)
    tripcolor = parse_ternary_single(TernaryAxesBase.tripcolor)
    triplot = parse_ternary_single(TernaryAxesBase.triplot)


def _normalize_tlr(t, l, r, ternary_sum):
    """Normalize ternary values

    This is used only in `hexbin` and `tribin` because in these methods ternary
    values must be analyzed inside.
    In the other methods ternary values are normalized in parsers beforehand.
    """
    scale = ternary_sum / (t + l + r)
    t *= scale
    l *= scale
    r *= scale
    return t, l, r
