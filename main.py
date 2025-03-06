from datetime import date
from models.stock import Stock
from models.portfolio import Portfolio
from models.position import Position


def main():
    apple = Stock('AAPL', {date(2022, 12, 31): 100, date(2023, 12, 31): 120})
    google = Stock('GOOGL', {date(2022, 12, 31): 50, date(2023, 12, 31): 60})
    msft = Stock('MSFT', {date(2022, 12, 31): 75})

    portfolio = Portfolio('Tech Stocks', [
            Position(apple, 10),
            Position(google, 5),
            Position(msft, 2)
        ])

    start_date = date(2022, 12, 31)
    end_date = date(2023, 12, 31)

    try:
        annualized_return = portfolio.profit(start_date, end_date, True)
        print(f'Annualized return of portfolio {portfolio.name} between {start_date} and'
              f'{end_date}: {annualized_return:.2%}\n')

        profit = portfolio.profit(start_date, end_date)
        print(f'Profit of portfolio {portfolio.name} between {start_date} and'
              f'{end_date}: ${profit:.2f}')

    except ValueError as error:
        print(f'Error calculating profit: {error}')


if __name__ == "__main__":
    main()
