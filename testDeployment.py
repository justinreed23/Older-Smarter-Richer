import streamlit as st
import numpy as np
import pandas as pd
import datetime
import math
import plotly.express as px
import plotly.graph_objects as go


st.set_page_config(
    "Older, Smarter, Richer",
    "📈",
    initial_sidebar_state="expanded",
    layout="wide",
    menu_items={
        "Report a Bug" : 'https://github.com/justinreed23/Older-Smarter-Richer/issues',
        "About" : 'https://github.com/justinreed23/Older-Smarter-Richer/blob/main/README.md',
        "Get Help" : 'https://media.tenor.com/mZZoOtDcouoAAAAM/stop-it-get-some-help.gif'
    }
)

#############################################
# start: title
#############################################

"""
# CAPM Portfolio Optimization with Risk Aversion Adjustment: Find Your Optimal Investment Portfolio for Retirement by filling Out Our Survey!
"""

#############################################
# start: sidebar
#############################################

with st.sidebar:

    '''
    ## Financial Assessment
    
    ### Please answer the following questions about your financial situation
    '''
    
    submitted_income = st.number_input("What is your annual income?(Max $10mil)", min_value=0,max_value=10000000, value=65000)
    income_growth = st.slider("What is your expected annual income growth rate in percentage?", min_value=1.0, max_value=10.0, value=3.0, step=0.1) / 100
    start_savings = st.number_input("At what age did you start saving?", min_value=18, max_value=50, value=25)
    retirement_start = st.number_input("At what age will you retire?", min_value=50, max_value=80,value=65)
    death_year = st.number_input("At what age do you expect you will pass away?", min_value=retirement_start, max_value=100,value=85)
    household_size = st.number_input("Number of people in household at time of retirement?", min_value=1, max_value=10, value=2)
    
    save_rate = st.slider("What percent of your income do you expect to save annually?", min_value=5.0, max_value=40.0, value=10.0, step=0.1) / 100
    consumption_rate= st.slider("What percent of your income do you plan to spend annually in retirement? General investment advice is 4%", min_value=1.0, max_value=20.0, value=4.0, step=0.1) / 100
    risk_aversion_options = ["Low", "Medium", "High"]
    selected_risk_aversion = st.selectbox("Select your risk aversion level:", risk_aversion_options)

# Assigning values based on user selection
    if selected_risk_aversion == "Low":
        risk_aversion = 2.84
    elif selected_risk_aversion == "Medium":
        risk_aversion = 3.84
    else:
        risk_aversion = 4.84

    inher_util_options = ["None", "Low", "Medium", "High"]
    selected_inher_util = st.selectbox("Select your inheritance utility level:", inher_util_options)

# Assigning values based on user selection
    if selected_inher_util == "None":
        inher_util = 0
    elif selected_inher_util == "Low":
        inher_util = 1000
    elif selected_risk_aversion == "Medium":
        inher_util = 2360
    else:
        inher_util = 6000


#############################################
# create returns df, normally this is an import
#############################################

monthly_income = submitted_income/12
monthly_growth = 1+ (income_growth/12)
month_start_savings = start_savings*12
month_retirement_start = retirement_start*12
death_month = death_year*12
# maybe I should let them option this
inflation = 0.02
inflation_rate = inflation/12
inher_luxury = 490000

# this is probably shitty, reason I am doing this is we dont have infinite data and I dont want to fix the rest of my code
month_start_savings = 0
month_retirement_start = month_retirement_start - month_start_savings
death_month = death_month - month_start_savings





rng = np.random.default_rng(123)

start_year = 1950
end_year = 2050
portfolios = ["First", "Second", "Third", "Fourth", "Fifth"]
portfolios_list = []
dates_list = []


for portfolio in portfolios:
    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            date = datetime.date(year, month, 1)
            dates_list.append(date)
            portfolios_list.append(portfolio)

random_returns = rng.uniform(low=0, high=(0.10 / 12), size=len(dates_list))


returns = pd.DataFrame(
    {"Portfolio": portfolios_list, "date": dates_list, "ret": random_returns}
)


returns['income'] = 0.0


total_monthly_incomes = []

for t in returns.index[month_start_savings:month_retirement_start]:
    current_month = t-month_start_savings
    income_for_month = monthly_income*(monthly_growth**current_month)
    total_monthly_incomes.append(income_for_month)
    


# Apply mapping to DataFrame's index to create a month column that resets for each portfolio
returns['month'] = returns.groupby('Portfolio').cumcount()

# Map the total_monthly_incomes to each row based on the month
income_series = pd.Series(total_monthly_incomes, index=range(month_start_savings, month_retirement_start))
returns['income'] = returns['month'].map(income_series)
# set all nan values in income to 0.0
returns['income'] = returns['income'].fillna(0.0)


def utility_consumption(consumption, household_size, risk_aversion):
    factor_risk = 1 - risk_aversion
    consumption_util = (consumption / math.sqrt(household_size)) ** factor_risk
    adj_consumption_util = consumption_util / factor_risk
    return adj_consumption_util


def utility_inheritance(inher_util, inheritance_amount, inher_luxury, risk_aversion):
    adj_inher_util = inher_util*(12**risk_aversion)
    factor_risk = 1-risk_aversion
    equation = (((inheritance_amount+inher_luxury)**factor_risk) / factor_risk) * adj_inher_util
    return equation


returns['savings'] = 0.0
returns['utility'] = 0.0

final_utility = {}
consumption_dict = {}

for portfolio in returns['Portfolio'].unique():
    # Filter the DataFrame by portfolio
    portfolio_data = returns[returns['Portfolio'] == portfolio]
    
    # Initialize previous savings
    previous_savings = 0.0
    initial_consumption = 0.0
    current_consumption = 0.0
    current_utility = 0.0
    
    
    # Iterate through each row in the portfolio data
    for index, row in portfolio_data.iterrows():
        if row['month'] == month_retirement_start:
            initial_consumption = (previous_savings * consumption_rate)/12
            current_savings = (previous_savings - initial_consumption) * (1 + row['ret'])
            current_utility = utility_consumption(initial_consumption, household_size, risk_aversion)
            returns.at[index, 'savings'] = current_savings
            returns.at[index, 'utility'] = current_utility
            consumption_dict[portfolio] = initial_consumption
        if row['income'] == 0.0 and row['month'] > month_retirement_start and row['month'] < death_month:
            current_consumption = initial_consumption * ((1+inflation_rate)**(row['month']-month_retirement_start))
            if previous_savings <= current_consumption:
                current_consumption = previous_savings
                current_utility = -10000000000000.0
                current_savings = (previous_savings - current_consumption) * (1 + row['ret'])
                returns.at[index, 'utility'] = current_utility
                returns.at[index, 'savings'] = current_savings
            else:
                current_savings = (previous_savings - current_consumption) * (1 + row['ret'])
                current_utility = utility_consumption(current_consumption, household_size, risk_aversion)
                returns.at[index, 'utility'] = current_utility + returns.at[index-1, 'utility']
                returns.at[index, 'savings'] = current_savings
        elif row['month'] == death_month:
            returns.at[index, 'savings'] = previous_savings
            current_consumption = initial_consumption * ((1+inflation_rate)**(row['month']-month_retirement_start))
            current_utility = utility_consumption(current_consumption, household_size, risk_aversion) + utility_inheritance(inher_util, returns.at[index, 'savings'], inher_luxury, risk_aversion)
            returns.at[index, 'utility'] = current_utility + returns.at[index-1, 'utility']
            final_utility[portfolio] = returns.at[index, 'utility']
        elif row['month'] > death_month:
            returns.at[index, 'savings'] = previous_savings
        else:
            current_savings = save_rate * row['income'] + previous_savings * (1 + row['ret'])
            returns.at[index, 'savings'] = current_savings
        # Update previous savings
        previous_savings = current_savings


max_key = max(final_utility, key=final_utility.get)


#############################################
# start: plot
#############################################



returns = returns[(returns['month'] >= month_start_savings) & (returns['month'] <= death_month)]


fig = go.Figure()

for portfolio_name, portfolio_frame in returns.groupby("Portfolio"):
    if portfolio_name == max_key:
        fig.add_trace(go.Scatter(x=portfolio_frame["month"], y=portfolio_frame["savings"], line_shape='spline', name=portfolio_name, line=dict(color='red'), hovertemplate="Month: %{x}<br>Savings: $%{y}"))
        fig.add_annotation(
            x=returns.loc[returns['month'] == month_retirement_start, 'month'].iloc[0],
            y=returns.loc[returns['month'] == month_retirement_start, 'savings'].iloc[0],
            text=f"{portfolio_name} is the optimal portfolio<br>"
             f"Savings at Retirement Start: ${returns.loc[returns['month'] == month_retirement_start, 'savings'].iloc[0]:,.2f}<br>"
             f"Savings at Retirement End (Inheritance): ${portfolio_frame['savings'].iloc[-1]:,.2f}<br>"
             f"Initial Monthly Consumption: ${initial_consumption:,.2f}",
            showarrow=True,
            arrowhead=1,
            ax=0,
            ay=-60,
            font=dict(color="black"),
            align="left",
            bordercolor="black",
            borderwidth=1,
            borderpad=4,
            bgcolor="white"
        )
    else:
        fig.add_trace(go.Scatter(x=portfolio_frame["month"], y=portfolio_frame["savings"], line_shape='spline', name=portfolio_name, line=dict(color='rgba(128, 128, 128, 0.5)'), hovertemplate="Month: %{x}<br>Savings: $%{y}"))

fig.update_layout(
    xaxis_title="Month",
    yaxis_title="Savings",
    width=1000,
    height=600,
    template="plotly_white"
)
fig.update_layout(
    title={
        'text': "Retirement Portfolios over time",
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    }
)

st.plotly_chart(fig, use_container_width=True, theme="streamlit")
