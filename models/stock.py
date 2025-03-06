from datetime import date
from exceptions.price_exceptions import PriceNotFoundError

class Stock:
    def __init__(self, symbol: str, price_history: dict[date, float]):
        self.symbol = symbol
        self.price_history = price_history

    def price(self, price_date: date) -> float:
        if price_date > date.today():
            raise ValueError(f'The entered date {price_date} cannot be later than '
                             f'today ({date.today()}).')

        if price_date not in self.price_history:
            raise PriceNotFoundError(f'No price found for {self.symbol} on {price_date}.')

        return self.price_history[price_date]
