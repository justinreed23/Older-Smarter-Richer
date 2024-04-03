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