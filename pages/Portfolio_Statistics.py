import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


results = pd.read_csv('inputs/fake_returns.csv')

results = results.drop(columns=['Unnamed: 0'])

