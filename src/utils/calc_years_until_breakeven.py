
def calc_years_until_breakeven(years, profits):
    """Takes a list of years and a list of total profits as input and returns a float value
    for the expected amount of years until breakeven on an investment"""
    
    # Find the index where the profit crosses zero
    negative_index = next((i for i, profit in enumerate(profits) if profit < 0), None)
    positive_index = next((i for i, profit in enumerate(profits) if profit >= 0), None)

    try: 
        correct_input = negative_index is not None and positive_index is not None

        if not correct_input:
            raise ValueError("Couldn't find a positive and negative index from the input lists")

    except ValueError as e:
        print(f"An error occurred: {e}")

    else:
        # Linear interpolation to estimate the year when profit becomes zero
        x1, x2 = profits[negative_index], profits[positive_index]
        year_at_zero_profit = years[negative_index] + (years[positive_index] - years[negative_index]) * (0 - x1) / (x2 - x1)
        return float(f"{year_at_zero_profit - years[0]:.1f}")
        # return f"{year_at_zero_profit - years[0]:.1f}"


if __name__=='__main__':

    years = [2010, 2011, 2012, 2013, 2014, 2015]
    profits = [-5000, -3000, -1000, 500, 2000, 4000]

    print(calc_years_until_breakeven(years, profits))