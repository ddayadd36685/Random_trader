import pandas as pd
import os

data_dir = 'data'
files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]

print('数据文件列表:')
print(files)
print()

results = {}

for f in files:
    df = pd.read_csv(os.path.join(data_dir, f))
    results[f] = {
        'shape': df.shape,
        'columns': df.columns.tolist(),
        'head': df.head(3).to_string()
    }

for f, info in results.items():
    print(f'=== {f} ===')
    print(f'形状: {info["shape"]}')
    print(f'列名: {info["columns"]}')
    print(f'前3行:')
    print(info['head'])
    print()
