import pandas as pd
import os

data_dir = 'data'
files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]

print('=' * 80)
print('股票数据概览')
print('=' * 80)
print()

for f in files:
    df = pd.read_csv(os.path.join(data_dir, f))
    print(f'文件: {f}')
    print(f'  形状: {df.shape[0]} 行 × {df.shape[1]} 列')
    print(f'  列名: {df.columns.tolist()}')
    if not df.empty:
        print(f'  时间范围: {df.iloc[:, 0].min()} 至 {df.iloc[:, 0].max()}')
    print()
