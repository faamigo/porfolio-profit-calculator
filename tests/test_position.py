import unittest
from datetime import date, timedelta
from exceptions.exceptions import PriceNotFoundError
from models.stock import Stock
from models.position import Position

class TestPosition(unittest.TestCase):
    def setUp(self):
        self.stock_aapl = Stock('AAPL', {date(2022, 12, 31): 150, date(2023, 12, 31): 175})
        self.stock_googl = Stock('GOOGL', {date(2022, 12, 31): 100, date(2023, 12, 31): 120})

    ### Tests init

    def test_position_creation_valid_quantity(self):
        position = Position(self.stock_aapl, 10)
        self.assertEqual(position.stock.symbol, 'AAPL')
        self.assertEqual(position.shares, 10)

    def test_position_creation_invalid_quantity_zero(self):
        with self.assertRaises(ValueError) as context:
            Position(self.stock_aapl, 0)
        self.assertEqual(str(context.exception), 'Shares must be greater than zero.')

    def test_position_creation_invalid_quantity_negative(self):
        with self.assertRaises(ValueError) as context:
            Position(self.stock_aapl, -5)
        self.assertEqual(str(context.exception), 'Shares must be greater than zero.')

    ### Tests value

    def test_value_with_valid_price(self):
        position = Position(self.stock_aapl, 10)
        calculated_value = position.value(date(2022, 12, 31))
        self.assertEqual(calculated_value, 1500)

    def test_value_with_non_existing_date(self):
        position = Position(self.stock_googl, 20)
        with self.assertRaises(PriceNotFoundError) as context:
            position.value(date(2024, 1, 1))
        self.assertEqual(str(context.exception), f'No price found for GOOGL on {date(2024, 1, 1)}.')

    def test_value_with_future_date(self):
        position = Position(self.stock_aapl, 10)
        future_date = date.today() + timedelta(days=1)
        with self.assertRaises(ValueError) as context:
            position.value(future_date)
        self.assertEqual(str(context.exception), f'The entered date {future_date} cannot be later '
                         f'than today ({date.today()}).')


if __name__ == "__main__":
    unittest.main()
