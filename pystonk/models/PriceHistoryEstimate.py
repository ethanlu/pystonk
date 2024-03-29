from scipy.stats import kurtosis, norm, skew
from typing import List, Tuple

import numpy as np


class PriceHistoryEstimate(object):
    def __init__(self, data: List[float]):
        self._data = data
        self._mean = np.mean(self._data)
        self._std = np.std(self._data)
        self._skew = skew(np.array(self._data))
        self._kurtosis = kurtosis(self._data)
        self._min = min(self._data)
        self._max = max(self._data)

        self._histogram, self._bin_edges = np.histogram(self._data, bins=self._calculate_bins())
        # center the histogram bins via:
        # https://stackoverflow.com/questions/17966093/is-there-a-way-to-return-same-length-arrays-in-numpy-hist
        self._bins = .5 * (self._bin_edges[1:] + self._bin_edges[:-1])

        self._pdf = norm.pdf(self._data, loc=self._mean, scale=self._std)
        self._cdf = norm(loc=self._mean, scale=self._std).cdf

    def _calculate_bins(self) -> List:
        diff = abs(self._max - self._min)

        interval = 1.0
        if 50 < diff <= 100:
            interval = 2.5
        if 100 < diff:
            interval = 5.0

        return list(np.arange((interval * round(self._min / interval) - interval), (interval * round(self._max / interval) + interval), interval))

    def mean(self) -> float:
        return round(float(self._mean), 2)

    def std(self) -> float:
        return round(float(self._std), 2)

    def min(self) -> float:
        return round(self._min, 2)

    def max(self) -> float:
        return round(self._max, 2)

    def skew(self) -> float:
        return round(float(self._skew), 2)

    def kurtosis(self) -> float:
        return round(float(self._kurtosis), 2)

    def histogram(self) -> List:
        return [round(d, 2) for d in self._histogram.tolist()]

    def histogram_bins(self) -> List:
        return [round(d, 2) for d in self._bins.tolist()]

    def histogram_bins_interval(self) -> List:
        return abs(self._bins[1] - self._bins[0])

    def pdf(self) -> Tuple:
        return self._data, [round(v, 4) for v in self._pdf]

    def percent_probability(self, percent: float) -> float:
        if percent >= 0:
            return round((1 - self._cdf(percent)) * 100, 2)
        else:
            return round(self._cdf(percent) * 100, 2)
