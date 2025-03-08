# Portfolio Profit Calculator

## Overview

This project is a simple portfolio profit calculator system, designed to calculate the profit and annualized return of a portfolio between two specified dates. The system is built using Python and includes classes for `Stock`, `Position`, and `Portfolio`. The `Portfolio` class manages a collection of positions (stocks with quantities) and provides methods to calculate the total value, profit, and annualized return of the portfolio.

## Features

- **Stock Class**: Represents a stock with a symbol and price history.
- **Position Class**: Represents a position in a portfolio, consisting of a stock and the number of shares.
- **Portfolio Class**: Manages a collection of positions and provides methods to calculate the total value, profit, and annualized return of the portfolio.
- **Profit Calculation**: Calculates the profit of the portfolio between two specified dates. Optionally calculates the annualized return of the portfolio if `annualized=True`.
- **Date Validation**: Ensures that the provided dates are valid and within acceptable ranges.
- **Error Handling**: Includes custom exceptions and logging for error handling.

## Assumptions

1.  **Whole shares**: The shares are whole and not fractional.
    
2.  **Purchase date**: The stock was purchased before or on the start date of the profit calculation period.

3.  **No sales**: No shares have been sold since they were purchased.
    
4.  **Stocks uniqueness**: Each stock in the portfolio is unique.

## Execution

The project includes a main script that can be executed to run the portfolio profit calculator. To run the main script, use the following command in the project root:

```bash
python3 main.py
```

## Testing
The project includes a suite of tests to ensure the correctness of the  `Stock`,  `Position`, and  `Portfolio`  classes and their methods. To run the tests, use the following command in the project root:

```bash
python3 -m unittest discover -s tests
```
