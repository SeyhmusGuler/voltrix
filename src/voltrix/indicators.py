import pandas as pd
import polars as pl


def vwap(high: pd.Series, low: pd.Series, close: pd.Series, volume: pd.Series, length: int) -> pd.Series:
    """Volume Weighted Average Price (VWAP)

    VWAP is a trading benchmark that gives the average price a security has traded at throughout the day,
    based on both volume and price. It is important because it provides traders with insight into both the trend
    and value of a security.

    Args:
        high (pd.Series): Series of high prices.
        low (pd.Series): Series of low prices.
        close (pd.Series): Series of closing prices.
        volume (pd.Series): Series of volume data.
        length (int): The period over which to calculate the VWAP.

    Returns:
        pd.Series: The VWAP values.
    """
    typical_price = (high + low + close) / 3
    tp_volume = typical_price * volume
    vwap = tp_volume.rolling(window=length).sum() / volume.rolling(window=length).sum()
    return vwap


def use_polars(high: pl.Series, low: pl.Series, close: pl.Series, volume: pl.Series, length: int) -> pl.Series:
    typical_price = (high + low + close) / 3
    tp_volume = typical_price * volume
    vwap = tp_volume.rolling_sum(length) / volume.rolling_sum(length)
    return vwap
