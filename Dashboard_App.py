# Libraries
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import base64

##________________Page configuration------------------
st.set_page_config(page_title='Agriculture in Bhutan',
                   page_icon=":bar_chart:",
                   layout='wide')

#.........HIDE STREAMLIT STYLE......#
hide_st_style = """
                <style>
                #MainMenu {visibility:hidden;}
                footer {visibility:hidden;}
                header {visibility:hidden;}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)

##....... LOAD DATA ........##
st.cache(persist=True)
def load_data():
    df = pd.read_csv('data.csv')
    df['Yield'] = (df['Production']*1000)/df['Area']
    assert isinstance(df, object)
    return df


df = load_data()

##-------------------SIDEBARS-----------------------##
st.sidebar.subheader("Filter dashboards here")
dashboards = st.sidebar.radio('Select a dashboard',
    options=['Crop Production Analysis', 'Export and Import Analysis', 'Self Sufficiency Analysis']
)
st.sidebar.markdown("---")

# Share the data
coded_data = base64.b64encode(df.to_csv(index=False).encode()).decode()
st.sidebar.subheader("Want to download the data?")
st.sidebar.markdown(
    f'<a href ="data:file/csv;base64, {coded_data}" download = "df.csv">Click to download</a>',
    unsafe_allow_html=True
)
st.sidebar.markdown("---")

##################### This is the end for the day***************

##---------------Crop Production Analysis---------------------------------##
if dashboards == 'Crop Production Analysis':
    st.markdown("<h3 style='text-align: center; color: Black;'>Production and area trends analysis</h3>", unsafe_allow_html=True)
    top_padding = 1
    bottom_padding = 1
    right_padding = 2
    left_padding = 2
    st.markdown(f""" <style>
        .reportview-container .main .block-container{{
            padding-top: {top_padding}rem;
            padding-right: {right_padding}rem;
            padding-left: {left_padding}rem;
            padding-bottom: {bottom_padding}rem;
        }} </style> """, unsafe_allow_html=True)
    st.markdown('---')
    df['Year'] = df['Year']
    crops = st.selectbox(
        label="Select a crop",
        options=df['Crop'].unique())

    ##---------SLECTION DATAFRAME-------------------##
    df_selection = df.query(
        "Crop == @crops")

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Bar(x=df_selection['Year'], y=df_selection['Production'], name='Production (MT)'),
        secondary_y=False,
    )

    fig.add_trace(
        go.Bar(name='Area (Acre)', x=df_selection['Year'], y=df_selection['Area']),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(name='Yield (kg/acre)',
                   x=df_selection['Year'],
                   y=df_selection['Yield'],
                   line = dict(shape = 'spline')),
        secondary_y=True
    )
        # go.Scatter(name='Area Trend', x=df_selection['Year'], y=df_selection['Area'])

    fig.update_layout(
        paper_bgcolor='#F0FFF0',
        plot_bgcolor='#F0FFF0',
        xaxis_title="Year",
        legend_title="<b>Legend<b>",
        hovermode="x", bargap=0.1
    )
    # Set y-axes titles
    fig.update_yaxes(title_text="<b>Production (MT) & Area (Acre)</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>Yield (Kg/Acre)</b>", secondary_y=True)
    st.plotly_chart(fig, use_container_width=True)

    #Expander for optional sections
    options = st.expander("Expand to see more", False)
    options.markdown("<b>Check the checkbox to see the data</b>", unsafe_allow_html=True)
    if options.checkbox('Show dataframe'):
        data = df_selection[['Year', 'Production', 'Area', 'Yield']]
        options.table(data.style.highlight_max(axis=0))

    # Share the code (Inside expander section)
    mycode = """
    # Initialize the figure with subplot display capability
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Bar(x=df_selection['Year'], y=df_selection['Production'], name='Production (MT)'),
        secondary_y=False,
    )

    fig.add_trace(
        go.Bar(name='Area (Acre)', x=df_selection['Year'], y=df_selection['Area']),
        secondary_y=False,
    )
    
    fig.add_trace(
        go.Scatter(name='Yield (kg/acre)', x=df_selection['Year'], y=df_selection['Yield']),
        secondary_y=True
    )
    
    # Update figure layout    
    fig.update_layout(
        width=1200,
        height=600,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Year",
        legend_title="<b>Legend<b>",
        hovermode="x", bargap=0.1
    )
    
    # Set y-axes titles
    fig.update_yaxes(title_text="<b>Production (MT) & Area (Acre)</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>Yield (Kg/Acre)</b>", secondary_y=True)
    st.plotly_chart(fig)
    """
    if options.checkbox('Show code'):
        options.code(mycode, language='python')

##--------------Export and Import Analysis---------------------------------##
if dashboards == 'Export and Import Analysis':
    st.markdown("<h3 style='text-align: center; color: Black;'>Export and import nalysis</h3>", unsafe_allow_html=True)
    top_padding = 1
    bottom_padding = 1
    right_padding = 2
    left_padding = 2
    st.markdown(f""" <style>
            .reportview-container .main .block-container{{
                padding-top: {top_padding}rem;
                padding-right: {right_padding}rem;
                padding-left: {left_padding}rem;
                padding-bottom: {bottom_padding}rem;
            }} </style> """, unsafe_allow_html=True)
    st.markdown("---")
    df['Year'] = df['Year']
    crops = st.selectbox(
        label="Select a crop",
        options=df['Crop'].unique())

    ##---------SLECTION DATAFRAME-------------------##
    df_selection = df.query(
        "Crop == @crops")

    # Create figure with secondary y-axis
    fig = go.Figure()

    # Add traces
    fig.add_trace(
        go.Bar(x=df_selection['Year'],
               y=df_selection['Export'],
               name='Export (MT)')
    )

    fig.add_trace(
        go.Bar(name='Import (MT)',
               x=df_selection['Year'],
               y=df_selection['Import'])
    )

    fig.update_layout(
        barmode = 'group',
        paper_bgcolor='#F5F5DC',
        plot_bgcolor='#F5F5DC',
        xaxis_title="Year",
        legend_title="<b>Legend<b>",
        hovermode="x", bargap=0.1
    )
    # Set y-axes titles
    fig.update_yaxes(title_text="<b>Export and Import (MT)</b>")
    st.plotly_chart(fig, use_container_width=True)

    #Expander for optional sections
    options = st.expander("Expand to see more", False)
    options.markdown("<b>Check the checkbox to see the data</b>", unsafe_allow_html=True)
    if options.checkbox('Show dataframe'):
        data = df_selection[['Year', 'Production', 'Area', 'Yield']]
        options.table(data.style.highlight_max(axis=0))

        # Share the code (Inside expander section)
    mycode2 = """
        # Initialize the figure with subplot display capability
        fig = go.Figure()

        # Add traces
        fig.add_trace(
            go.Bar(x=df_selection['Year'], 
            y=df_selection['Export'], 
            name='Export (MT)'),
        )

        fig.add_trace(
            go.Bar(name='Import (MT)', 
            x=df_selection['Year'], 
            y=df_selection['Import']),
        )

        fig.update_layout(
            barmode = 'group',
            width=1200,
            height=600,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Year",
            legend_title="<b>Legend<b>",
            hovermode="x", bargap=0.1
        )
        # Set y-axes titles
        fig.update_yaxes(title_text="<b>Export and Import (MT)</b>")
        st.plotly_chart(fig)
        """
    if options.checkbox('Show code'):
        options.code(mycode2, language='python')

##------------------Self fufficiency rate and IDR---------------------------------##
if dashboards == 'Self Sufficiency Analysis':
    st.markdown("<h3 style='text-align: center; color: Black;'>Self Sufficiency Analysis</h3>", unsafe_allow_html=True)
    top_padding = 1
    bottom_padding = 1
    right_padding = 2
    left_padding = 2
    st.markdown(f""" <style>
            .reportview-container .main .block-container{{
                padding-top: {top_padding}rem;
                padding-right: {right_padding}rem;
                padding-left: {left_padding}rem;
                padding-bottom: {bottom_padding}rem;
            }} </style> """, unsafe_allow_html=True)
    st.markdown("---")
    df['Year'] = df['Year']
    crops = st.selectbox(
        label="Select a crop",
        options=df['Crop'].unique())

    ##---------SLECTION DATAFRAME-------------------##
    df_selection = df.query(
        "Crop == @crops")

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Scatter(name='Sufficiency rate (%)',
                   x=df_selection['Year'],
                   y=df_selection['SSR'],
                   line=dict(shape='spline'))
    )

    fig.add_trace(
        go.Scatter(name = 'DES (Per Capita)',
                   x=df_selection['Year'],
                   y = df_selection['DES'],
                   line=dict(shape='spline')))

    fig.add_trace(
        go.Scatter(name='IDR (%)',
                   x=df_selection['Year'],
                   y=df_selection['IDR'],
                   line=dict(shape='spline')),
        secondary_y = True
    )

    fig.update_layout(
        paper_bgcolor='#FFF0F5',
        plot_bgcolor='#FFF0F5',
        xaxis_title="<b>Year<b>",
        yaxis_title="<b>SSR & IDR (%)<b>",
        legend_title="<b>Legend<b>",
        hovermode="x"
    )
    # Set y-axes titles
    fig.update_yaxes(title_text="<b>SSR (%) and DES (kcal/day)</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>IDR (%)</b>", secondary_y=True)
    st.plotly_chart(fig, use_container_width=True)

    #Expander for optional sections
    options = st.expander("Expand to see more", False)
    options.markdown("<b>Check the checkbox to see the data</b>", unsafe_allow_html=True)
    if options.checkbox('Show dataframe'):
        data = df_selection[['Year', 'Production', 'Area', 'Yield', 'Export', 'Import', 'SSR']]
        options.table(data.style.highlight_max(axis=0))

    # Share the code (Inside expander section)
    mycode3 = """
        # Initialize the figure with subplot display capability
        # Create figure with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Add traces
        fig.add_trace(
            go.Scatter(name='Sufficiency rate (%)',
                x=df_selection['Year'],
                y=df_selection['SSR'],
                line=dict(shape='spline'))
            )

        fig.add_trace(
            go.Scatter(name='IDR (%)',
                x=df_selection['Year'],
                y=df_selection['IDR'],
                line=dict(shape='spline')),
            secondary_y = True
            )

        fig.update_layout(
            width=1200,
            height=600,
            paper_bgcolor='#FFF0F5',
            plot_bgcolor='#FFF0F5',
            xaxis_title="Year",
            yaxis_title="SSR & IDR (%)",
            legend_title="<b>Legend<b>",
            hovermode="x"
        )
        # Set y-axes titles
        fig.update_yaxes(title_text="<b>SSR (%)</b>", secondary_y=False)
        fig.update_yaxes(title_text="<b>IDR (%)</b>", secondary_y=True)
        st.plotly_chart(fig)
    """
    if options.checkbox('Show code') and dashboards == 'Self Sufficiency Analysis':
        options.code(mycode3, language='python')
