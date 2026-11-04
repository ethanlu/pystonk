from io import BytesIO
from scipy.stats import kurtosis, norm, probplot, skew
from typing import List, Tuple

import io
import matplotlib.pyplot as plt
import numpy as np


class PriceHistoryAnalysis(object):
    def __init__(self, data: List[float]):
        self._data = data
        self._mean, self._std = norm.fit(self._data)
        self._skew = skew(self._data)
        self._kurtosis = kurtosis(self._data)

    def min(self) -> float:
        return round(min(self._data), 2)

    def max(self) -> float:
        return round(max(self._data), 2)

    def mean(self) -> float:
        return round(float(self._mean), 2)

    def std(self) -> float:
        return round(float(self._std), 2)

    def skew(self) -> float:
        return round(float(self._skew), 2)

    def kurtosis(self) -> float:
        return round(float(self._kurtosis), 2)

    def percent_probability(self, percent: float) -> float:
        cdf = norm(loc=self._mean, scale=self._std).cdf
        if percent >= 0:
            return round((1 - cdf(percent)) * 100, 2)
        else:
            return round(cdf(percent) * 100, 2)

    def histogram(self) -> BytesIO:
        # set up the figure and the primary axis (Left: Counts)
        fig, ax1 = plt.subplots()

        # plot the histogram using raw counts on ax1 and capture the bin settings to match
        counts, bins, patches = ax1.hist(self._data, bins=25, color='skyblue', edgecolor='black')

        ax1.set_xlabel("Percent Change")
        ax1.set_ylabel("Bin Counts", color='skyblue')
        ax1.tick_params(axis='y', labelcolor='skyblue')
        ax1.grid(True, alpha=.3)

        # create a twin axis that shares the same x-axis (Right: Density)
        ax2 = ax1.twinx()

        # generate points for the curve
        xmin, xmax = ax1.get_xlim()
        x = np.linspace(xmin, xmax, 100)
        p = norm.pdf(x, self._mean, self._std)

        # 7. Plot the curve on the density axis (ax2)
        ax2.plot(x, p, 'r-', linewidth=2, color='orange', label=f'Fit (μ={self._mean:.2f}, σ={self._std:.2f})')

        ax2.set_ylabel("Probability Density", color='orange')
        ax2.tick_params(axis='y', labelcolor='orange')

        # align the limits so the scales mathematically match and scale the right axis (Density) maximum relative to the left axis (Counts) maximum
        bin_width = bins[1] - bins[0]
        total_count = len(self._data)
        # Maximum counts divided by total samples and bin width gives the peak density limit
        ax2.set_ylim(0, ax1.get_ylim()[1] / (total_count * bin_width))

        # clean up layout and display
        plt.title("Percent Change With Normal Fit")
        plt.legend()
        fig.tight_layout()

        # save graph as byte array
        image_buffer = BytesIO()
        plt.savefig(image_buffer, format='png', bbox_inches='tight')

        return image_buffer

    def qq(self) -> BytesIO:
        # generate qq data
        (theoretical_quantiles, ordered_samples), (slope, intercept, r) = (probplot(self._data, dist="norm", fit=True))
        qq_data = np.column_stack((theoretical_quantiles, ordered_samples))

        # fitted line's y-values for each theoretical quantile
        line_y = slope * theoretical_quantiles + intercept

        # plot qq information as scatter plot
        plt.figure(figsize=(6, 6))
        plt.scatter(
            theoretical_quantiles,
            ordered_samples,
            color="blue",
            alpha=0.7,
            label="Percent Change Data",
        )
        plt.plot(
            theoretical_quantiles,
            line_y,
            color="red",
            linestyle="--",
            label=f"Fit (slope={slope:.2f}, intercept={intercept:.2f})",
        )

        plt.xlabel("Theoretical Quantiles")
        plt.ylabel("Ordered Percent Change")
        plt.title("QQ Scatter Plot")
        plt.legend()
        plt.grid(True)

        # save graph as byte arrat
        image_buffer = BytesIO()
        plt.savefig(image_buffer, format='png', bbox_inches='tight')

        return image_buffer
