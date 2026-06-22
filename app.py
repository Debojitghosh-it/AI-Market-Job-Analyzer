import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("AI Job Market Analyzer")

df = pd.read_csv("AI_Impact_on_Jobs_2030.csv")

st.subheader("Dataset Overview")
st.write(df.head())

# Top job roles
st.subheader("Top Job Roles")

top_jobs = df["Job_Title"].value_counts().head(10)

fig, ax = plt.subplots(figsize=(10, 5))
top_jobs.plot(kind="bar", ax=ax)

plt.xticks(rotation=45)

st.pyplot(fig)
