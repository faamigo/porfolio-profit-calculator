import unittest
from datetime import date, timedelta
from models.position import Position
from models.stock import Stock
from models.portfolio import Portfolio

class TestPortfolio(unittest.TestCase):
    def setUp(self):
        self.stock1 = Stock('AAPL', {date(2022, 12, 31): 100, date(2023, 12, 31): 120})
        self.stock2 = Stock('GOOGL', {date(2022, 12, 31): 50, date(2023, 12, 31): 60})
        self.stock3 = Stock('MSFT', {date(2022, 12, 31): 75})

        self.portfolio = Portfolio('Tech Stocks', [
            Position(self.stock1, 10),
            Position(self.stock2, 5),
            Position(self.stock3, 2)
        ])

    ### Tests profit

    def test_calculate_profit(self):
        profit = self.portfolio.profit(date(2022, 12, 31), date(2023, 12, 31))
        self.assertEqual(profit, 250.0)

    def test_calculate_annualized_return(self):
        annualized_return = self.portfolio.profit(date(2022, 12, 31),
                                                  date(2023, 12, 31), annualized=True)
        self.assertEqual(annualized_return, 0.2)

    def test_all_stocks_zero_start_value(self):
        msft = Stock('MSFT', {date(2024, 1, 1): 0, date(2025, 1, 1): 100})
        portfolio = Portfolio('Zero Start Value Portfolio', [
            Position(msft, 1)
        ])

        with self.assertRaises(ValueError) as context:
            portfolio.profit(date(2024, 1, 1), date(2025, 1, 1), annualized=True)
        self.assertEqual(str(context.exception),
                         'The initial value of the portfolio cannot be zero.')

    ### Tests calculate_total_value

    def test_calculate_total_value(self):
        initial_value, final_value = self.portfolio.calculate_total_value(date(2022, 12, 31),
                                                                          date(2023, 12, 31))
        self.assertEqual(initial_value, 1250)
        self.assertEqual(final_value, 1500)

    def test_calculate_total_value_missing_price(self):
        stock4 = Stock('TSLA', {})
        portfolio = Portfolio('Empty Portfolio', [
            Position(stock4, 1)
        ])

        with self.assertRaises(ValueError) as context:
            portfolio.calculate_total_value(date(2022, 12, 31), date(2023, 12, 31))
        self.assertEqual(str(context.exception),
                         'No valid prices were obtained for any stock on the specified dates.')

    def test_stock_with_price_only_in_start_or_end_date(self):
        stock_only_start = Stock('TSLA', {date(2022, 12, 31): 100})
        stock_only_end = Stock('AMZN', {date(2023, 12, 31): 200})

        portfolio = Portfolio('Partial Portfolio', [
            Position(stock_only_start, 1),
            Position(stock_only_end, 1)
        ])

        with self.assertRaises(ValueError) as context:
            portfolio.calculate_total_value(date(2022, 12, 31), date(2023, 12, 31))

        self.assertEqual(str(context.exception),
                         'No valid prices were obtained for any stock on the specified dates.')

    def test_calculate_total_value_empty_portfolio(self):
        empty_portfolio = Portfolio('Empty Portfolio', [])
        with self.assertRaises(ValueError) as context:
            empty_portfolio.calculate_total_value(date(2022, 12, 31), date(2023, 12, 31))
        self.assertEqual(str(context.exception), 'The portfolio is empty.')

    ### Tests validate_dates

    def test_validate_dates_future_end_date(self):
        future_date = date.today() + timedelta(days=1)
        with self.assertRaises(ValueError) as context:
            self.portfolio.validate_dates(date(2022, 12, 31), future_date)
        self.assertEqual(str(context.exception),
                         f'The end date {future_date} cannot be later than today ({date.today()}).')

    def test_validate_dates_invalid_start_date(self):
        with self.assertRaises(ValueError) as context:
            self.portfolio.validate_dates(date(2024, 1, 1), date(2023, 1, 1))
        self.assertEqual(str(context.exception),
                         f'The start date {date(2024, 1, 1)} must be earlier '
                         f'than the end date {date(2023, 1, 1)}.')

        with self.assertRaises(ValueError) as context:
            self.portfolio.validate_dates(date(2023, 1, 1), date(2023, 1, 1))
        self.assertEqual(str(context.exception),
                         f'The start date {date(2023, 1, 1)} must be earlier '
                         f'than the end date {date(2023, 1, 1)}.')


if __name__ == '__main__':
    unittest.main()
