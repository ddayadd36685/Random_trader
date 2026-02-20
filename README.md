# 🎲 Random Trader vs Index

随机交易员大战大盘 - 一个可视化量化策略演示系统

## 项目简介

本项目用中国A股历史数据，模拟"每周随机买入/卖出"的交易策略，并通过网页动画可视化展示：
- 📊 K线蜡烛图
- 📈 随机策略净值曲线（金色）
- 📉 基准指数/买入持有净值曲线（蓝色）
- 🎬 每周交易动画（买卖标记、卡片）
- 🏆 最终收益对比（是否跑赢大盘）

## 技术栈

- **后端**: Python + FastAPI
- **前端**: HTML + 原生 JavaScript
- **图表库**: TradingView Lightweight Charts
- **动画**: requestAnimationFrame

## 项目结构

```
random_trade/
├── backend/
│   ├── __init__.py
│   ├── main.py           # FastAPI主入口
│   ├── data_loader.py    # 数据加载模块
│   ├── strategy.py       # 随机策略引擎
│   └── metrics.py        # 指标计算模块
├── frontend/
│   └── index.html        # 前端页面
├── data/                 # 股票数据目录
├── requirements.txt      # Python依赖
├── start.py             # 启动脚本
└── README.md
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动服务

```bash
python start.py
```

或者直接运行：

```bash
python -m uvicorn backend.main:app --reload
```

### 3. 打开浏览器

访问 `http://localhost:8000`

## 功能特性

### 🎛️ 策略参数

- **初始资金**: 设置初始投资金额
- **买入概率**: 每周买入的概率（0-100%）
- **卖出概率**: 每周卖出的概率（0-100%）
- **手续费**: 交易手续费（bps）
- **随机种子**: 可选，用于复现某次模拟

### 🎬 播放控制

- **播放/暂停**: 控制动画播放
- **上一周/下一周**: 逐周查看
- **播放速度**: 0.5x / 1x / 2x / 4x
- **进度条**: 拖动跳转到任意位置

### 📊 指标展示

- 当前日期
- 总资产
- 策略收益
- 基准收益
- 总收益、年化、最大回撤等

### 🏆 结算面板

- 跑赢/跑输大盘的大字展示
- 完整指标卡片
- 胜利时的彩纸效果

## 使用流程

1. **设置参数**: 在右侧面板调整策略参数
2. **运行模拟**: 点击"🚀 开始模拟"
3. **观看动画**: 点击"▶️"播放，观察净值曲线变化
4. **查看结果**: 动画结束后查看结算面板

## API 接口

### `POST /api/run-strategy`

运行随机策略模拟

**请求体**:
```json
{
  "initial_capital": 100000,
  "buy_prob": 0.4,
  "sell_prob": 0.4,
  "hold_prob": 0.2,
  "commission_bps": 5,
  "seed": 42
}
```

**响应**:
```json
{
  "success": true,
  "data": {
    "candles": [...],
    "equity": [...],
    "benchmark": [...],
    "trades": [...],
    "metrics": {...}
  }
}
```

## 数据说明

数据位于 `data/` 目录，包含：
- `close_adj_day.csv`: 复权收盘价
- `amt_day.csv`: 成交额
- 等等...

详见 `股票数据介绍.md`

## 注意事项

- 本项目仅用于教学和演示目的
- 随机策略不构成任何投资建议
- 历史表现不代表未来收益

## License

MIT
