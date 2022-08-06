import pandas as pd

penguins = pd.read_csv('penguins_cleaned.csv')

df = penguins.copy()
target = 'species'
encode = ['sex','island']

for col in encode:
    dummy = pd.get_dummies(df[col])