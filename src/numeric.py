"""Task 3: NumPy functions for cleaning and analysis."""
import numpy as np


def remove_outliers(prices):
    """Replace values more than 3 standard deviations from the mean with the median."""
    prices = np.array(prices, dtype=float)  # np.array makes a copy
    mean = prices.mean()
    std = prices.std()
    is_outlier = np.abs(prices - mean) > 3 * std
    median = np.median(prices[~is_outlier])
    prices[is_outlier] = median
    return prices


def compute_refund_ratio(sales_count, refund_count):
    """Element-wise refund ratio. The tiny 1e-6 avoids division by zero."""
    return refund_count / (sales_count + 1e-6)
