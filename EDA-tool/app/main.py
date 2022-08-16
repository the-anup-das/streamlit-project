from tkinter.ttk import Style
import streamlit as st
import pandas as pd
import plotly.express as px
import os

from utils import space, sidebar_space, df_info,df_isnull
from utils import sidebar_multiselect_container, number_of_outliers

#optional needed to do this as running multiple streamlit apps from same respositary
path = os.path.dirname(__file__)
icon = path+'/assets/icon.png'

st.set_page_config(layout="wide", page_icon=icon, page_title="EDA Tool for Data Scinece Enthusiast")

st.header("🎨Exploratory Data Analysis Tool for Data Science Projects")

st.write('<p style="font-size:160%">You will be able to✅:</p>', unsafe_allow_html=True)


st.write('<p style="font-size:100%">&nbsp 1. See the whole dataset</p>', unsafe_allow_html=True)
st.write('<p style="font-size:100%">&nbsp 2. Get column names, data types info</p>', unsafe_allow_html=True)
st.write('<p style="font-size:100%">&nbsp 3. Get the count and percentage of NA values</p>', unsafe_allow_html=True)
st.write('<p style="font-size:100%">&nbsp 4. Get descriptive analysis</p>', unsafe_allow_html=True)
st.write('<p style="font-size:100%">&nbsp 5. Check inbalance or distribution of target variable</p>', unsafe_allow_html=True)
st.write('<p style="font-size:100%">&nbsp 6. See distribution of numerical columns</p>', unsafe_allow_html=True)
st.write('<p style="font-size:100%">&nbsp 7. See count plot of categorical columns</p>', unsafe_allow_html=True)
st.write('<p style="font-size:100%">&nbsp 8. Get outlier analysis with box plots</p>', unsafe_allow_html=True)
st.write('<p style="font-size:100%">&nbsp 9. Obtain info of target value variance with categorical columns</p>', unsafe_allow_html=True)

space()

st.write('<p style="font-size:100%">Import Dataset</p>', unsafe_allow_html=True)

file_format = st.radio('Select file format:',('csv','excel'), key='file_format')
dataset = st.file_uploader(label = '')

load_sample = st.checkbox('Use example Dataset')
if load_sample:
    dataset = path+'/data/CarPrice.csv'

st.sidebar.header('Import Dataset to Use Available Features: 👉')

if dataset:
    if file_format == 'csv' or load_sample:
        df = pd.read_csv(dataset)
    else:
        df = pd.read_excel(dataset)
    
    st.subheader('Datafram:')
    n, m = df.shape
    st.write(f'<p style="font-size:130%">Dataset contains {n} rows and {m} columns.</p>', unsafe_allow_html=True)   
    st.dataframe(df)

    all_visuals = ['Info','NA Info', 'Descriptive Analysis', 'Target Analysis',
    'Distribution of Numerical Columns','Count plots of Categorical Columns', 'Box Plots',
    'Outlier Analysis','Variance of Target with Categorical Columns']

    sidebar_space(3)
    visuals = st.sidebar.multiselect("Choose which visualizations you want to see 👇",all_visuals)

    if 'Info' in visuals:
        st.subheader('Info:')
        c1, c2, c3 = st.columns([1, 2, 1])
        c2.dataframe(df_info(df))

    if 'NA Info' in visuals:
        st.subheader('NA Value Information:')
        if df.isnull().sum().sum() == 0:
            st.write('There is not any NA value in your dataset')
        else:
            c1, c2, c3 = st.columns([0.5, 2, 0.5])
            c2.dataframe(df_isnull(df), width=1500)
            space(2)

    if 'Descriptive Analysis' in visuals:
        st.subheader('Descriptive Analysis:')
        st.dataframe(df.describe())

    if 'Target Analysis' in visuals:
        st.subheader("Select target column:")
        target_column = st.selectbox("", df.columns, index = len(df.columns) - 1)

        st.subheader("Histogram of target column")
        fig = px.histogram(df, x = target_column)
        c1, c2, c3 = st.columns([0.5, 2, 0.5])
        c2.plotly_chart(fig)

    num_columns = df.select_dtypes(exclude = 'object').columns
    cat_columns = df.select_dtypes(include = 'object').columns

    if 'Distribution of Numerical Columns' in visuals:
        if len(num_columns) == 0:
            st.write('There is no numerical columns in the data.')
        else:
            selected_num_cols = sidebar_multiselect_container('Choose columns for Count plots:', cat_columns, 'Count')
            st.subheader('Count plots of categorical columns')
            i = 0
            while (i < len( selected_num_cols)):
                c1, c2 = st.columns(2)
                for j in [c1, c2]:
                    if (i >= len(selected_num_cols)):
                        break

                    fig = px.histogram(df, x = selected_num_cols[i])
                    j.plotly_chart(fig, use_container_width = True)
                    i += 1

    if 'Count Plots of Categorical Columns' in visuals:
        if len(cat_columns) == 0:
            st.write('There is no categorical columns in the data.')
        else:
            selected_cat_cols = sidebar_multiselect_container('Choose columns for Count plots:', cat_columns, 'Count')
            st.subheader('Count plots of categorical columns')
            i = 0
            while (i < len(selected_cat_cols)):
                c1, c2 = st.columns(2)
                for j in [c1, c2]:
                    if (i >= len(selected_cat_cols)):
                        break

                    fig = px.histogram(df, x = selected_cat_cols[i], color_discrete_sequence=['indianred'])
                    j.plotly_chart(fig)
                    i += 1

    if 'Box Plots' in visuals:
        if len(num_columns) == 0:
            st.write('There is no numerical columns in the data.')
        else:
            selected_num_cols =  sidebar_multiselect_container('Choose columns for Box plots:', num_columns, 'Box')
            st.subheader('Box plots')
            i = 0
            while (i < len(selected_num_cols)):
                c1, c2 = st.columns(2)
                for j in [c1, c2]:
                    if (i >= len(selected_num_cols)):
                        break
                    fig = px.box(df, y = selected_num_cols[i])
                    j.plotly_chart(fig, use_container_width = True)
                    i += 1

    if 'Outlier Analysis' in visuals:
        st.subheader('Outlier Analysis')
        c1, c2, c3 = st.columns([1,2,1])
        c2.dataframe(number_of_outliers(df))

    if 'Variance of Target with Categorical Columns' in visuals:
            
            
            df_1 = df.dropna()
            
            high_cardi_columns = []
            normal_cardi_columns = []

            for i in cat_columns:
                if (df[i].nunique() > df.shape[0] / 10):
                    high_cardi_columns.append(i)
                else:
                    normal_cardi_columns.append(i)


            if len(normal_cardi_columns) == 0:
                st.write('There is no categorical columns with normal cardinality in the data.')
            else:
            
                st.subheader('Variance of target variable with categorical columns')
                model_type = st.radio('Select Problem Type:', ('Regression', 'Classification'), key = 'model_type')
                selected_cat_cols = sidebar_multiselect_container('Choose columns for Category Colored plots:', normal_cardi_columns, 'Category')
                
                if 'Target Analysis' not in visuals:   
                        target_column = st.selectbox("Select target column:", df.columns, index = len(df.columns) - 1)
                            
                i = 0
                while (i < len(selected_cat_cols)):                                
                                
                            
                                if model_type == 'Regression':
                                    fig = px.box(df_1, y = target_column, color = selected_cat_cols[i])
                                else:
                                    fig = px.histogram(df_1, color = selected_cat_cols[i], x = target_column)

                                st.plotly_chart(fig, use_container_width = True)
                                i += 1

                if high_cardi_columns:
                                if len(high_cardi_columns) == 1:
                                    st.subheader('The following column has high cardinality, that is why its boxplot was not plotted:')
                                else:
                                    st.subheader('The following columns have high cardinality, that is why its boxplot was not plotted:')
                                for i in high_cardi_columns:
                                    st.write(i)
                                
                                st.write('<p style="font-size:140%">Do you want to plot anyway?</p>', unsafe_allow_html=True)    
                                answer = st.selectbox("", ('No', 'Yes'))

                                if answer == 'Yes':
                                    for i in high_cardi_columns:
                                        fig = px.box(df_1, y = target_column, color = i)
                                        st.plotly_chart(fig, use_container_width = True)