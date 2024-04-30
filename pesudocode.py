

# grab code that is ready to sample

# cache the sampling function so that it only runs on button press


# sample stocks using n=12*80
# don't set random state so that each refresh gets new sample

# do all the fixing to make it work (I assume you have the pseduocode for this)
# because it's taken from build sample


# set the returns dataframe equal to the prepared sample


# set up sidebar
# ask user input for investment parameters
# income, household size, expected death date, etc

# assign risk aversion and inheritance utility parameters based on low, medium , high responses

# next we edit the submitted parameters to make them work more nicely with data
# dividing stuff by 12 to make it monthly
# we dividing rates by 12 and then using them introduces compounding issues
# but I don't care and don't want to work on fixing that

# rename ETF column to Portfolio because Im lazy and dont want to change input file

# initialize income column to put in expected income of respondent

# create a list of expected incomes and then map it to the dataframe based on given savings start and retirement start data

# next define utility functions to be used in determining portfolio utility

# also initialize savings/utility columns to store in df

# initialize a bunch of dicts we use to store values

# final_utility is utility of each portfolio a t=death
# consumption dict is the initial consumption for each portolio
# capture only initial consumption for each portfolio because later consumption is just a function of inflation increases
# drawdown_dict is True for each portfolio then False if it hits the set drawdown limit defined in risk aversion parameter




# Do a nested for loop to estimate the savings/utility/consumption for each portfolio based on given parameters
# first for loop is basically for each portfolio
# second for loop is for each row in the given portfolio
# does a bunch of checks on what time it is and assigns values to each column based on the month variable
# the if row['income'] == 0.0 and row['month'] > month_retirement_start and row['month'] < death_month
# could probably be modified to removed the row income part but I don't want to touch anything cause im scared itll break

# max_key is the portfolio with highest utility


# Next we do plotting
# we use plotly graph objects because it makes it easier to combine different lines
# plot savings for portfolio if it meets highest utility and drawdown and line in red
# otherwise line in red for highest utility
# an another line for highest utility that also meets drawdown requiremnts but in blue
# every other line is grey

# each other tab just shows a solo plot for each graph
# I'd like to provide more summary statistics on each portfolio so this is subject to change