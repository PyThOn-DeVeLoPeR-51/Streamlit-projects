import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px


st.set_page_config(page_title="Dashboard", page_icon=":chart_with_upwards_trend:", layout="wide")
st.markdown("<style>div.block-container{padding-top:1rem;}</style>", unsafe_allow_html=True)
html_title = """
    <style>
        .title-test {
        font-weight:bold;
        padding:5px;
        border-radius:6px}
    </style>
    <center><h1 class='title-test'>ANALYTICS BY ATTEND OF STUDENTS</h1></center>    
        """
st.markdown(html_title, unsafe_allow_html=True)

df = pd.read_csv('Analytic_by_students.csv')
df_attend = pd.read_csv("attend_students.csv")
df_no_attend = pd.read_csv("no_attend_students.csv")

# st.sidebar.image("data/logo1.png", caption="Online Analytics")
st.sidebar.header("Please filter")

weekday = st.sidebar.multiselect("Select weekday", options=df['weekday'].unique(), default=df['weekday'].unique())
month = st.sidebar.multiselect("Select month", options=df['month'].unique(), default=df['month'].unique())



df_selection = df.query("weekday == @weekday & month == @month")


def home():
    with st.expander("Tabular"):
        showData = st.multiselect("Filter: ", df_selection.columns)
        st.write(df_selection[showData])

    total_students = df_selection['customer_id'].count()
    total_attends = df_selection[df_selection['is_attend']=='attend']['is_attend'].count()
    total_no_attends = df_selection[df_selection['is_attend']=='no_attend']['is_attend'].count()
    total_groups = len(df_selection['group_ids'].unique())
    total_subjects = len(df_selection['event_id'].unique())

    total1, total2, total3, total4, total5 = st.columns(5, gap='large')
    with total1:
        st.info("Total students", icon="🤵🏻")
        st.metric(label="Students", value=f"{total_students:,.0f}")

    with total2:
        st.info("Attended", icon="🤵🏻")
        st.metric(label="Attended", value=f"{total_attends:,.0f}")

    with total3:
        st.info("No attended", icon="🤵🏻")
        st.metric(label="No attended", value=f"{total_no_attends:,.0f}")

    with total4:
        st.info("Total groups", icon="👧")
        st.metric(label="Type of groups", value=f"{total_groups:,}")

    with total5:
        st.info("Total subjects", icon="📚")
        st.metric(label="Type of subjects", value=f"{total_subjects:,}")

    st.divider()
home()

def graph():
    # attend_students = df_attend.groupby(by=['customer_id'])['weekday'].count()
    fig_bar_month = px.bar(
        df_selection,
        x="customer_id",
        y="month",
        orientation="h",
        title="<b>Attended of students by month</b>",
        color_discrete_sequence=["#0083b8"]*len(df_selection),
        template="gridon")

    # attend_students = df_attend.groupby(by=['weekday']).count()[['customer_id']].sort_values(by="customer_id")
    fig_bar_week = px.bar(
        df_selection,
        x='customer_id',
        y='weekday',
        orientation="h",
        title="<b>Attended of students by weekday</b>",
        color_discrete_sequence=["#0083b8"]*len(df_selection),
        template="gridon")

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_bar_month, use_container_width=True)

    with col2:
        st.plotly_chart(fig_bar_week, use_container_width=True)

    st.divider()

    attend_students=df_selection.groupby(by=['weekday']).count()[['is_attend']]
    fig_line_week = px.line(
        attend_students,
        x=attend_students.index,
        y='is_attend',
        orientation="v",
        title="<b>Attended of students by weekday</b>",
        color_discrete_sequence=["#0083b8"]*len(attend_students),
        template="plotly_white")
    fig_line_week.update_layout(xaxis=dict(tickmode="linear"))

    attend_students_by_month=df_selection.groupby(by=['event_date']).count()[['is_attend']]
    fig_line_month = px.line(
        attend_students_by_month,
        x=attend_students_by_month.index,
        y='is_attend',
        orientation="v",
        title="<b>Attended of students by month</b>",
        color_discrete_sequence=["#0083b8"]*len(attend_students_by_month),
        template="plotly_white")
    fig_line_month.update_layout(xaxis=dict(tickmode="linear"))

    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(fig_line_week, use_container_width=True)
    with col4:
        st.plotly_chart(fig_line_month, use_container_width=True)

    st.divider()


    df_pie1 = df_selection.groupby(by=['month'])['customer_id'].value_counts().reset_index()
    pie_chart1 = px.pie(df_pie1, values="customer_id", names='month', hole=0.5, title='Attended of students by month')
    pie_chart1.update_traces(text=df_pie1['month'], textposition="outside")

    df_pie2 = df_selection.groupby(by=['weekday'])['customer_id'].value_counts().reset_index()
    pie_chart2 = px.pie(df_pie2, values="customer_id", names='weekday', hole=0.5, title='Attended of students by weekday')
    pie_chart2.update_traces(text=df_pie2['weekday'], textposition="outside")


    pie1, pie2 = st.columns((2))
    with pie1:
        st.plotly_chart(pie_chart1, use_container_width=True)
    with pie2:
        st.plotly_chart(pie_chart2, use_container_width=True)

    st.divider()

    st.subheader("Amount attend of students IDs")
    treemap = df_selection[['month', 'customer_id', 'weekday', 'is_attend']].groupby(by=['month', 'weekday', 'is_attend'])['customer_id'].count().reset_index()
    fig_tree = px.treemap(treemap, path=['month', 'weekday', 'is_attend'], values='customer_id', height=700, width=600, color="is_attend")

    fig_tree.update_traces(textinfo="label+value")
    st.plotly_chart(fig_tree, use_container_width=True)

graph()