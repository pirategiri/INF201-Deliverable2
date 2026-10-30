"""Task 4: pandas functions."""
import pandas as pd

from src.numeric import compute_refund_ratio

STATUSES = ["SUCCESS", "REFUND", "CANCELLED"]


def build_dataframe(records):
    """List of dicts -> DataFrame indexed by timestamp, sorted in time order."""
    df = pd.DataFrame(records)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.set_index("timestamp").sort_index()
    return df


def hourly_revenue(df):
    """Total price per item in 1-hour windows."""
    return df.groupby("item")["price"].resample("1h").sum()


def status_pivot(df):
    """Total revenue per item (rows) and status (columns)."""
    pivot = df.pivot_table(values="price", index="item", columns="status",
                           aggfunc="sum", fill_value=0)
    return pivot.reindex(columns=STATUSES, fill_value=0)


def item_refund_ratios(df):
    """Refund ratio per item, using the NumPy function from Task 3."""
    counts = df.groupby(["item", "status"]).size().unstack(fill_value=0)
    counts = counts.reindex(columns=STATUSES, fill_value=0)
    ratio = compute_refund_ratio(counts["SUCCESS"].to_numpy(),
                                 counts["REFUND"].to_numpy())
    return pd.DataFrame({"item": counts.index, "refund_ratio": ratio})
