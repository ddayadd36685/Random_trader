import pandas as pd
import numpy as np
from typing import Dict


def calculate_metrics(equity_series: pd.Series, benchmark_series: pd.Series, initial_capital: float) -> Dict:
    """
    计算策略和基准的各项指标
    """
    strategy_returns = equity_series.pct_change().dropna()
    benchmark_returns = benchmark_series.pct_change().dropna()
    
    total_return = (equity_series.iloc[-1] / initial_capital) - 1
    benchmark_total_return = (benchmark_series.iloc[-1] / initial_capital) - 1
    
    trading_days = len(equity_series)
    years = trading_days / 252
    
    annualized_return = (1 + total_return) ** (1 / years) - 1 if years > 0 else 0
    benchmark_annualized_return = (1 + benchmark_total_return) ** (1 / years) - 1 if years > 0 else 0
    
    annualized_volatility = strategy_returns.std() * np.sqrt(252)
    benchmark_annualized_volatility = benchmark_returns.std() * np.sqrt(252)
    
    max_drawdown = calculate_max_drawdown(equity_series)
    benchmark_max_drawdown = calculate_max_drawdown(benchmark_series)
    
    alpha = total_return - benchmark_total_return
    
    winning_trades = 0
    total_trades = 0
    
    return {
        "total_return": float(total_return),
        "benchmark_total_return": float(benchmark_total_return),
        "annualized_return": float(annualized_return),
        "benchmark_annualized_return": float(benchmark_annualized_return),
        "annualized_volatility": float(annualized_volatility),
        "benchmark_annualized_volatility": float(benchmark_annualized_volatility),
        "max_drawdown": float(max_drawdown),
        "benchmark_max_drawdown": float(benchmark_max_drawdown),
        "alpha": float(alpha),
        "final_equity": float(equity_series.iloc[-1]),
        "benchmark_final_equity": float(benchmark_series.iloc[-1]),
        "initial_capital": float(initial_capital),
        "trading_days": int(trading_days),
        "outperform": bool(total_return > benchmark_total_return)
    }


def calculate_max_drawdown(equity_series: pd.Series) -> float:
    """
    计算最大回撤
    """
    rolling_max = equity_series.cummax()
    drawdown = (equity_series - rolling_max) / rolling_max
    max_drawdown = drawdown.min()
    return float(max_drawdown)


def convert_equity_to_format(equity_series: pd.Series) -> list:
    """
    将净值序列转换为前端需要的格式
    """
    data = []
    for idx, value in equity_series.items():
        data.append({
            "t": int(idx.timestamp() * 1000),
            "v": float(value)
        })
    return data
