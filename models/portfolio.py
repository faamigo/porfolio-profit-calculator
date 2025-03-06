from datetime import date
from typing import List, Tuple
import logging

from exceptions.price_exceptions import PriceNotFoundError
from logging_config import configure_logging
from models.position import Position

configure_logging()


class Portfolio:
    def __init__(self, name: str, positions: List[Position]):
        self.name = name
        self.positions = positions

    def validate_dates(self, start_date: date, end_date: date):
        if end_date > date.today():
            raise ValueError(f'The end date {end_date} cannot be later than today '
                             f'({date.today()}).')

        if start_date >= end_date:
            raise ValueError(f'The start date {start_date} must be earlier than '
                             f'the end date {end_date}.')

    def calculate_total_value(self, start_date: date, end_date: date) -> Tuple[float]:
        if not self.positions:
            logging.error('Attempted to calculate profit on an empty portfolio.')
            raise ValueError('The portfolio is empty.')

        initial_value = final_value = 0
        valid_stocks_count = 0

        for position in self.positions:
            try:
                start_position = position.value(start_date)
                final_position = position.value(end_date)

                initial_value += start_position
                final_value += final_position

                valid_stocks_count += 1

            except PriceNotFoundError as error:
                logging.warning('Excluding stock %s from total value'
                                'calculation due to missing price data: %s', 
                                position.stock.symbol, error)

        if valid_stocks_count == 0:
            raise ValueError('No valid prices were obtained for any stock on the specified dates.')

        return (initial_value, final_value)

    def profit(self, start_date: date, end_date: date, annualized=False) -> float:
        self.validate_dates(start_date, end_date)

        initial_value, final_value = self.calculate_total_value(start_date, end_date)
        profit = final_value - initial_value

        if not annualized:
            return round(profit, 2)

        if initial_value == 0:
            logging.error('The initial value of the portfolio is zero. '
                          'Cannot calculate annualized return.')

            raise ValueError('The initial value of the portfolio cannot be zero.')

        years = (end_date - start_date).days / 365
        annualized_return = (final_value / initial_value) ** (1 / years) - 1

        return round(annualized_return, 4)
