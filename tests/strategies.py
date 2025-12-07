from datetime import datetime

import numpy as np
import pandas as pd
import polars as pl
from hypothesis import strategies as st
from hypothesis.extra import numpy as npst

# -----------------------------------------------------------------------------
# Base Strategies
# -----------------------------------------------------------------------------


def valid_dates(start_date: str = "2000-01-01", end_date: str = "2025-12-31") -> st.SearchStrategy[datetime]:
    """Strategy for generating dates within a specific range."""
    return st.dates(
        min_value=datetime.strptime(start_date, "%Y-%m-%d").date(),
        max_value=datetime.strptime(end_date, "%Y-%m-%d").date(),
    ).map(lambda d: datetime.combine(d, datetime.min.time()))


def mongo_ids() -> st.SearchStrategy[str]:
    """Strategy to generate mock MongoDB ObjectIds."""
    return st.text(alphabet="0123456789abcdef", min_size=24, max_size=24)


# -----------------------------------------------------------------------------
# Data Factories (Composite Strategies)
# -----------------------------------------------------------------------------


@st.composite
def trade_data_strategy(draw, size: int = 10):
    """
    Generates a dictionary representing trade data.
    """
    return {
        "trade_id": draw(st.lists(st.uuids().map(str), min_size=size, max_size=size)),
        "symbol": draw(st.lists(st.sampled_from(["AAPL", "GOOGL", "MSFT", "TSLA"]), min_size=size, max_size=size)),
        "price": draw(st.lists(st.floats(min_value=10.0, max_value=1000.0), min_size=size, max_size=size)),
        "quantity": draw(st.lists(st.integers(min_value=1, max_value=100), min_size=size, max_size=size)),
        "timestamp": draw(st.lists(valid_dates(), min_size=size, max_size=size)),
    }


@st.composite
def pandas_trades_dataframe(draw, min_size=1, max_size=10):
    """
    Generates a Pandas DataFrame of trades.
    """
    size = draw(st.integers(min_value=min_size, max_value=max_size))
    data = draw(trade_data_strategy(size=size))
    return pd.DataFrame(data)


@st.composite
def polars_trades_dataframe(draw, min_size=1, max_size=10):
    """
    Generates a Polars DataFrame of trades.
    """
    size = draw(st.integers(min_value=min_size, max_value=max_size))
    data = draw(trade_data_strategy(size=size))
    return pl.DataFrame(data)


# -----------------------------------------------------------------------------
# Numpy Arrays
# -----------------------------------------------------------------------------


def financial_returns_array(shape=(100,)) -> st.SearchStrategy[np.ndarray]:
    """Generates an array of financial returns (small floats)."""
    return npst.arrays(
        dtype=np.float64, shape=shape, elements=st.floats(min_value=-0.1, max_value=0.1, allow_nan=False)
    )
