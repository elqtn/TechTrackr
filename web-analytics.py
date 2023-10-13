import streamlit as st
import pandas as pd
import plotly.express as px
import json

# Load the data from web-analytics.json
with open('web-analytics.json', 'r') as file:
    analytics_data = json.load(file)

# Extract data from the JSON
total_pageviews = analytics_data["total_pageviews"]
total_script_runs = analytics_data["total_script_runs"]
total_time_seconds = analytics_data["total_time_seconds"]

per_day_data = analytics_data["per_day"]
days = per_day_data["days"]
pageviews = per_day_data["pageviews"]
script_runs = per_day_data["script_runs"]

widgets_data = analytics_data["widgets"]

st.set_page_config(layout="wide")

# Title and summary
st.title('Web Analytics Dashboard')

# Create three columns for side-by-side display
col1, col2, col3 = st.columns(3)

# Column 1: Total Pageviews
with col1:
    st.info(f"""
        #### Total Pageviews
        # {total_pageviews}
    """)

# Column 2: Total Script Runs
with col2:
    st.info(f"""
        #### Total Script Runs
        # {total_script_runs}
    """)

# Column 3: Total Time
with col3:
    st.info(f"""
        #### Total Time (in seconds)
        # {total_time_seconds:.2f}
    """)

# Create two columns for side-by-side display
col1, col2 = st.columns(2)

# Column 1: Pageviews and Script Runs per Day
with col1:
    st.subheader('Pageviews and Script Runs per Day')
    
    df_per_day = pd.DataFrame({'Day': days, 'Pageviews': pageviews, 'Script Runs': script_runs})

    fig_per_day = px.area(df_per_day, x='Day', y=['Pageviews', 'Script Runs'], title='Pageviews and Script Runs per Day')
    st.plotly_chart(fig_per_day)

# Column 2: Event Type Analysis
with col2:
    st.subheader('Event Type Analysis')

    widget_data = widgets_data["Select Event Type"]
    event_data = [{'Event Type': event_type, 'Count': count} for event_type, count in widget_data.items() if count > 0]

    df_event = pd.DataFrame(event_data)

    fig_event = px.pie(df_event, values='Count', names='Event Type', title='Event Type Analysis')
    st.plotly_chart(fig_event)

# Widget Analysis
st.subheader('Widget Analysis')

# Handle the space key in "Select Top-Level Category" widget data
widget_data = widgets_data.get("Select Top-Level Category", {})
widget_data.pop(" ", None)  # Remove the key with space

# Filter out categories with zero count
widget_data = {category: count for category, count in widget_data.items() if count > 0}

df_widget = pd.DataFrame({'Category': widget_data.keys(), 'Count': widget_data.values()})

fig_widget = px.bar(df_widget, x='Category', y='Count', title='Top-Level Categories')
st.plotly_chart(fig_widget)

# First Sub-Level Category Analysis
st.subheader('First Sub-Level Category Analysis')

# Handle the space key in "Select First Sub-Level Category" widget data
widget_data = widgets_data.get("Select First Sub-Level Category", {})
widget_data.pop(" ", None)  # Remove the key with space

# Filter out categories with zero count
widget_data = {category: count for category, count in widget_data.items() if count > 0}

df_sub_level = pd.DataFrame({'Sub-Level Category': widget_data.keys(), 'Count': widget_data.values()})

fig_sub_level = px.bar(df_sub_level, x='Count', y='Sub-Level Category', orientation='h', title='First Sub-Level Categories')
st.plotly_chart(fig_sub_level)

# Second Sub-Level Category Analysis
st.subheader('Second Sub-Level Category Analysis')

# Handle the space key in "Select Second Sub-Level Category" widget data
widget_data = widgets_data.get("Select Second Sub-Level Category", {})
widget_data.pop(" ", None)  # Remove the key with space

# Filter out categories with zero count
widget_data = {category: count for category, count in widget_data.items() if count > 0}

df_sub_level2 = pd.DataFrame({'Sub-Level Category': widget_data.keys(), 'Count': widget_data.values()})

fig_sub_level2 = px.bar(df_sub_level2, x='Count', y='Sub-Level Category', orientation='h', title='Second Sub-Level Categories')
st.plotly_chart(fig_sub_level2)

# Start time
start_time = analytics_data["start_time"]
st.subheader('Analytics Start Time')
st.write(start_time)
