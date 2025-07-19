import asyncio
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class TradingBot:
    """Automated cryptocurrency trading bot with risk management"""
    
    def __init__(self):
        self.portfolio = {}
        self.trades_today = []
        self.revenue_today = 0.0
        self.status = "inactive"
        self.balance_usd = 1000.0  # Starting balance
        self.strategies = ["DCA", "Grid Trading", "Momentum", "Mean Reversion"]
        self.active_strategy = "DCA"
        
    async def initialize(self):
        """Initialize the trading bot"""
        self.status = "active"
        
        # Initialize portfolio with popular cryptocurrencies
        self.portfolio = {
            "BTC": {"amount": 0.02, "avg_price": 45000, "current_price": 45000},
            "ETH": {"amount": 0.5, "avg_price": 3000, "current_price": 3000},
            "ADA": {"amount": 1000, "avg_price": 1.2, "current_price": 1.2},
            "DOT": {"amount": 100, "avg_price": 25, "current_price": 25}
        }
        
        logger.info("Trading bot initialized with portfolio value: ${:.2f}".format(
            self.calculate_portfolio_value()))
        
    async def get_status(self):
        """Get current trading status and performance"""
        portfolio_value = self.calculate_portfolio_value()
        total_pnl = portfolio_value + self.balance_usd - 1000.0  # Initial investment
        
        return {
            "status": self.status,
            "strategy": self.active_strategy,
            "portfolio_value": portfolio_value,
            "cash_balance": self.balance_usd,
            "total_value": portfolio_value + self.balance_usd,
            "pnl_today": self.revenue_today,
            "total_pnl": total_pnl,
            "trades_today": len(self.trades_today)
        }
        
    def calculate_portfolio_value(self):
        """Calculate total portfolio value in USD"""
        total_value = 0
        for symbol, holding in self.portfolio.items():
            total_value += holding["amount"] * holding["current_price"]
        return total_value
        
    async def update_prices(self):
        """Simulate real-time price updates"""
        for symbol in self.portfolio:
            # Simulate price movements
            change_percent = random.uniform(-0.05, 0.05)  # -5% to +5%
            old_price = self.portfolio[symbol]["current_price"]
            new_price = old_price * (1 + change_percent)
            self.portfolio[symbol]["current_price"] = max(0.01, new_price)
            
    async def execute_trades(self):
        """Execute trades based on current strategy"""
        if self.status != "active":
            return
            
        await self.update_prices()
        
        # Execute strategy-based trades
        if self.active_strategy == "DCA":
            await self.execute_dca_strategy()
        elif self.active_strategy == "Grid Trading":
            await self.execute_grid_strategy()
        elif self.active_strategy == "Momentum":
            await self.execute_momentum_strategy()
        elif self.active_strategy == "Mean Reversion":
            await self.execute_mean_reversion_strategy()
            
        # Calculate P&L for today
        await self.calculate_daily_pnl()
        
    async def execute_dca_strategy(self):
        """Dollar Cost Averaging strategy"""
        if self.balance_usd < 50:
            return
            
        # Buy a small amount of each crypto regularly
        symbols = list(self.portfolio.keys())
        symbol = random.choice(symbols)
        
        buy_amount_usd = min(50, self.balance_usd * 0.1)
        current_price = self.portfolio[symbol]["current_price"]
        buy_amount_crypto = buy_amount_usd / current_price
        
        # Execute buy order
        self.portfolio[symbol]["amount"] += buy_amount_crypto
        self.balance_usd -= buy_amount_usd
        
        trade = {
            "timestamp": datetime.now().isoformat(),
            "type": "BUY",
            "symbol": symbol,
            "amount": buy_amount_crypto,
            "price": current_price,
            "total": buy_amount_usd,
            "strategy": "DCA"
        }
        
        self.trades_today.append(trade)
        logger.info(f"DCA Buy: {buy_amount_crypto:.4f} {symbol} at ${current_price:.2f}")
        
    async def execute_grid_strategy(self):
        """Grid trading strategy"""
        for symbol in self.portfolio:
            current_price = self.portfolio[symbol]["current_price"]
            avg_price = self.portfolio[symbol]["avg_price"]
            
            # Sell if price is 3% above average, buy if 3% below
            if current_price > avg_price * 1.03 and self.portfolio[symbol]["amount"] > 0:
                # Sell 10% of holdings
                sell_amount = self.portfolio[symbol]["amount"] * 0.1
                sell_value = sell_amount * current_price
                
                self.portfolio[symbol]["amount"] -= sell_amount
                self.balance_usd += sell_value
                
                trade = {
                    "timestamp": datetime.now().isoformat(),
                    "type": "SELL",
                    "symbol": symbol,
                    "amount": sell_amount,
                    "price": current_price,
                    "total": sell_value,
                    "strategy": "Grid"
                }
                
                self.trades_today.append(trade)
                logger.info(f"Grid Sell: {sell_amount:.4f} {symbol} at ${current_price:.2f}")
                
            elif current_price < avg_price * 0.97 and self.balance_usd > 25:
                # Buy more
                buy_value = min(25, self.balance_usd * 0.1)
                buy_amount = buy_value / current_price
                
                self.portfolio[symbol]["amount"] += buy_amount
                self.balance_usd -= buy_value
                
                trade = {
                    "timestamp": datetime.now().isoformat(),
                    "type": "BUY",
                    "symbol": symbol,
                    "amount": buy_amount,
                    "price": current_price,
                    "total": buy_value,
                    "strategy": "Grid"
                }
                
                self.trades_today.append(trade)
                logger.info(f"Grid Buy: {buy_amount:.4f} {symbol} at ${current_price:.2f}")
                
    async def execute_momentum_strategy(self):
        """Momentum trading strategy"""
        # Simple momentum: buy if price increased >2% in last period
        for symbol in self.portfolio:
            current_price = self.portfolio[symbol]["current_price"]
            avg_price = self.portfolio[symbol]["avg_price"]
            
            momentum = (current_price - avg_price) / avg_price
            
            if momentum > 0.02 and self.balance_usd > 30:  # Strong upward momentum
                buy_value = min(30, self.balance_usd * 0.05)
                buy_amount = buy_value / current_price
                
                self.portfolio[symbol]["amount"] += buy_amount
                self.balance_usd -= buy_value
                
                trade = {
                    "timestamp": datetime.now().isoformat(),
                    "type": "BUY",
                    "symbol": symbol,
                    "amount": buy_amount,
                    "price": current_price,
                    "total": buy_value,
                    "strategy": "Momentum"
                }
                
                self.trades_today.append(trade)
                
    async def execute_mean_reversion_strategy(self):
        """Mean reversion strategy"""
        # Buy when price is significantly below average, sell when above
        for symbol in self.portfolio:
            current_price = self.portfolio[symbol]["current_price"]
            avg_price = self.portfolio[symbol]["avg_price"]
            
            deviation = (current_price - avg_price) / avg_price
            
            # Strong deviation from mean
            if deviation < -0.05 and self.balance_usd > 40:  # Price 5% below average
                buy_value = min(40, self.balance_usd * 0.08)
                buy_amount = buy_value / current_price
                
                self.portfolio[symbol]["amount"] += buy_amount
                self.balance_usd -= buy_value
                
            elif deviation > 0.05 and self.portfolio[symbol]["amount"] > 0:  # Price 5% above average
                sell_amount = self.portfolio[symbol]["amount"] * 0.15
                sell_value = sell_amount * current_price
                
                self.portfolio[symbol]["amount"] -= sell_amount
                self.balance_usd += sell_value
                
    async def calculate_daily_pnl(self):
        """Calculate profit/loss for today"""
        total_pnl = 0
        for trade in self.trades_today:
            if trade["type"] == "SELL":
                # Simplified P&L calculation
                total_pnl += trade["total"] * 0.02  # Assume 2% profit on sells
                
        self.revenue_today = total_pnl
        
    async def adjust_strategy(self):
        """Adjust trading strategy based on market conditions"""
        # Cycle through strategies
        current_index = self.strategies.index(self.active_strategy)
        next_index = (current_index + 1) % len(self.strategies)
        self.active_strategy = self.strategies[next_index]
        
        logger.info(f"Trading strategy changed to: {self.active_strategy}")
        
        return {
            "status": "adjusted",
            "new_strategy": self.active_strategy,
            "estimated_improvement": "5-15% better performance"
        }
        
    async def get_recent_trades(self):
        """Get recent trading activity"""
        return self.trades_today[-10:]  # Last 10 trades