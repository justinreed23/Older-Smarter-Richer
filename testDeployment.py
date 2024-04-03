import streamlit as st

st.set_page_config(
    "Portfolio Opt by WSB, Ported to Streamlit by Don Bowen",
    "📊",
    initial_sidebar_state="expanded",
    layout="wide",
)

"""
# CAPM Portfolio Optimization with Risk Aversion Adjustment 

Itsa me, Justin!

"""


#############################################
# start: sidebar
#############################################

with st.sidebar:

    # % chance lose, $ lose, % chance win, $win, CARA formula e, CARA formula V
    qs ={1 :[.50,0,.50,10   ],
         2 :[.50,0,.50,1000 ],
         3 :[.90,0,.10,10   ],
         4 :[.90,0,.10,1000 ],
         5 :[.25,0,.75,100  ],
         6 :[.75,0,.25,100  ]}    

    """
    ## Risk aversion assessment

    ### Part 1: How much would you pay to enter the following lotteries?
    """
    ans = {}
    for i in range(1,len(qs)+1):
        rn = qs[i][0]*qs[i][1] + qs[i][2]*qs[i][3]
        ans[i] = st.slider(f'{int(qs[i][0]*100)}% chance of \${qs[i][1]} and {int(qs[i][2]*100)}% chance of \${qs[i][3]}',
                           0.0,rn,rn,0.1, key=i)
    
    risk_aversion = 0
    for i in range(1,len(qs)+1):
        
        # quadratic util: mu - 0.5 * A * var
        # here, set util = willing to pay, solve for A
        
        exp = qs[i][0]* qs[i][1]          +  qs[i][2]* qs[i][3]
        var = qs[i][0]*(qs[i][1]-exp)**2  +  qs[i][2]*(qs[i][3]-exp)**2
        
        implied_a = 2*(exp-ans[i])/var
           
        risk_aversion += implied_a
  
    if risk_aversion < 0.000001: # avoid the float error when risk_aversion is too small
       risk_aversion = 0.000001    
       
    f'''
    #### Result: Using the survey, your risk aversion parameter is {risk_aversion:.3f}
    ---
    ### If you want, you can override that parameter here:
    
    '''
    
    risk_aversion = st.number_input('Risk aversion parameter',0.000001,float(5),format='%0.2f',value=risk_aversion)