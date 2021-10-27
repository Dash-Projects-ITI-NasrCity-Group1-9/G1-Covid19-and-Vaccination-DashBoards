#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import plotly.express as px
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.figure_factory as ff
import base64


# In[2]:


df = pd.read_csv('country_vaccinations.csv')
df['date'] = pd.to_datetime(df['date'])
df['year'] = pd.DatetimeIndex(df['date']).year
df['month'] = pd.DatetimeIndex(df['date']).month
df["people_vaccinated"]= df.groupby("country").total_vaccinations.tail(1)
top_country=df.groupby("country")["people_vaccinated"].mean().sort_values(ascending= False).head(10).reset_index()
ratio=df.groupby('country')['total_vaccinations_per_hundred'].max().sort_values(ascending=False).head(10).reset_index()


# In[3]:


app=dash.Dash()

app.layout=html.Div([
    html.Div([
        html.H1("The Vaccination Against Pandemic",
        style={ 
        'color':'white',
        'vertical-align':'middle',

        'text-align': 'center',
        'vertical-align': 'middle',
        'line-height': '80px',
        'height': 'auto',
        })
    ], style={
        'text-align': 'center',
        'vertical-align': 'top',
        'background-color': "#1c113d", 'height': '90px',}),
    # html.Img(
    #     src=app.get_asset_url("img.jpeg"), style={"float": "left", "height": 90}
    # ),
    html.Div([
        dcc.Graph(id='id1'),
        dcc.Graph(id='id2'),
    ], style={"display": "grid", "grid-template-columns": "50% 50%"}),

    dcc.Slider(
            id = "slider_1",
            updatemode = "drag",
            marks = {i: "{}".format(i) for i in range(1,13)},
            min = 1,
            max = 12,
            step = 1,
            value = 5),

    html.Br(),
    html.Br(),
    html.Div([
        dcc.Dropdown(
        id='dropdown',
         options=[
            {'label': str(c), 'value': str(c)} for c in df['country'].unique()
        ],
        value='China',

    )
    ], style={"width": "30%"},)
    ,
   dcc.Graph(id='line'),
])


# In[4]:


@app.callback(
    Output(component_id='line',component_property='figure'),
    Input(component_id='dropdown',component_property='value'),)
def update_my_graph(dropdownvalue):
    fig=px.line(
        df[df['country']==dropdownvalue], x="date", y="daily_vaccinations", 
        title='Trend in Daily Vaccinations Number')
    fig.update_layout(title=dict(font={'size': 25}, x=0.5, xanchor='center'))
    return fig

@app.callback(
    [
        Output(component_id='id1',component_property='figure'),
        Output(component_id='id2',component_property='figure')
    ],
    Input(component_id='slider_1',component_property='value'),)
def update_my_graph1(month):

    df1 = df[(df.month<=month) | (df.year==2020)]
    top_country=df1.groupby("country")["people_vaccinated"].mean().sort_values(ascending= False).head(10).reset_index()
    ratio=df1.groupby('country')['total_vaccinations_per_hundred'].max().sort_values(ascending=False).head(10).reset_index()

    fig1 = px.bar(
    top_country,
    x='country', y='people_vaccinated', 
    title='Total Vaccination Among Countries',
    color='country',
    )
    fig1.update_layout(
        title=dict(font={'size': 25}, x=0.5, xanchor='center', ),
        )

    fig2 = px.bar(ratio,
        color='country',
        y="country", x="total_vaccinations_per_hundred", 
        orientation="h", hover_name="country",title='Total Vaccinations / Population')
    fig2.update_layout(
        title=dict(font={'size': 25}, 
        x=0.5, xanchor='center',),
        )
    return fig1,fig2
        


# In[ ]:


app.run_server(port='5552')


# In[ ]:




