# Build Sample
# download monthly Adj Close prices for our selected ETFs

# Import csv files into one df (format: tall df) - Drop unnecessary columns

# Calculate returns for each ETF

# Convert tall to wide df


# Dashboard
# Grab df from build sample

# Cache the sampling function so that it only runs on button press

# Sample stocks using n=12*80 (don't set random state so that each refresh gets new sample)

# Create adidtional portforlios

# Convert wide to tall df


# Set up sidebar
# Ask user input for investment parameters (income, household size, expected death date, etc)

# Assign risk aversion and inheritance utility parameters based on low, medium , high responses

# Edit the submitted parameters to make them work more nicely with data (dividing stuff by 12 to make it monthly)

# Rename ETF column to Portfolio

# Initialize income column to put in expected income of respondent

# Create a list of expected incomes and then map it to the dataframe based on given savings start and retirement start data

# Next define utility functions to be used in determining portfolio utility

# Also initialize savings/utility columns to store in df

# Initialize a bunch of dicts we use to store values

# Final_utility is utility of each portfolio at t=death
# Consumption dict is the initial consumption for each portolio
# Capture only initial consumption for each portfolio because later consumption is just a function of inflation
# Drawdown_dict is True for each portfolio then False if it hits the set drawdown limit defined in risk aversion parameter


# Do a nested for loop to estimate the savings/utility/consumption for each portfolio based on given parameters
# First for loop is basically for each portfolio
# Second for loop is for each row in the given portfolio
# does a bunch of checks on what time it is and assigns values to each column based on the month variable

# max_key is the portfolio with highest utility

# Next we do plotting
# we use plotly graph objects because it makes it easier to combine different lines
# plot savings for portfolio if it meets highest utility and drawdown and line in red
# otherwise line in red for highest utility
# an another line for highest utility that also meets drawdown requiremnts but in blue
# every other line is grey

# each other tab just shows a solo plot for each graph
