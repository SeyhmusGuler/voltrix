import polars as pl
from hypothesis import given

from tests.strategies import polars_trades_dataframe

# -----------------------------------------------------------------------------
# Function under test
# -----------------------------------------------------------------------------


def filter_large_trades(df: pl.DataFrame, threshold: float = 1000.0) -> pl.DataFrame:
    """Filters trades with a total value (price * quantity) greater than threshold."""
    if df.is_empty():
        return df

    return df.filter((pl.col("price") * pl.col("quantity")) > threshold)


# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------


@given(trades=polars_trades_dataframe())
def test_filter_large_trades(trades: pl.DataFrame):
    """
    Property: Filtered result should only contain trades with value > threshold.
    """
    threshold = 5000.0  # Using a fixed threshold for simplicity

    filtered = filter_large_trades(trades, threshold=threshold)

    # Property 1: Schema should be preserved
    assert filtered.schema == trades.schema

    # Property 2: Row count should be <= original row count
    assert filtered.height <= trades.height

    # Property 3: All remaining rows must satisfy the condition
    if not filtered.is_empty():
        # Calculate value column just for verification
        check_df = filtered.with_columns((pl.col("price") * pl.col("quantity")).alias("value"))
        min_value = check_df["value"].min()
        assert min_value > threshold


@given(trades=polars_trades_dataframe())
def test_polars_lazy_execution(trades: pl.DataFrame):
    """
    Demonstrate testing with LazyFrames.
    """
    # Convert to LazyFrame
    lazy_trades = trades.lazy()

    # Apply some operations
    result_lazy = lazy_trades.group_by("symbol").agg(pl.col("price").mean().alias("avg_price"))

    # Collect results
    result = result_lazy.collect()

    assert isinstance(result, pl.DataFrame)
    # Check that we have one row per unique symbol
    unique_symbols = trades["symbol"].unique()
    assert result.height == unique_symbols.len()
