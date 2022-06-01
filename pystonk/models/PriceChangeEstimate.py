from pystonk.models.CandleStick import CandleStick

from scipy.stats import norm
from typing import List, Tuple

import numpy as np


class PriceChangeEstimate(object):
    def __init__(self, data: List[CandleStick], bins=10):
        self._raw_data = data
        self._data = [c.percentChange for c in self._raw_data]
        self._mean = np.mean(self._data)
        self._std = np.std(self._data)

        self._histogram, self._bin_edges = np.histogram(self._data, bins='fd')
        # center the histogram bins via:
        # https://stackoverflow.com/questions/17966093/is-there-a-way-to-return-same-length-arrays-in-numpy-hist
        self._bins = .5 * (self._bin_edges[1:] + self._bin_edges[:-1])

        self._pdf = norm.pdf(self._data, loc=self._mean, scale=self._std)
        self._cdf = norm(loc=self._mean, scale=self._std).cdf

    def mean(self) -> float:
        return round(float(self._mean), 2)

    def std(self) -> float:
        return round(float(self._std), 2)

    def histogram(self) -> List:
        return [round(d, 2) for d in self._histogram.tolist()]

    def histogramBins(self) -> List:
        return [round(d, 2) for d in self._bins.tolist()]

    def pdf(self) -> Tuple:
        return self._data, [round(v, 4) for v in self._pdf]

    def percentProbability(self, percent: float) -> float:
        return round((1 - self._cdf(percent)) * 100, 2)
