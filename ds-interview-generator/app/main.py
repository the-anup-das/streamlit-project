"""
Main Program for the streamlit app
"""

from secrets import choice
import streamlit as st
from utils import set_bg, head, body, footer, read_data
import os

path = os.path.dirname(__file__)
icon = path+'/assets/icon.png'

st.set_page_config(page_title='Data Science Interview practice', page_icon=icon)

st.write(path)

# st.set_page_config(page_title='Data Science Interview practice', page_icon='assets/icon.png')

ss = st.session_state
set_bg(path+'/assets/background.png')
head()

if 'prob_click' not in ss:
    ss['prob_click'] = False

if st.button('Bring it on!'):
    ss['prob_click'] = True
    ss['report_click'] = False
    df = read_data(path+'/data/olympiad-problems.csv')
    choice = df.sample(1)
    ss['sample'] = choice
    body(choice)

if ss['prob_click'] and ss['report_click']:
    body(ss['sample'])
    footer(ss['sample'])
elif ss['prob_click']:
    footer(ss['sample'])
    ss['report_click'] = True