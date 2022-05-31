from pystonk.models.CandleStick import CandleStick

from statsmodels.nonparametric.kde import KDEUnivariate
from typing import List, Tuple

import numpy as np


class PriceChangeEstimate(object):
    BINS = list(range(-30, 31, 3))

    def __init__(self, data: List[CandleStick], bins=10):
        self._raw_data = data
        self._data = [c.percentChange for c in self._raw_data]
        self._mean = round(np.mean(self._data), 2)
        self._std = round(np.std(self._data), 2)

        self._histogram, self._bin_edges = np.histogram(self._data, bins=self.BINS)
        # center the histogram bins via:
        # https://stackoverflow.com/questions/17966093/is-there-a-way-to-return-same-length-arrays-in-numpy-hist
        self._bins = .5 * (self._bin_edges[1:] + self._bin_edges[:-1])

        self._kde_unweighted = KDEUnivariate(self._bins)
        self._kde_unweighted.fit()
        self._kde_weighted = KDEUnivariate(self._bins)
        self._kde_weighted.fit(weights=self._histogram.astype(float), fft=False)

    def mean(self) -> float:
        return self._mean

    def std(self) -> float:
        return self._std

    def histogram(self, normalize=False) -> List:
        h = self._histogram.tolist()
        if normalize:
            max_value = max(h)

        return [round(d / max_value if normalize else d, 2) for d in h]

    def histogramBins(self) -> List:
        return [round(d, 2) for d in self._bins.tolist()]

    def pdf(self, weighted: bool = True) -> Tuple:
        if weighted:
            support = self._kde_weighted.support
            density = self._kde_weighted.density
        else:
            support = self._kde_unweighted.support
            density = self._kde_unweighted.density

        return [round(s, 2) for s in support], [round(d, 4) for d in density]

    def percentProbability(self, percent: float, weighted: bool = True) -> float:
        if weighted:
            cdf = zip(self._kde_weighted.support, self._kde_weighted.cdf)
        else:
            cdf = zip(self._kde_unweighted.support, self._kde_unweighted.cdf)

        return round((1 - [c for (s, c) in cdf if percent > s][-1]) * 100, 2)
