import pandas as pd
from pathlib import Path

data_path = Path("data")
close_df = pd.read_csv(data_path / "close_adj_day.csv", index_col=0, parse_dates=True)

print("Columns in close_adj_day.csv:")
print(close_df.columns.tolist()[:20])
print(f"\nTotal columns: {len(close_df.columns)}")
