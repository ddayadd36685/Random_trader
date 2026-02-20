import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.data_loader import load_sample_data, prepare_data_for_strategy
from backend.strategy import RandomTrader
from backend.metrics import calculate_metrics

print("Testing data loading...")
try:
    df, _ = load_sample_data()
    print(f"Data loaded successfully! Shape: {df.shape}")
    print(f"Index: {df.index[:5]}")
    
    daily_df, weekly_df = prepare_data_for_strategy(df)
    print(f"Daily df shape: {daily_df.shape}")
    print(f"Weekly df shape: {weekly_df.shape}")
    
    print("\nTesting strategy...")
    trader = RandomTrader(initial_capital=100000)
    trades, equity_series, benchmark_series = trader.run(daily_df, weekly_df)
    print(f"Strategy ran successfully! Trades: {len(trades)}")
    print(f"Equity series length: {len(equity_series)}")
    
    print("\nTesting metrics...")
    metrics = calculate_metrics(equity_series, benchmark_series, 100000)
    print(f"Metrics calculated: {metrics}")
    
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
