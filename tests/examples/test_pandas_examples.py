import numpy as np
import pandas as pd
import pandera.pandas as pa
from hypothesis import given
from pandera.typing import DataFrame, Series

from tests.strategies import pandas_trades_dataframe

# -----------------------------------------------------------------------------
# Pandera Schema Definition
# -----------------------------------------------------------------------------


class TradeSchema(pa.DataFrameModel):
    trade_id: Series[str] = pa.Field(coerce=True)
    symbol: Series[str] = pa.Field(isin=["AAPL", "GOOGL", "MSFT", "TSLA"])
    price: Series[float] = pa.Field(ge=0.0)
    quantity: Series[int] = pa.Field(ge=1)
    timestamp: Series[pd.Timestamp]

    class Config:
        strict = True


# -----------------------------------------------------------------------------
# Function under test
# -----------------------------------------------------------------------------


@pa.check_types
def calculate_vwap(trades: DataFrame[TradeSchema]) -> float:
    """Calculates Volume Weighted Average Price."""
    if trades.empty:
        return 0.0

    total_value = (trades["price"] * trades["quantity"]).sum()
    total_volume = trades["quantity"].sum()

    if total_volume == 0:
        return 0.0

    return total_value / total_volume


# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------


@given(trades=pandas_trades_dataframe())
def test_calculate_vwap_properties(trades: pd.DataFrame):
    """
    Test that VWAP calculation holds basic properties:
    1. Returns a float
    2. Is within the range of min and max prices in the input
    3. Handles generated data strictly checking schema
    """
    # Pandera validation happens automatically via @pa.check_types decorator
    # but we can also validate explicitly if we want
    validated_df = TradeSchema.validate(trades)

    vwap = calculate_vwap(validated_df)

    assert isinstance(vwap, float)

    if not trades.empty:
        # VWAP must be between min and max price
        min_price = trades["price"].min()
        max_price = trades["price"].max()
        assert min_price - 1e6 * np.finfo(float).eps <= vwap <= max_price + 1e6 * np.finfo(float).eps
