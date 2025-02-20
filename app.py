import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO  # Import StringIO specifically

plt.style.use("ggplot")

st.set_page_config(page_title="UR CRISTIANO RONALDO (CR7) - Extensive EDA & Analytics", layout="wide")

st.sidebar.title("📊 UR Cristiano (CR7) Analytics")

st.sidebar.image("cr7.png", use_container_width=True)

sections = {
    "Introduction": "👋 Introduction",
    "Basic Exploration": "🔍 Data Overview",
    "Goals per Competition": "🏆 Competition Analysis",
    "Goals per Season": "📅 Seasonal Performance",
    "Goals per Club": "⚽ Club Career",
    "Goals per Playing Position": "🎯 Position Analysis",
    "Goals per Game Minute": "⏱️ Timing Analysis",
    "Goals per Type": "🎨 Goal Types",
    "Scoreline After Goals": "📊 Impact Analysis",
    "Opponents": "🆚 Opposition Analysis",
    "Favorite Opponents": "🎯 Top Opponents",
    "Assists": "🤝 Assist Analysis",
    "Goals per Venue": "🏟️ Venue Statistics"
}

selections = st.sidebar.radio("Navigate to", list(sections.values()))


def load_data():
    df = pd.read_csv("data.csv")
    return df

df = load_data()

# Match the selection back to the original key
current_section = [k for k, v in sections.items() if v == selections][0]

if current_section == "Introduction":
    st.title("⚽ CR7 - Career Statistics Dashboard")
    st.subheader("Cristiano Ronaldo's Complete Goal Analysis")

    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("""
        **Cristiano Ronaldo dos Santos Aveiro** is widely regarded as one of the greatest footballers of all time.
        This dashboard provides comprehensive analysis of his goal-scoring career across different clubs and competitions.
        
        ### Career Highlights
        - All-time top goalscorer in football history
        - Most international goals in men's football
        - 5 UEFA Champions League titles
        - 5 Ballon d'Or awards
        - Over 800 career goals
        """)
    
    with col2:
        st.write("""
        ### Quick Facts
        - **Current team**: Al-Nassr (#7)
        - **Position**: Forward
        - **Born**: February 5, 1985
        - **Nationality**: Portuguese 🇵🇹
        - **Height**: 1.87 m
        """)

elif current_section == "Basic Exploration":
    st.title("🔍 Data Overview")
    
    tab1, tab2, tab3 = st.tabs(["📊 Data Preview", "📈 Statistics", "🔢 Column Analysis"])
    
    with tab1:
        st.subheader("Raw Data Sample")
        st.dataframe(df.head())
        
    with tab2:
        st.subheader("Dataset Information")
        buffer = StringIO()
        df.info(buf=buffer)
        info_str = buffer.getvalue()
        st.text(info_str)
        
    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Unique Values per Column")
            st.dataframe(pd.DataFrame(df.apply(lambda col:len(col.unique())), 
                        columns=["Unique Values"]).style.background_gradient())
        
        with col2:
            st.subheader("Categorical Statistics")
            st.dataframe(df.describe(include=['object']).T)

elif current_section == "Goals per Competition":
    st.title("🏆 Competition Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig = px.histogram(df, x='Competition', color='Club', 
                          title="Goals Distribution Across Competitions",
                          height=500,
                          hover_name="Club", 
                          hover_data=['Competition', 'Club'])
        fig.update_layout(showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Competition Breakdown")
        comp_stats = df.Competition.value_counts()
        st.dataframe(pd.DataFrame({
            'Competition': comp_stats.index,
            'Goals': comp_stats.values,
            'Percentage': (comp_stats.values / len(df) * 100).round(2)
        }).style.background_gradient())

elif current_section == "Goals per Season":
    st.title("📅 Seasonal Performance")
    fig = px.histogram(df, x='Season', color='Club', title="Goals per Season", 
                      height=500, hover_name="Club", hover_data=['Season', 'Club'])
    st.plotly_chart(fig, use_container_width=True)

elif current_section == "Goals per Club":
    st.title("⚽ Club Career")
    fig1 = px.histogram(df, x = 'Club', color='Season', title = "Goals per Club - Season", 
                 height=500,hover_name = "Season", hover_data=['Competition', 'Season', 'Club'])
    fig2 = px.histogram(df, x = 'Club', color='Competition', title = "Goals per Club - Competition", 
                 height=500,hover_name = "Competition", hover_data=['Competition', 'Season', 'Club'])
    st.plotly_chart(fig1, use_container_width=True)
    st.plotly_chart(fig2, use_container_width=True)

elif current_section == "Goals per Playing Position":
    st.title("🎯 Position Analysis")
    fig = px.histogram(df, x = 'Playing_Position', color='Club', title = "Goals per Playing Position", 
                 height=500,hover_name = "Club", hover_data=['Playing_Position','Competition', 'Season', 'Club'])
    st.plotly_chart(fig, use_container_width=True)

elif current_section == "Goals per Game Minute":
    st.title("⏱️ Timing Analysis")
    df['Minute'] = df['Minute'].str.extract('(\d+)', expand=False).fillna(0).astype(int)
    bins = [0,15,30,45,60,75,90,105,120]
    labels = ['0-15', '15-30', '30-45', '45-60','60-75', '75-90', '90-105','105-120']
    df['Minute_Bin'] = pd.cut(df['Minute'], bins = bins, labels=labels, right=False)
    fig = px.histogram(df, x = 'Minute_Bin', title = "Goals per Game Minute", color = 'Club', height=500)
    st.plotly_chart(fig, use_container_width=True)

elif current_section == "Goals per Type":
    st.title("🎨 Goal Types")
    fig = px.histogram(df, x = 'Type', title = "Goals per Typee", color = 'Club', height=500)
    st.plotly_chart(fig, use_container_width=True)

elif current_section == "Scoreline After Goals":
    st.title("📊 Impact Analysis")
    top_20_scores = df['At_score'].value_counts().nlargest(20).index
    df_top_20 = df[df['At_score'].isin(top_20_scores)]

    fig, ax = plt.subplots(figsize=(15,7))
    sns.countplot(x='At_score', data=df_top_20, order = top_20_scores, ax = ax)
    ax.set_title("Top 20 Scoresheets after Scoring", fontsize = 20)
    st.pyplot(fig)

elif current_section == "Opponents":
    st.title("🆚 Opposition Analysis")
    top_20_opponent = df['Opponent'].value_counts().nlargest(20).index
    df_top_20 = df[df['Opponent'].isin(top_20_opponent)]
    fig, ax = plt.subplots(figsize=(30,10))
    sns.countplot(x='Opponent', data = df_top_20, order = top_20_opponent, ax=ax)
    ax.set_title("Goal per Opponents", fontsize = 20)
    st.pyplot(fig)

elif current_section == "Favorite Opponents":
    st.title("🎯 Top Opponents")
    fig, ax = plt.subplots(figsize=(15,7))
    fav_opponents_df = df['Opponent'].value_counts()[df['Opponent'].value_counts()>15]
    sns.countplot(x='Opponent', data = df[df['Opponent'].isin(fav_opponents_df.index)], order = fav_opponents_df.index, ax=ax)
    ax.set_title("Favorite Opponents", fontsize = 20)
    st.pyplot(fig)

elif current_section == "Assists":
    st.title("🤝 Assist Analysis")

    top_10_assist = df['Goal_assist'].value_counts().nlargest(10).index

    df_top_10 = df[df['Goal_assist'].isin(top_10_assist)]

    fig, ax = plt.subplots(figsize=(15,7))

    sns.countplot(x = 'Goal_assist', data = df_top_10, order = top_10_assist, ax = ax)

    ax.set_title("Top 10 Assists", fontsize = 20)

    st.pyplot(fig)

elif current_section == "Goals per Venue":
    st.title("🏟️ Venue Statistics")
    fig, ax = plt.subplots(figsize = (15,7))
    sns.countplot(x = 'Venue', data = df, order = df['Venue'].value_counts().index, ax = ax)
    ax.set_title("Goal Per Venue", fontsize = 20)
    st.pyplot(fig)