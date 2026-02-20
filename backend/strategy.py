import pandas as pd
import numpy as np
from typing import List, Dict, Tuple
import random


class RandomTrader:
    def __init__(
        self,
        initial_capital: float = 100000,
        buy_prob: float = 0.4,
        sell_prob: float = 0.4,
        hold_prob: float = 0.2,
        min_position_ratio: float = 0.2,
        max_position_ratio: float = 0.8,
        commission_bps: float = 5,
        seed: int = None
    ):
        self.initial_capital = initial_capital
        self.buy_prob = buy_prob
        self.sell_prob = sell_prob
        self.hold_prob = hold_prob
        self.min_position_ratio = min_position_ratio
        self.max_position_ratio = max_position_ratio
        self.commission_bps = commission_bps
        
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
        
        self.cash = initial_capital
        self.positions: Dict[str, float] = {}
        self.equity_history = []
        self.trades = []
    
    def _get_action(self) -> str:
        actions = ["BUY", "SELL", "HOLD"]
        probs = [self.buy_prob, self.sell_prob, self.hold_prob]
        return random.choices(actions, weights=probs, k=1)[0]
    
    def _get_random_position_ratio(self) -> float:
        return random.uniform(self.min_position_ratio, self.max_position_ratio)
    
    def _calculate_transaction_cost(self, amount: float) -> float:
        commission = amount * (self.commission_bps / 10000)
        return commission
    
    def _get_total_equity(self, current_prices: Dict[str, float]) -> float:
        position_value = 0
        for stock_code, shares in self.positions.items():
            if stock_code in current_prices and not pd.isna(current_prices[stock_code]):
                position_value += shares * current_prices[stock_code]
        return self.cash + position_value
    
    def run(self, close_df: pd.DataFrame, weekly_dates: pd.DatetimeIndex) -> Tuple[List[Dict], pd.Series]:
        self.cash = self.initial_capital
        self.positions = {}
        self.equity_history = []
        self.trades = []
        
        weekly_date_set = set(weekly_dates)
        all_stocks = close_df.columns.tolist()
        
        for idx, row in close_df.iterrows():
            current_prices = row.to_dict()
            
            if idx in weekly_date_set:
                valid_stocks = [s for s in all_stocks if not pd.isna(current_prices.get(s)) and current_prices.get(s, 0) > 0]
                
                if valid_stocks:
                    action = self._get_action()
                    selected_stock = random.choice(valid_stocks)
                    stock_price = current_prices[selected_stock]
                    
                    trade = {
                        "week": idx.strftime("%Y-W%W"),
                        "date": idx,
                        "action": action,
                        "stock": selected_stock,
                        "price": stock_price,
                        "shares": 0,
                        "position_ratio": 0,
                        "cash": self.cash,
                        "equity": self._get_total_equity(current_prices)
                    }
                    
                    if action == "BUY":
                        position_ratio = self._get_random_position_ratio()
                        amount_to_invest = self.cash * position_ratio
                        
                        if amount_to_invest > 0 and stock_price > 0:
                            shares_to_buy = int(amount_to_invest / stock_price)
                            if shares_to_buy > 0:
                                cost = shares_to_buy * stock_price
                                commission = self._calculate_transaction_cost(cost)
                                total_cost = cost + commission
                                
                                if total_cost <= self.cash:
                                    if selected_stock in self.positions:
                                        self.positions[selected_stock] += shares_to_buy
                                    else:
                                        self.positions[selected_stock] = shares_to_buy
                                    self.cash -= total_cost
                                    trade["shares"] = shares_to_buy
                                    trade["position_ratio"] = position_ratio
                                else:
                                    trade["action"] = "HOLD"
                                    trade["note"] = "资金不足"
                    
                    elif action == "SELL":
                        if self.positions:
                            stocks_to_sell = list(self.positions.keys())
                            if stocks_to_sell:
                                stock_to_sell = random.choice(stocks_to_sell) if selected_stock not in self.positions else selected_stock
                                if stock_to_sell in self.positions and not pd.isna(current_prices.get(stock_to_sell)):
                                    sell_price = current_prices[stock_to_sell]
                                    shares_to_sell = self.positions[stock_to_sell]
                                    
                                    proceeds = shares_to_sell * sell_price
                                    commission = self._calculate_transaction_cost(proceeds)
                                    net_proceeds = proceeds - commission
                                    
                                    self.positions[stock_to_sell] -= shares_to_sell
                                    if self.positions[stock_to_sell] <= 0:
                                        del self.positions[stock_to_sell]
                                    self.cash += net_proceeds
                                    
                                    trade["stock"] = stock_to_sell
                                    trade["price"] = sell_price
                                    trade["shares"] = shares_to_sell
                    
                    trade["cash"] = self.cash
                    trade["equity"] = self._get_total_equity(current_prices)
                    self.trades.append(trade)
            
            total_equity = self._get_total_equity(current_prices)
            
            self.equity_history.append({
                "date": idx,
                "cash": self.cash,
                "positions": self.positions.copy(),
                "total_equity": total_equity
            })
        
        equity_series = pd.Series(
            [h["total_equity"] for h in self.equity_history],
            index=[h["date"] for h in self.equity_history],
            name="strategy_equity"
        )
        
        return self.trades, equity_series
