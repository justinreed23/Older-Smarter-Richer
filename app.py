import streamlit as st
import numpy as np
import pandas as pd


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

"""
# CAPM Portfolio Optimization with Risk Aversion Adjustment: Find your Optimal Investment Portfolio for Retirement by filling out our Survey
## Project Purpose:
In the modern investing landscape, the traditional approach of using a 60:40 stock-bond approach is prevalent. This strategy involves allocating 60% to stocks and 40% bonds at the beggining of one's life, then typically flips those weights after retirement. This aims to provide a simplified balance between growth potential from stocks and stability from bonds. Our goal was to come up with a more advanced model, which creates a survey for one to clarify their investing and retirement goals to find their optimal investing strategy without having to use unrefined methods or taking the time and effort to work with a professional advisor.  
We hypothesise that different income levels and risk profiles favor different strategies. We use an equation to determine the optimal portfolio selection after the subject has outlined his/her self-described parameters. In addition to findinf the optimal investment portfolio, we will also display the cumulative returns over time that one may recieve using our optimized model. 
##Caveats
##Links to Raw Data
##About Us


"""


#############################################
# start: sidebar
#############################################

with st.sidebar:

    '''
    ## Financial Assessment
    
    ### Please answer the following questions about your financial situation
    '''
    
    submitted_income = st.number_input("What is your annual income?(Max $10mil)", min_value=0, value=10000000)
    income_growth = st.slider("What is your expected annual income growth rate in percentage?", min_value=0.0, max_value=100.0, value=10.0, step=0.1)
    start_savings = st.number_input("At what age did you start saving?", min_value=18, max_value=50)
    retirement_start = st.number_input("At what age will you retire?", min_value=50, max_value=80)
    death_year = st.number_input("At what age do you expect you will pass away?", min_value=50, max_value=105)
    household_size = st.number_input("Number of people in household at time of retirement?", min_value=1, value=10)
    
    inher_util = st.slider("What is your expected annual inheritance utilization?", min_value=0.0, max_value=100000.0, value=2000.0, step=0.1)
    save_rate = st.slider("What percent of your income do you expect to save annually?", min_value=0.0, max_value=100.0, value=5.0, step=0.1)
    consumption_rate= st.slider("What percent of your income do you plan to spend annually?", min_value=0.0, max_value=1.0, value=0.5, step=0.1)
    inflation_rate = st.slider("What is your expected annual income growth rate?", min_value=0.0, max_value=10.0, value=5.0, step=0.1)
   

    risk_aversion_options = ["Low", "Medium", "High"]
    selected_risk_aversion = st.selectbox("Select your risk aversion level:", risk_aversion_options)

# Assigning values based on user selection
    if selected_risk_aversion == "Low":
        risk_aversion = (0.0, 3.0)  # Assign a specific value for low risk aversion
    elif selected_risk_aversion == "Medium":
        risk_aversion = (4.0, 6.0)  # Assign a specific value for medium risk aversion
    else:
        risk_aversion = (7.0, 10.0)  # Assign a specific value for high risk aversion

#############################################
# create returns df, normally this is an import
#############################################

monthly_income = submitted_income/12
monthly_growth = 1+ (income_growth/12)
month_start_savings = start_savings*12
month_retirement_start = retirement_start*12
death_month = death_year*12




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





#############################################
# start: plot
#############################################

