import streamlit as st

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
In the modern investing landscape, the traditional approach of using a 60:40 stock-bond approach is prevalent. This strategy involves allocating 60% to stocks and 40% bonds at the beggining of one's life, then typically flips those weights after retirement. This aims to provide a simplified balance between growth potential from stocks and stability from bonds. 

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



# https://docs.streamlit.io/develop/api-reference/widgets/st.slider
