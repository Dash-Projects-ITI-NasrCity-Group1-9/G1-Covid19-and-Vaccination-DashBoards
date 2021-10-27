#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import plotly.express as px
import dash_bootstrap_components as dbc
import dash
from dash import html, dcc
from dash.dependencies import Input, Output


# In[2]:


df = pd.read_csv('country_wise_latest.csv')


# In[3]:


df.head()


# In[4]:


df['Country/Region'] = df['Country/Region'].replace(['US'],'USA')
df[df['Country/Region']=='USA']


# In[5]:


df.info()


# In[6]:


missing = df.isnull().sum()
missing = missing[missing > 0]
missing.sort_values(inplace = True)
missing


# In[7]:


df_continent = pd.read_csv('worldometer_data.csv')
df_continent


# In[8]:


df[~ df['Country/Region'].isin(df_continent['Country/Region'])]


# In[9]:


set(df_continent['Country/Region']).symmetric_difference(df['Country/Region'])


# In[10]:


df[df['Country/Region']=='Brunei']


# In[11]:


country_dict = {'United Kingdom':'UK','United Arab Emirates':'UAE','Taiwan*':'Taiwan','Saint Vincent and the Grenadines':'St. Vincent Grenadines','Brunei':'Brunei ','South Korea':'S. Korea'}


# In[12]:


df.replace({'Country/Region' : country_dict})


# In[13]:


df_new = pd.merge(df,df_continent[['Country/Region','Continent']],how='inner',on=['Country/Region'])
df_new


# In[14]:


df_new['Deaths'].sum()


# In[15]:


#df_new[['Confirmed','Continent']].groupby('Continent').plot(kind='bar', stacked=True)
df_cases = df_new.groupby(['Continent']).agg({'Confirmed': "sum"}).reset_index()
df_cases


# In[16]:


df_cases.columns


# In[17]:


df_time = pd.read_csv('full_grouped.csv')
df_time.head()


# In[18]:


df_time[df_time['Country/Region']=='Afghanistan']['Confirmed']


# In[19]:


px.line(df_time[df_time['Country/Region'] == 'US'], x = 'Date', y = 'Confirmed',markers = 'True', width = 1000, height = 600, template = 'simple_white', title = "Cases Changes over Time")


# In[20]:


#px.bar(df_cases, x = 'Continent', y = 'Confirmed', width = 1000, height = 600, template = 'simple_white', title = "Total Cases/Continent", hover_name = 'Continent')


# In[21]:


import plotly.graph_objects as go
df_new_cases = df_cases.sort_values(by=['Confirmed'])
fig = go.Figure(go.Bar(
            y = df_new_cases['Continent'],
            x = df_new_cases['Confirmed'],
            orientation='h'),
    layout=go.Layout(
        title=go.layout.Title(text="Total Cases/Continent")
    ))

fig.show()


# In[22]:


import plotly.graph_objects as go
df_recovered = df_new.groupby(['Continent']).agg({'Recovered': "sum",'Deaths': "sum"}).reset_index()
df_recovered


# In[23]:


df_old = pd.read_csv('country_wise_latest.csv')


# In[24]:


import plotly.express as px

map_fig = px.choropleth(df_old,locations='Country/Region',locationmode = 'country names', color='Deaths',
                           color_continuous_scale="Viridis",
                           range_color=(0, df_old['Deaths'].max()),
                           labels={'Deaths':'Deaths'},
                           title='Total Deaths/Country'
                          )
#fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
map_fig.show()


# In[25]:


# Start the app
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server


# In[26]:


# Card components
cards = [
    dbc.Card(
        [
            html.H2("{:,}".format(df_old['Deaths'].sum()), className="card-title"),
            html.P("Total Deaths", className="card-text"),
        ],
        body=True,
        color="dark",
        inverse=True,
    ),
    dbc.Card(
        [
            html.H2("{:,}".format(df_old['Confirmed'].sum()), className="card-title"),
            html.P("Total Cases", className="card-text"),
        ],
        body=True,
        color= "primary",
        inverse=True,
    ),
    dbc.Card(
        [
            html.H2("{:,}".format(df_old['Recovered'].sum()), className="card-title"),
            html.P("Total Recovered", className="card-text"),
        ],
        body=True,
        color="green",
        inverse=True,
    ),
]


# In[27]:


# Graph components
graphs = [
    [
        dcc.Graph(id="graph-map",figure=map_fig),
    ],
    [
        dcc.Graph(id="graph-case",figure=fig),
    ]
]
# Graph components
graphs2 = [
    [
        dcc.Graph(id="graph-time"),
    ],
    [
        dcc.Graph(id="graph-total"),
    ]
]


# In[28]:


def Header(name, app):
    title = html.H1(name, style={"margin-top": 20})
    logo = html.Img(
        src=app.get_asset_url("corona.png"), style={"float": "left", "height": 90}
    )

    return dbc.Row([dbc.Col(logo, md=1), dbc.Col(title, md=10)],style={"background":"#1c113d", "color":'white'})


# In[29]:


app.layout = dbc.Container(
    [
        Header("Coronavirus Tracking", app),
        html.Hr(),
        dbc.Row([dbc.Col(card) for card in cards]),
        html.Br(),
        dbc.Row([dbc.Col(graph) for graph in graphs]),
        html.Br(),
dcc.Dropdown(
    options=[{'label': str(i), 'value': str(i)}for i in df_old['Country/Region']],
    id = 'drop'),
        dbc.Row([dbc.Col(graph) for graph in graphs2]),
    ],
    fluid=False,
    className="p-3 bg-light rounded-3",
)


# In[30]:


dounut_labels = ['Total Deaths','Total Recovered']


# In[31]:


filtered_df = df_new[df_new['Country/Region'] == 'Brazil']
dounut_values = [filtered_df['Deaths'].iloc[0], filtered_df['Recovered'].iloc[0]]
dounut_fig = go.Figure(data=[go.Pie(labels = dounut_labels, values=dounut_values, hole=.7)])


# In[32]:


filtered_df['Deaths'].iloc[0]


# In[33]:


filtered_df = df[df['Country/Region'] == 'Brazil']
dounut_values = [filtered_df['Deaths'].iloc[0], filtered_df['Recovered'].iloc[0]]
dounut_fig = go.Figure(data=[go.Pie(labels = dounut_labels, values=dounut_values, hole=.7)])
dounut_fig.update_traces(marker=dict(colors=['black', 'green']))
dounut_fig.show()


# In[34]:


@app.callback(
                Output(component_id = 'graph-time', component_property = 'figure'),
                Output(component_id = 'graph-total', component_property = 'figure'),
                Input(component_id = 'drop',component_property = 'value')
              )
def update_My_Div(drop):
    if drop == None:
        time_fig = px.line(df_time[df_time['Country/Region'] == 'Brazil'], x = 'Date', y = 'Confirmed',markers = 'True', template = 'simple_white', title = "Confirmed Cases over Time")
        filtered_df = df[df['Country/Region'] == 'Brazil']
        dounut_values = [filtered_df['Deaths'].iloc[0], filtered_df['Recovered'].iloc[0]]
        dounut_fig = go.Figure(data=[go.Pie(labels = dounut_labels, values=dounut_values, hole=.7)])
        dounut_fig = dounut_fig.update_traces(marker=dict(colors=['black', 'green']))
    else:
        time_fig = px.line(df_time[df_time['Country/Region'] == drop], x = 'Date', y = 'Confirmed',markers = 'True',template = 'simple_white', title = "Cases Changes over Time")
        filtered_df = df[df['Country/Region'] == drop]
        dounut_values = [filtered_df['Deaths'].iloc[0], filtered_df['Recovered'].iloc[0]]
        dounut_fig = go.Figure(data=[go.Pie(labels = dounut_labels, values=dounut_values, hole=.7)])
        dounut_fig = dounut_fig.update_traces(marker=dict(colors=['black', 'green']))
        
        
    return time_fig, dounut_fig


# In[ ]:


app.run_server()


# In[ ]:




