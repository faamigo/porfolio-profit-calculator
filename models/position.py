from datetime import date
from models.stock import Stock

class Position:
    def __init__(self, stock: Stock, shares: int):
        if shares <= 0:
            raise ValueError('Shares must be greater than zero.')

        self.stock = stock
        self.shares = shares

    def value(self, price_date: date) -> float:
        return self.stock.price(price_date) * self.shares
