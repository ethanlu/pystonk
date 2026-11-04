from io import BytesIO
from typing import List

import math
import matplotlib.pyplot as plt
import numpy as np
import statistics


class PriceHistoryAnalysis(object):
    def __init__(self, data: List[float]):
        self._data = data
        self._mean = statistics.mean(self._data)
        self._std = statistics.pstdev(self._data)

    def _normal_cdf(self, x: float, loc: float, scale: float) -> float:
        return 0.5 * (1.0 + math.erf(((x - loc) / scale) / math.sqrt(2.0)))

    def _normal_pdf(self, x: float, loc: float, scale: float) -> float:
        variance = scale ** 2
        denominator = math.sqrt(2 * math.pi * variance)
        exponent = -((x - loc) ** 2) / (2 * variance)
        return math.exp(exponent) / denominator

    def _rational_approximation(self, t) -> float:
        """Beasley-Springer-Moro approximation for standard normal inverse CDF."""
        c = [2.515517, 0.802853, 0.010328]
        d = [1.432788, 0.189269, 0.001308]
        numerator = (c[2] * t + c[1]) * t + c[0]
        denominator = ((d[2] * t + d[1]) * t + d[0]) * t + 1.0
        return t - numerator / denominator

    def _normal_ppf(self, p) -> float:
        """Percent point function (inverse CDF) for standard normal distribution."""
        if p <= 0.0 or p >= 1.0:
            raise ValueError("Probability must be between 0 and 1 exclusive.")
        if p < 0.5:
            t = math.sqrt(-2.0 * math.log(p))
            return -self._rational_approximation(t)
        else:
            t = math.sqrt(-2.0 * math.log(1.0 - p))
            return self._rational_approximation(t)

    def _probplot(self):
        """
            Computes theoretical normal quantiles (osm) and ordered sample data (osr)
            similar to scipy.stats.probplot.
            """
        n = len(self._data)
        if n == 0:
            return [], []

        # 1. Sort the sample data
        osr = sorted(self._data)

        # 2. Compute plotting positions (using Filliben-like or Blom's formula: (i - 0.375) / (n + 0.25))
        osm = []
        for i in range(1, n + 1):
            # Blom's formula for plotting positions
            p = (i - 0.375) / (n + 0.25)
            quant = self._normal_ppf(p)
            osm.append(quant)

        return osm, osr

    def _calculate_least_squares(self, x, y):
        """
        Calculates the slope, intercept, and R-squared coefficient
        for a linear regression line using native Python.
        """
        n = len(x)
        if n != len(y):
            raise ValueError("x and y must be of the same length.")
        if n < 2:
            raise ValueError("At least two data points are required.")

        # 1. Compute means
        mean_x = sum(x) / n
        mean_y = sum(y) / n

        # 2. Compute variance and covariance components
        numerator = 0.0  # Sum of (x_i - mean_x) * (y_i - mean_y)
        denominator = 0.0  # Sum of (x_i - mean_x)^2
        ss_tot = 0.0  # Total sum of squares for R^2: Sum of (y_i - mean_y)^2

        for xi, yi in zip(x, y):
            dx = xi - mean_x
            dy = yi - mean_y
            numerator += dx * dy
            denominator += dx * dx
            ss_tot += dy * dy

        # Prevent division by zero if all x values are identical
        if denominator == 0:
            raise ZeroDivisionError("Cannot compute slope; X variance is zero.")

        # 3. Calculate slope and intercept
        slope = numerator / denominator
        intercept = mean_y - (slope * mean_x)

        # 4. Calculate R-squared (Coefficient of Determination)
        ss_res = 0.0  # Residual sum of squares: Sum of (y_i - y_predicted)^2
        for xi, yi in zip(x, y):
            y_pred = slope * xi + intercept
            ss_res += (yi - y_pred) ** 2

        # If ss_tot is 0, data is a perfectly horizontal line
        r_squared = 1.0 - (ss_res / ss_tot) if ss_tot != 0 else 1.0

        return slope, intercept, r_squared

    def min(self) -> float:
        return round(min(self._data), 2)

    def max(self) -> float:
        return round(max(self._data), 2)

    def mean(self) -> float:
        return round(float(self._mean), 2)

    def std(self) -> float:
        return round(float(self._std), 2)

    def skew(self, bias=True) -> float:
        n = len(self._data)
        if n < 3 and not bias:
            raise ValueError("bias=False requires at least 3 data points.")
        if n < 2:
            raise ValueError("Data must contain at least 2 points.")

        # 1. Calculate the mean
        mean = sum(self._data) / n

        # 2. Calculate the 2nd (variance) and 3rd central moments
        m2 = sum((x - mean) ** 2 for x in self._data) / n
        m3 = sum((x - mean) ** 3 for x in self._data) / n

        if m2 == 0:
            return 0.0  # Avoid division by zero for constant data

        # 3. Compute the biased skewness
        skew_biased = m3 / (m2 ** 1.5)

        if bias:
            return round(skew_biased, 2)
        else:
            # SciPy's unbiased correction formula for skewness
            correction = ((n * (n - 1)) ** 0.5) / (n - 2)
            return round(skew_biased * correction, 2)

    def kurtosis(self, fisher=True, bias=True) -> float:
        n = len(self._data)
        if n < 4 and not bias:
            raise ValueError("bias=False requires at least 4 data points.")
        if n < 2:
            raise ValueError("Data must contain at least 2 points.")

        # 1. Calculate the mean
        mean = sum(self._data) / n

        # 2. Calculate the 2nd (variance) and 4th central moments
        m2 = sum((x - mean) ** 2 for x in self._data) / n
        m4 = sum((x - mean) ** 4 for x in self._data) / n

        if m2 == 0:
            return 0.0  # Avoid division by zero for constant data

        # 3. Compute the biased kurtosis
        kurt_biased = m4 / (m2 ** 2)

        if bias:
            kurt = kurt_biased
        else:
            # SciPy's unbiased correction formula using k-statistics
            # This matches scipy.stats.kurtosis(bias=False, fisher=False)
            kurt = (1 / ((n - 2) * (n - 3))) * ((n + 1) * kurt_biased - 3 * (n - 1)) + 3

        # 4. Adjust for Fisher vs. Pearson definition
        return round(kurt - 3.0 if fisher else kurt, 2)

    def percent_probability(self, percent: float) -> float:
        if percent >= 0:
            pp = (1 - self._normal_cdf(percent, self.mean(), self.std())) * 100
        else:
            pp = self._normal_cdf(percent, self.mean(), self.std()) * 100
        return round(pp, 2)

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
        p = [self._normal_pdf(d, self.mean(), self.std()) for d in list(x)]

        # 7. Plot the curve on the density axis (ax2)
        ax2.plot(x, p, linewidth=2, color='orange', label=f'Fit (μ={self._mean:.2f}, σ={self._std:.2f})')

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
        theoretical_quantiles, ordered_samples = self._probplot()
        slope, intercept, r = self._calculate_least_squares(theoretical_quantiles, ordered_samples)
        qq_data = np.column_stack((theoretical_quantiles, ordered_samples))

        # fitted line's y-values for each theoretical quantile
        line_y = [slope * x + intercept for x in theoretical_quantiles]

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

        # save graph as byte array
        image_buffer = BytesIO()
        plt.savefig(image_buffer, format='png', bbox_inches='tight')

        return image_buffer
