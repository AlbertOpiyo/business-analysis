import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.subplots as sp
import plotly.graph_objects as go

# call connections\
from postgres_connect import *

#set page
st.set_page_config(page_title="Analytics Dashboard", page_icon="🌎", layout="wide")  
st.subheader("📈 Business Analytics Dashboard ")


# load CSS Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

#get data from mysql
result = view_all_data()
df = pd.DataFrame(result,columns=[	
"EEID","Full Name","JobTitle",
"Department","BusinessUnit","Gender",
"Ethnicity","Age","Hire Date",
"AnnualSalary","Bonus","Country",
"City","id"
])

#switcher
st.sidebar.header("Please filter")
department=st.sidebar.multiselect(
    "Filter Department",
     options=df["Department"].unique(),
     default=df["Department"].unique(),
)
country=st.sidebar.multiselect(
    "Filter Country",
     options=df["Country"].unique(),
     default=df["Country"].unique(),
)
businessunit=st.sidebar.multiselect(
    "Filter Business",
     options=df["BusinessUnit"].unique(),
     default=df["BusinessUnit"].unique(),
)

df_selection=df.query(
    "Department==@department & Country==@country & BusinessUnit ==@businessunit"
)



#top analytics
def metrics():
 from streamlit_extras.metric_cards import style_metric_cards
 col1, col2, col3 = st.columns(3)

 col1.metric(label="Total Customers", value=df_selection.Gender.count(), delta="All customers")

 col2.metric(label="Total Annual Salary", value= f"{df_selection.AnnualSalary.sum():,.0f}",delta=df.AnnualSalary.median())

 col3.metric(label="Annual Salary", value= f"{ df_selection.AnnualSalary.max()-df.AnnualSalary.min():,.0f}",delta="Annual Salary Range")

 style_metric_cards(background_color="#071021",border_left_color="#1f66bd")

# metrics()
#create divs
div1, div2=st.columns(2)

#pie chart
def pie():
 with div1:
  theme_plotly = None # None or streamlit
  fig = px.pie(df_selection, values='AnnualSalary', names='Department', title='Customers by Country')
  fig.update_layout(legend_title="Country", legend_y=0.9)
  fig.update_traces(textinfo='percent+label', textposition='inside')
  st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

# pie()
#bar chart
def barchart():
  theme_plotly = None # None or streamlit
  with div2:
    fig = px.bar(df_selection, y='AnnualSalary', x='Department', text_auto='.2s',title="Controlled text sizes, positions and angles")
    fig.update_traces(textfont_size=18, textangle=0, textposition="outside", cliponaxis=False)
    st.plotly_chart(fig, use_container_width=True, theme="streamlit")
# barchart()

# table
def table():
  with st.expander("Tabular"):
  #st.dataframe(df_selection,use_container_width=True)
   shwdata = st.multiselect('Filter :', df.columns, default=["EEID","Full Name","JobTitle",
                                                             "Department","BusinessUnit","Gender",
                                                             "Ethnicity","Age","Hire Date","AnnualSalary",
                                                             "Bonus","Country","City","id"])
   st.dataframe(df_selection[shwdata],use_container_width=True)

# table()

#option menu
from streamlit_option_menu import option_menu
with st.sidebar:
        selected=option_menu(
        menu_title="Main Menu",
         #menu_title=None,
        options=["Home","Table"],
        icons=["house","book"],
        menu_icon="cast", #option
        default_index=0, #option
        orientation="vertical",
)
 

if selected=="Home":
    
    pie()
    barchart()
    metrics()

if selected=="Table":
   metrics()
   table()
   df_selection.describe().T