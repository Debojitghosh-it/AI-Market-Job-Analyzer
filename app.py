import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Job Market Analyzer",
    page_icon="🤖",
    layout="wide"
)

# ---------------- LOAD DATA ----------------
try:
    df = pd.read_csv("cleaned_ai_jobs.csv")
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

# ---------------- HEADER ----------------
st.title("🤖 AI Job Market Analyzer")
st.markdown(
    "Analyze AI job trends, salaries, education requirements, and market insights."
)

st.divider()

# ---------------- SIDEBAR ----------------
st.sidebar.header("🔍 Filters")

if "Job_Title" in df.columns:
    selected_job = st.sidebar.selectbox(
        "Select Job Role",
        ["All"] + sorted(df["Job_Title"].dropna().unique().tolist())
    )

    if selected_job != "All":
        df = df[df["Job_Title"] == selected_job]

# ---------------- KPI SECTION ----------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Records", len(df))

with col2:
    if "Average_Salary" in df.columns:
        st.metric(
            "Average Salary",
            f"${df['Average_Salary'].mean():,.0f}"
        )
    else:
        st.metric("Average Salary", "N/A")

with col3:
    if "Years_Experience" in df.columns:
        st.metric(
            "Avg Experience",
            f"{df['Years_Experience'].mean():.1f} yrs"
        )
    else:
        st.metric("Avg Experience", "N/A")

with col4:
    if "Education_Level" in df.columns:
        st.metric(
            "Top Education",
            df["Education_Level"].mode()[0]
        )
    else:
        st.metric("Top Education", "N/A")

st.divider()

# ---------------- DATA PREVIEW ----------------
st.subheader("📋 Dataset Overview")
st.dataframe(df.head(10), use_container_width=True)

st.divider()

# ---------------- CHARTS ----------------
col1, col2 = st.columns(2)

# Top Job Roles
with col1:
    if "Job_Title" in df.columns:
        st.subheader("💼 Top Job Roles")

        top_jobs = df["Job_Title"].value_counts().head(10)

        fig, ax = plt.subplots(figsize=(8, 4))
        top_jobs.plot(kind="bar", ax=ax)

        ax.set_xlabel("Job Title")
        ax.set_ylabel("Count")
        plt.xticks(rotation=45)
        plt.tight_layout()

        st.pyplot(fig)

# Education Distribution
with col2:
    if "Education_Level" in df.columns:
        st.subheader("🎓 Education Distribution")

        edu = df["Education_Level"].value_counts()

        fig2, ax2 = plt.subplots(figsize=(6, 6))
        ax2.pie(
            edu,
            labels=edu.index,
            autopct="%1.1f%%"
        )

        st.pyplot(fig2)

st.divider()

# ---------------- SALARY ANALYSIS ----------------
if "Average_Salary" in df.columns:
    st.subheader("💰 Salary Distribution")

    fig3, ax3 = plt.subplots(figsize=(10, 4))

    ax3.hist(
        df["Average_Salary"],
        bins=20
    )

    ax3.set_xlabel("Salary")
    ax3.set_ylabel("Frequency")

    st.pyplot(fig3)

st.divider()

# ---------------- INSIGHTS ----------------
st.subheader("📌 Key Insights")

if (
    "Average_Salary" in df.columns
    and "Job_Title" in df.columns
):
    highest_salary = df.loc[df["Average_Salary"].idxmax()]

    st.success(
        f"Highest paying role: "
        f"{highest_salary['Job_Title']} "
        f"(${highest_salary['Average_Salary']:,.0f})"
    )

st.info(
    "Use the filters on the left to explore specific job roles and trends."
)