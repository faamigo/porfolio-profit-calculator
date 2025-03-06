import unittest
from datetime import date, timedelta
from models.stock import Stock, PriceNotFoundError

class TestStock(unittest.TestCase):
    def setUp(self):
        self.prices = {
            date(2023, 1, 1): 100.0,
            date(2023, 12, 31): 120.0
        }
        self.stock = Stock('AAPL', self.prices)

    ### Tests price

    def test_price_valid_date(self):
        price = self.stock.price(date(2023, 1, 1))
        self.assertEqual(price, 100.0)

    def test_price_invalid_date(self):
        with self.assertRaises(PriceNotFoundError) as context:
            self.stock.price(date(2023, 6, 15))
        self.assertEqual(str(context.exception), f'No price found for AAPL on {date(2023, 6, 15)}.')

    def test_price_future_date(self):
        future_date = date.today() + timedelta(days=1)
        with self.assertRaises(ValueError) as context:
            self.stock.price(future_date)
        self.assertEqual(str(context.exception),
                         f'The entered date {future_date} cannot be later '
                         f'than today ({date.today()}).')


if __name__ == '__main__':
    unittest.main()
