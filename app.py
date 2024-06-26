import streamlit as st
import numpy as np
import pandas as pd
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
# import custom sampling to allow users to resample
#############################################
ready_sample = pd.read_csv('inputs/ready_to_sample.csv')

@st.cache_data
def process_data(ready_to_sample):
    """
    Process the given dataframe to generate final_data.

    Parameters:
    ready_to_sample (pandas.DataFrame): The dataframe to be processed.

    Returns:
    pandas.DataFrame: The processed dataframe containing final_data.
    """
    wide_sim_life = ready_to_sample.sample(n=12*80, replace=True, ignore_index=True).reset_index()
    etfs_full_tall = wide_sim_life.melt(id_vars='index', var_name='ETF', value_name='ret')
    etfs_full_tall = etfs_full_tall[etfs_full_tall['ETF'] != 'Date']
    etfs_full_tall = wide_sim_life.melt(id_vars='index', var_name='ETF', value_name='ret')
    etfs_full_tall = etfs_full_tall[etfs_full_tall['ETF'] != 'Date']
    etfs_full_tall.rename(columns={'index': 'month'}, inplace=True)
    rets_wide = etfs_full_tall.pivot(index='month', columns='ETF', values='ret')
    rets_wide['SPY_VFWAX'] = 0.5*rets_wide['SPY'] + 0.5 * rets_wide['VFWAX'] #domestic/international stock split
    rets_wide['SPY_BND'] = 0.5*rets_wide['SPY'] + 0.5 * rets_wide['BND'] #stock/bond split
    rets_wide['SPY_VNQ_BND'] = 0.5*rets_wide['SPY'] + 0.5 * rets_wide['VNQ'] #stock/bond/real estate split
    rets_wide['SPY_VFWAX_BND'] = 0.4*rets_wide['SPY'] + 0.4 * rets_wide['VFWAX'] + 0.2 * rets_wide['BND'] #domestic/ international stock/bond split
    final_data = rets_wide.reset_index().melt(id_vars='month', var_name='ETF', value_name='ret')
    
    return final_data



returns = process_data(ready_sample)

#############################################
# start: sidebar
#############################################

with st.sidebar:
    if st.button("Resample data"):
        st.cache_data.clear()
        
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
# edit some parameters to make them work nicely
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
month_retirement_start = month_retirement_start - month_start_savings
death_month = death_month - month_start_savings
month_start_savings = 0



#############################################
# portfolio df creation
#############################################


# rename the 'ETF' column to 'Portfolio'
returns = returns.rename(columns={'ETF': 'Portfolio'})

# initialize income column
returns['income'] = 0.0


# create a list of total monthly incomes
total_monthly_incomes = []

for t in returns.index[month_start_savings:month_retirement_start]:
    current_month = t-month_start_savings
    income_for_month = monthly_income*(monthly_growth**current_month)
    total_monthly_incomes.append(income_for_month)
    


# Map the total_monthly_incomes to each row based on the month
income_series = pd.Series(total_monthly_incomes, index=range(month_start_savings, month_retirement_start))
returns['income'] = returns['month'].map(income_series)
# set all nan values in income to 0.0
returns['income'] = returns['income'].fillna(0.0)


# define utility functions, look into caching?
####################################################
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

# initialize savings and utility columns
returns['savings'] = 0.0
returns['utility'] = 0.0

# create dictionaries to store consumption and utility values at t=death
final_utility = {}
consumption_dict = {}


# this is where the magic happens
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
        # this is the if scenario for when user first retires
        if row['month'] == month_retirement_start:
            # stores initial consumption value
            initial_consumption = (previous_savings * consumption_rate)/12
            # find savings at t=month
            current_savings = (previous_savings - initial_consumption) * (1 + row['ret'])
            # find utility at t=month
            current_utility = utility_consumption(initial_consumption, household_size, risk_aversion)
            # set the savings and utility values in the DataFrame
            returns.at[index, 'savings'] = current_savings
            returns.at[index, 'utility'] = current_utility
            # find add initial consumption to our consumption dict
            consumption_dict[portfolio] = initial_consumption
            
        # this is the if scenario for when user is retired
        if row['income'] == 0.0 and row['month'] > month_retirement_start and row['month'] < death_month:
            current_consumption = initial_consumption * ((1+inflation_rate)**(row['month']-month_retirement_start))
            # check if retiree runs out of money
            # sets their utility to -10000000000000.0
            # above could use changing, want to punish for running out of money but not too much
            # like punishment should be different for running out of money in month 1 vs month 100
            if previous_savings <= current_consumption:
                current_consumption = previous_savings
                current_utility = -10000000000000.0
                current_savings = (previous_savings - current_consumption) * (1 + row['ret'])
                returns.at[index, 'utility'] = current_utility
                returns.at[index, 'savings'] = current_savings
            # this scenario is if retiree has money left over
            else:
                current_savings = (previous_savings - current_consumption) * (1 + row['ret'])
                current_utility = utility_consumption(current_consumption, household_size, risk_aversion)
                returns.at[index, 'utility'] = current_utility + returns.at[index-1, 'utility']
                returns.at[index, 'savings'] = current_savings
        # records a bunch of useful info at death month and calculates inheritance utility
        elif row['month'] == death_month:
            returns.at[index, 'savings'] = previous_savings
            current_consumption = initial_consumption * ((1+inflation_rate)**(row['month']-month_retirement_start))
            current_utility = utility_consumption(current_consumption, household_size, risk_aversion) + utility_inheritance(inher_util, returns.at[index, 'savings'], inher_luxury, risk_aversion)
            returns.at[index, 'utility'] = current_utility + returns.at[index-1, 'utility']
            final_utility[portfolio] = returns.at[index, 'utility']
        # this is where the user is dead
        elif row['month'] > death_month:
            returns.at[index, 'savings'] = previous_savings
        # this is where user is working, not spending money from retirement account
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

tabs = ['Overview'] + list(returns['Portfolio'].unique())

tabOverview, tab0, tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs(tabs)

with tabOverview:
    fig = go.Figure()

    for portfolio_name, portfolio_frame in returns.groupby("Portfolio"):
        if portfolio_name == max_key:
            fig.add_trace(go.Scatter(x=portfolio_frame["month"], y=portfolio_frame["savings"], line_shape='spline', name=portfolio_name, line=dict(color='red'), hovertemplate="Month: %{x}<br>Savings: $%{y}"))
            fig.add_annotation(
                x=portfolio_frame.loc[portfolio_frame['month'] == month_retirement_start, 'month'].iloc[0],
                y=portfolio_frame.loc[portfolio_frame['month'] == month_retirement_start, 'savings'].iloc[0],
                text=f"{portfolio_name} is the optimal portfolio<br>"
                f"Savings at Retirement Start: ${portfolio_frame.loc[portfolio_frame['month'] == month_retirement_start, 'savings'].iloc[0]:,.2f}<br>"
                f"Savings at Retirement End (Inheritance): ${portfolio_frame['savings'].iloc[-1]:,.2f}<br>"
                f"Initial Annual Consumption: ${initial_consumption*12:,.2f}",
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

with tab0:
    fig = go.Figure()
    current_portfolio = list(returns['Portfolio'].unique())[0]
    spec_portfolio = returns.groupby('Portfolio').get_group(current_portfolio)
    fig.add_trace(go.Scatter(x=spec_portfolio['month'], y=spec_portfolio['savings'], line_shape='spline', name=current_portfolio, line=dict(color='blue'), hovertemplate="Month: %{x}<br>Savings: $%{y}"))
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Savings",
        width=1000,
        height=600,
        template="plotly_white"
    )
    fig.update_layout(
        title={
            'text': f"{current_portfolio} as chosen Portfolio over time<br>",
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        }
    )
    fig.add_annotation(
        x=0,
        y=spec_portfolio.loc[spec_portfolio['month'] == month_retirement_start, 'savings'].iloc[0],
        text="Hello!",
        showarrow=False,
        font=dict(color="black"),
        align="left",
        bordercolor="black",
        borderwidth=1,
        borderpad=4,
        bgcolor="white"
    )
    st.plotly_chart(fig, use_container_width=True, theme="streamlit")
    
with tab1:
    fig = go.Figure()
    current_portfolio = list(returns['Portfolio'].unique())[1]
    spec_portfolio = returns.groupby('Portfolio').get_group(current_portfolio)
    fig.add_trace(go.Scatter(x=spec_portfolio['month'], y=spec_portfolio['savings'], line_shape='spline', name=current_portfolio, line=dict(color='blue'), hovertemplate="Month: %{x}<br>Savings: $%{y}"))
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Savings",
        width=1000,
        height=600,
        template="plotly_white"
    )
    fig.update_layout(
        title={
            'text': f"{current_portfolio} as chosen Portfolio over time",
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        }
    )
    st.plotly_chart(fig, use_container_width=True, theme="streamlit")
with tab2:
    fig = go.Figure()
    current_portfolio = list(returns['Portfolio'].unique())[2]
    spec_portfolio = returns.groupby('Portfolio').get_group(current_portfolio)
    fig.add_trace(go.Scatter(x=spec_portfolio['month'], y=spec_portfolio['savings'], line_shape='spline', name=current_portfolio, line=dict(color='blue'), hovertemplate="Month: %{x}<br>Savings: $%{y}"))
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Savings",
        width=1000,
        height=600,
        template="plotly_white"
    )
    fig.update_layout(
        title={
            'text': f"{current_portfolio} as chosen Portfolio over time",
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        }
    )
    st.plotly_chart(fig, use_container_width=True, theme="streamlit")
with tab3:
    fig = go.Figure()
    current_portfolio = list(returns['Portfolio'].unique())[3]
    spec_portfolio = returns.groupby('Portfolio').get_group(current_portfolio)
    fig.add_trace(go.Scatter(x=spec_portfolio['month'], y=spec_portfolio['savings'], line_shape='spline', name=current_portfolio, line=dict(color='blue'), hovertemplate="Month: %{x}<br>Savings: $%{y}"))
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Savings",
        width=1000,
        height=600,
        template="plotly_white"
    )
    fig.update_layout(
        title={
            'text': f"{current_portfolio} as chosen Portfolio over time",
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        }
    )
    st.plotly_chart(fig, use_container_width=True, theme="streamlit")
with tab4:
    fig = go.Figure()
    current_portfolio = list(returns['Portfolio'].unique())[4]
    spec_portfolio = returns.groupby('Portfolio').get_group(current_portfolio)
    fig.add_trace(go.Scatter(x=spec_portfolio['month'], y=spec_portfolio['savings'], line_shape='spline', name=current_portfolio, line=dict(color='blue'), hovertemplate="Month: %{x}<br>Savings: $%{y}"))
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Savings",
        width=1000,
        height=600,
        template="plotly_white"
    )
    fig.update_layout(
        title={
            'text': f"{current_portfolio} as chosen Portfolio over time",
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        }
    )
    st.plotly_chart(fig, use_container_width=True, theme="streamlit")