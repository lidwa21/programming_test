import numpy as np
import pandas as pd

# Logic


def check_uniqueness(lst):
    """
    Check if a list contains only unique values.
    Returns True only if all values in the list are unique, False otherwise
    """
    nb_unique_elements  = len(set(lst)) # we get the number of unique values
    if nb_unique_elements == len(lst):
        return True
    else :
        return False


def smallest_difference(array):
    """
    Code a function that takes an array and returns the smallest
    absolute difference between two elements of this array
    Please note that the array can be large and that the more
    computationally efficient the better
    """
    
    flat_array = array.flatten() # we flatten the array to have a (n,) dimension
    flat_array = np.array(sorted(flat_array)) # we sort the flat array in ascending order and make sure the result is an array 
    
    consecutive_differences = flat_array[1:] - flat_array[:-1] # we calculate the differences of side by side elements 
    
    return(min(consecutive_differences))


# Finance and DataFrame manipulation


def macd(prices, window_short=12, window_long=26):
    """
    Code a function that takes a DataFrame named prices and
    returns it's MACD (Moving Average Convergence Difference) as
    a DataFrame with same shape
    Assume simple moving average rather than exponential moving average
    The expected output is in the output.csv file
    """
    numerical_col_names = prices.select_dtypes(include=np.number).columns # we select only the cumerical columns
    df_result = pd.DataFrame()
    for col_name in numerical_col_names:
        df_result["MACD "+col_name] = prices[col_name].rolling(window=window_short).mean() - prices[col_name].rolling(window=window_long).mean()
    
    return df_result
    


def sortino_ratio(prices):
    """
    Code a function that takes a DataFrame named prices and
    returns the Sortino ratio for each column
    Assume risk-free rate = 0
    On the given test set, it should yield 0.05457
    """
    risk_free_rate = 0
    prices = prices.select_dtypes(include=np.number) # we select only numerical columns
    returns = prices.pct_change() # the calculate the returns for all columns
    returns = returns.dropna()
    
    def downside_deviation(x):
        return np.std(np.minimum(0,x))
    
    def daily_retun_2_annual(x):
        cumulative_return = (x+1).prod()
        ann_return = cumulative_return**(252/len(x)) - 1 # 252 number of open days in a year
        return ann_return
    
    result = returns.apply(lambda x: (daily_retun_2_annual(x) - risk_free_rate)/downside_deviation(x), axis=0) # we calculathe the ratio
    #################### Important 
    ##  The resulting values is not the one expected. I must have implemented a wrong formula for the downside deviation. It might also be due to considering annual returns
    return result


def expected_shortfall(prices, level=0.95):
    """
    Code a function that takes a DataFrame named prices and
    returns the expected shortfall at a given level
    On the given test set, it should yield -0.03468
    """ 
    prices = prices.select_dtypes(include=np.number) # we select only the cumerical columns
    returns = prices.pct_change() # we calculate the returns for each column
    returns = returns.dropna()
    n_col = prices.shape[1]
    ES = np.zeros(n_col)
    for i in range(n_col): # we calculate the ES for each column
        selected_column = returns.iloc[:,i]
        worst_returns = selected_column[selected_column < selected_column.quantile(1-level)]
        ES[i] = np.mean(worst_returns)
    return ES


# Plot


def visualize(prices, path, plot_name = "SX5T Index", plot_type = ".pdf"):
    """
    Code a function that takes a DataFrame named prices and
    saves the plot to the given path
    """
    
    prices_plot = prices.select_dtypes(include=np.number) # we select only the cumerical columns
    prices_plot.plot(figsize=(8,6))
    plt.legend()
    plt.savefig(path+"/"+plot_name+plot_type)
