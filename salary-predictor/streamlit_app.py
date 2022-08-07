import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
from plotly import graph_objs as plx

import numpy as np
from sklearn.linear_model import LinearRegression

data = pd.read_csv("assets//Salary_Data.csv")

x = np.array(data["YearsExperience"]).reshape(-1,1)
y = data["Salary"]

st.title("Salary Predictor App")

nav = st.sidebar.radio("Navigation",["Home","Prediction","Contribute"])

if nav == "Home":
    st.image("assets//salary.png", width=600)

    if st.checkbox("Show Table"):
        st.table(data)

    graph = st.selectbox("What kind of graph?",["Non-interactive","Interactive"])

    val = st.slider("Filter data using years", 0, 20)
    data = data.loc[data["YearsExperience"] >= val]

    if graph == "Non-interactive":
        fig, ax = plt.subplots(figsize = (10,5))
        ax.scatter(data["YearsExperience"], data["Salary"])
        # ax.set_ylim(5,0)
        ax.set_xlabel("Years of Experience")
        ax.set_ylabel("Salary")
        fig.tight_layout()
        st.pyplot(fig)
    elif graph == "Interactive":
        layout = plx.Layout(
            xaxis = dict(range = [0,15]),
            yaxis = dict(range = [0,230000])
        )

        fig = plx.Figure(data = plx.Scatter(x=data["YearsExperience"],y = data["Salary"], mode='markers'), layout=layout)
        st.plotly_chart(fig)

elif nav == "Prediction":
    lr = LinearRegression()
    lr.fit(x,np.array(y))

    st.header("Know your salary")
    val = st.number_input("Enter your experience", 0.00,20.00,step=0.25)
    pred = lr.predict(np.array(val).reshape(1,-1))[0]
    
    if st.button("Predict"):
        st.success(f"Your predicted salary is {round(pred)}")

elif nav == "Contribute":
    st.header("Primary Data Contribution")
    ex = st.number_input("Enter your Experience for work",0.00,20.00)
    sal = st.number_input("Enter your salary for your work",0.00,800000.00, step = 100.00)

    if st.button("Submit"):
        to_add = {"YearsExperience":ex, "Salary":sal}
        to_add = pd.DataFrame(to_add, index=[0])
        to_add.to_csv("assets//Salary_Data.csv", mode='a', header = False, index = False)

        st.success("Data Submitted!")
