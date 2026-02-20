import pandas as pd
import os

data_dir = 'data'
files = ['close_day.csv', 'amt_day.csv', 'turn_day.csv', 'pb_lf_day.csv', 'cs_indus_code_day.csv', 'IPO_date_info.csv', 'delist_date_info.csv']

for f in files:
    print('=' * 60)
    print(f'文件: {f}')
    print('=' * 60)
    df = pd.read_csv(os.path.join(data_dir, f))
    print(f'形状: {df.shape}')
    print(f'列名: {df.columns.tolist()}')
    print()
    print('前3行数据:')
    print(df.head(3).T)  # 转置显示，便于看列
    print()
