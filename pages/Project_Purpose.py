import streamlit as st

"""
# CAPM Portfolio Optimization with Risk Aversion Adjustment: Find Your Optimal Investment Portfolio for Retirement by filling Out Our Survey!
## Project Purpose:
In the modern investing landscape, the traditional approach of using a 60:40 stock-bond approach is prevalent. This strategy involves allocating 60% to stocks and 40% bonds at the beggining of one's life, then typically flips those weights after retirement. This aims to provide a simplified balance between growth potential from stocks and stability from bonds. Our goal was to come up with a more advanced model, which creates a survey for one to clarify their investing and retirement goals to find their optimal investing strategy without having to use unrefined methods or taking the time and effort to work with a professional advisor.  
We hypothesise that different income levels and risk profiles favor different strategies. We use an equation to determine the optimal portfolio selection after the subject has outlined his/her self-described parameters. In addition to finding the optimal investment portfolio, we will also display the cumulative returns over time that one may recieve using our optimized model. The data that we use to optimize a portfolio comes from 10 different ETFs we extracted from Yahoo Finance. We downloaded monthly returns for as long as they date back, then merge them by data into one wide dataset. Lastly, we randomly pulled rows to create a new 600 row dataframe (12 rows x 50 years) and converr that back to a tall dataframe.
This is the equation we use:
"""

st.latex(r'''
         U(C,B) = \displaystyle\sum_{t=\Delta}^{T_{max}} \frac{(C_{t}/\sqrt{H_{t}})^{1-\gamma}}{1-\gamma} + \theta{\frac{(B+k)^{1-\gamma}}{1-\gamma}}
         ''')


"""
1. We will be using the utility equation from [Anarkulova, Cederburg, O'Doherty](Related_reading/Beyond_Status_Quo.pdf) (2023) to determine optimal portfolio selection
2. Variable Definitions
   1. $C$ is defined as consumption in dollars during retirement
   2. $H$ is number of people in household during retirement
   3. $t$ is time since started saving (in months)
   4. $\gamma$ is risk aversion
      1. The medium value is $3.84$
      2. We will adjust this based on respondents self-described risk aversion
   5. $θ$ is inheritance utility intensity
      1. The medium value is $2360 multiplied by 12^{\gamma}$ to adjust for monthly returns
      2. We will adjust this based on respondents self-described inheritance goals
   6. $B$ is inheritance amount
   7. $k$ is the extent to which inheritance is viewed as a luxury good
      1. Normal is $490,000
   8. $\Delta$ is the time between retirement age and savings age in months
   9.  $T^{max}$ is date of death.
## Inspiration: 
Our work was inspired by "Beyond the Status Quo: A Critical Assessment of Lifecycle Investment Advice." In this paper, the authors discuss the limitations of the traditional 60:40 stock-bond approach and propose a new model that takes into account the individual's risk aversion and inheritance goals. However their study focuses on the average investor using a simulation of many possible American lifestyles. We wanted to take this a step further and create a model that is personalized to the individual investor.
## Caveats:
Our models for the ETFs are not particularly robust and can use better refinement for accurate, large scale modeling. We are essentially saying past predictions will provide accurate predictions for future results. Our data consists of monthly returns from these ETFs, which also do not date back past around 40 years. Our model does not account for irregularities in the economic landscape.
Ideally, our data would be 
"""
