import streamlit as st
# from deta import Deta

import utils

st.set_page_config(layout="wide", page_title='Oscars Predictions')

#Connect Deta Database Connection
# deta = Deta(st.secrets["project_key"])
# db = deta.Base("oscar_bets_test")

cols = ['name','email','password','city','best_movie','best_director','best_actor','best_actress']

safeCols = cols.copy()
safeCols.remove('email')
safeCols.remove('password')

nominees = utils.grab_nominees() 
# df = utils.grab_predictions()
# emails = df['email'].to_list()

best_movies = nominees[nominees['Category']=='Best Picture']['Nominee'].drop_duplicates().sort_values()

# selectPage = st.sidebar.selectbox("Select Page", ("Oscar 2022 Nominees", "Oscar 2022 Predictions","Past Oscar Winners", "Emoji Quiz"))

utils.emoji_quiz(best_movies)