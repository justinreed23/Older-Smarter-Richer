import streamlit as st
[theme]
base="light"
primaryColor="#FF4B4B"
backgroundColor="#FFFFFF"
secondaryBackgroundColor="#F0F2F6"
textColor="#262730"
font="sans serif"
sidebar.backgroundColor="#0088FF"

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
# CAPM Portfolio Optimization with Risk Aversion Adjustment: Find Your Optimal Investment Portfolio for Retirement by filling Out Our Survey!
## Project Purpose:
In the modern investing landscape, the traditional approach of using a 60:40 stock-bond approach is prevalent. This strategy involves allocating 60% to stocks and 40% bonds at the beggining of one's life, then typically flips those weights after retirement. This aims to provide a simplified balance between growth potential from stocks and stability from bonds. Our goal was to come up with a more advanced model, which creates a survey for one to clarify their investing and retirement goals to find their optimal investing strategy without having to use unrefined methods or taking the time and effort to work with a professional advisor.  
We hypothesise that different income levels and risk profiles favor different strategies. We use an equation to determine the optimal portfolio selection after the subject has outlined his/her self-described parameters. In addition to finding the optimal investment portfolio, we will also display the cumulative returns over time that one may recieve using our optimized model. The data that we use to optimize a portfolio comes from 10 different ETFs we extracted from Yahoo Finance. We downloaded monthly returns for as long as they date back, then merge them by data into one wide dataset. Lastly, we randomly pulled rows to create a new 600 row dataframe (12 rows x 50 years) and converr that back to a tall dataframe.
This is the equation we use: $$U(C,B) = \displaystyle\sum_{t=\Delta}^{T_{max}} \frac{(C_{t}/\sqrt{H_{t}})^{1-\gamma}}{1-\gamma} + \theta{\frac{(B+k)^{1-\gamma}}{1-\gamma}}$$

$$U(C,B) = \displaystyle\sum_{t=\Delta}^{T_{max}} \frac{(C_{t}/\sqrt{H_{t}})^{1-\gamma}}{1-\gamma} + \theta{\frac{(B+k)^{1-\gamma}}{1-\gamma}}$$

1. We will be using the utility equation from [Anarkulova, Cederburg, O'Doherty](Related_reading/Beyond_Status_Quo.pdf) (2023) to determine optimal portfolio selection
2. Variable Definitions
   1. $C$ is defined as consumption in dollars
   2. $H$ is number of people in household
   3. $t$ is time since started saving (in months)
   4. $\gamma$ is risk aversion
      1. "Normal" is $3.82$
      2. We will adjust this based on respondents self-described risk aversion
   5. $\theta$ is inheritance utility intensity
      1. Normal is $2360 * 12^{\gamma}$
      2. We will adjust this based on respondents self-described inheritance goals
   6. $B$ is inheritance amount
   7. $k$ is the extent to which inheritance is viewed as a luxury good
      1. Normal is $490,000
   8. $\Delta$ is the time between retirement age and savings age in months
   9.  $T^{max}$ is date of death.
9.  Saving assumption is 10% of income if income is $>15000$
10. Ask respondent for expected income growth(?)
## Inspiration: 
## Caveats:
Our models for the ETFs are not particulary robust and can use better refinement for accurate, large scale modeling. We are essentially saying past predictions will provide accurate predictions for future results. Our data consists of monthly returns from these ETFs, which also do not date back past arounf 40 years. Ourmodel does not account for irregularities in the economic landscape.
## About Us:
### Reghan Hesser
title: "Reghan Hesser" # Your name (or website title) here
logo: "/images/headshot.jpg"
- Major: Finance 
- Year of Graduation: 2024
- Interests: Cooking, Skiing, Dancing 
### Justin Reed
### Maria Maragkelli


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



# https://docs.streamlit.io/develop/api-reference/widgets/st.slider
