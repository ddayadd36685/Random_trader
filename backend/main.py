from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List, Dict
import pandas as pd
import os
from pathlib import Path

from backend.data_loader import (
    load_all_stocks,
    prepare_data_for_strategy,
    calculate_market_equal_weight,
    calculate_csi_all_index,
    convert_to_candles_format
)
from backend.strategy import RandomTrader
from backend.metrics import calculate_metrics, convert_equity_to_format

app = FastAPI(title="Random Trader vs Index")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class StrategyParams(BaseModel):
    initial_capital: float = 100000
    buy_prob: float = 0.4
    sell_prob: float = 0.4
    hold_prob: float = 0.2
    min_position_ratio: float = 0.2
    max_position_ratio: float = 0.8
    commission_bps: float = 5
    seed: Optional[int] = None


@app.get("/")
async def root():
    return FileResponse("frontend/index.html")


@app.get("/api/health")
async def health_check():
    return {"status": "ok"}


@app.get("/api/sample-data")
async def get_sample_data():
    try:
        close_df, amt_df, csiall_series = load_all_stocks()
        daily_df, weekly_df = prepare_data_for_strategy(close_df)
        
        first_stock = close_df.columns[0]
        candles = convert_to_candles_format(close_df[first_stock])
        
        return {
            "success": True,
            "data": {
                "candles": candles,
                "date_range": {
                    "start": close_df.index[0].isoformat(),
                    "end": close_df.index[-1].isoformat()
                },
                "trading_days": len(close_df),
                "stock_count": len(close_df.columns)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/run-strategy")
async def run_strategy(params: StrategyParams):
    try:
        close_df, amt_df, csiall_series = load_all_stocks()
        daily_df, weekly_dates = prepare_data_for_strategy(close_df)
        
        trader = RandomTrader(
            initial_capital=params.initial_capital,
            buy_prob=params.buy_prob,
            sell_prob=params.sell_prob,
            hold_prob=params.hold_prob,
            min_position_ratio=params.min_position_ratio,
            max_position_ratio=params.max_position_ratio,
            commission_bps=params.commission_bps,
            seed=params.seed
        )
        
        trades, equity_series = trader.run(daily_df, weekly_dates)
        
        csi_all_index = calculate_csi_all_index(csiall_series, params.initial_capital)
        market_equal_weight = calculate_market_equal_weight(close_df, params.initial_capital)
        
        common_dates = equity_series.index.intersection(csi_all_index.index).intersection(market_equal_weight.index)
        
        equity_series = equity_series.loc[common_dates]
        csi_all_index = csi_all_index.loc[common_dates]
        market_equal_weight = market_equal_weight.loc[common_dates]
        
        metrics = calculate_metrics(equity_series, csi_all_index, params.initial_capital)
        
        first_stock = close_df.columns[0]
        first_stock_prices = close_df[first_stock].loc[common_dates]
        candles = convert_to_candles_format(first_stock_prices)
        equity_data = convert_equity_to_format(equity_series)
        csi_all_data = convert_equity_to_format(csi_all_index)
        equal_weight_data = convert_equity_to_format(market_equal_weight)
        
        formatted_trades = []
        for trade in trades:
            formatted_trades.append({
                "week": trade["week"],
                "t": int(trade["date"].timestamp() * 1000),
                "action": trade["action"],
                "stock": trade.get("stock", ""),
                "price": float(trade["price"]),
                "shares": int(trade["shares"]),
                "position_ratio": float(trade.get("position_ratio", 0)),
                "cash": float(trade["cash"]),
                "equity": float(trade["equity"]),
                "note": trade.get("note", "")
            })
        
        return {
            "success": True,
            "data": {
                "candles": candles,
                "equity": equity_data,
                "csi_all": csi_all_data,
                "market_equal_weight": equal_weight_data,
                "trades": formatted_trades,
                "metrics": metrics
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
