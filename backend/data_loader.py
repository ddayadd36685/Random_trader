import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Tuple, Optional


def load_all_stocks(data_dir: str = "data") -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series]:
    """
    加载所有股票的收盘价数据
    返回: (close_df, amt_df, csiall_series)
    """
    data_path = Path(data_dir)
    
    close_df = pd.read_csv(data_path / "close_adj_day.csv", index_col=0)
    amt_df = pd.read_csv(data_path / "amt_day.csv", index_col=0)
    csiall_df = pd.read_csv(data_path / "csiall_day.csv", index_col=0)
    
    close_df = close_df.T
    close_df.index = pd.to_datetime(close_df.index)
    
    amt_df = amt_df.T
    amt_df.index = pd.to_datetime(amt_df.index)
    
    csiall_series = csiall_df.iloc[0, :]
    csiall_series.index = pd.to_datetime(csiall_series.index)
    csiall_series = csiall_series.dropna()
    
    return close_df, amt_df, csiall_series


def prepare_data_for_strategy(close_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DatetimeIndex]:
    """
    准备策略数据
    返回: (daily_df, weekly_dates)
    """
    daily_df = close_df.copy()
    daily_df.index.name = "date"
    
    weekly_dates = daily_df.resample("W-FRI").last().index
    
    return daily_df, weekly_dates


def calculate_market_equal_weight(close_df: pd.DataFrame, initial_capital: float = 100000) -> pd.Series:
    """
    计算市场等权指数（量化级严谨处理）
    每天只对当日有有效价格的股票做等权平均
    正确处理：未上市、退市、停牌等NaN情况
    """
    returns = close_df.pct_change()
    
    valid_count = close_df.notna().sum(axis=1)
    
    returns_sum = returns.sum(axis=1, skipna=True)
    
    equal_weight_returns = returns_sum / valid_count
    
    equal_weight_returns = equal_weight_returns.where(valid_count > 0, 0)
    
    equal_weight_index = (1 + equal_weight_returns).cumprod() * initial_capital
    
    first_valid_idx = valid_count[valid_count > 0].first_valid_index()
    if first_valid_idx is not None:
        equal_weight_index.loc[first_valid_idx] = initial_capital
    
    return equal_weight_index


def calculate_csi_all_index(csiall_series: pd.Series, initial_capital: float = 100000) -> pd.Series:
    """
    从中证全指原始点位计算基准曲线
    """
    csiall_clean = csiall_series.dropna()
    
    csi_index = (csiall_clean / csiall_clean.iloc[0]) * initial_capital
    
    return csi_index


def convert_to_candles_format(prices: pd.Series) -> list:
    """
    将价格序列转换为前端需要的蜡烛图格式
    """
    candles = []
    for idx, price in prices.items():
        if pd.isna(price):
            continue
        candles.append({
            "t": int(idx.timestamp() * 1000),
            "o": float(price),
            "h": float(price),
            "l": float(price),
            "c": float(price),
            "v": 0
        })
    return candles
