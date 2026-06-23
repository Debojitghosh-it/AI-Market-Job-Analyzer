import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Job Market Analyzer",
    page_icon="🤖",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
}

h1, h2, h3 {
    color: #60a5fa;
}

[data-testid="metric-container"] {
    background-color: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    padding: 15px;
    border-radius: 12px;
}

[data-testid="stSidebar"] {
    background-color: #111827;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
try:
    df = pd.read_csv("backend/AI_Impact_on_Jobs_2030.csv")
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

filtered_df = df.copy()

if "Job_Title" in df.columns:
    job_options = ["All"] + sorted(df["Job_Title"].dropna().unique().tolist())

    selected_job = st.sidebar.selectbox(
        "Select Job Role",
        job_options
    )

    if selected_job != "All":
        filtered_df = filtered_df[
            filtered_df["Job_Title"] == selected_job
        ]

# ---------------- KPI SECTION ----------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Records", len(filtered_df))

with col2:
    if "Average_Salary" in filtered_df.columns:
        st.metric(
            "Average Salary",
            f"${filtered_df['Average_Salary'].mean():,.0f}"
        )
    else:
        st.metric("Average Salary", "N/A")

with col3:
    if "Years_Experience" in filtered_df.columns:
        st.metric(
            "Avg Experience",
            f"{filtered_df['Years_Experience'].mean():.1f} yrs"
        )
    else:
        st.metric("Avg Experience", "N/A")

with col4:
    if (
        "Education_Level" in filtered_df.columns
        and not filtered_df["Education_Level"].dropna().empty
    ):
        st.metric(
            "Top Education",
            filtered_df["Education_Level"].mode()[0]
        )
    else:
        st.metric("Top Education", "N/A")

st.divider()

# ---------------- DATA PREVIEW ----------------
st.subheader("📋 Dataset Overview")
st.dataframe(
    filtered_df.head(10),
    use_container_width=True
)

st.divider()

# ---------------- CHARTS ----------------
col1, col2 = st.columns(2)

# Top Job Roles
with col1:
    if "Job_Title" in filtered_df.columns:

        st.subheader("💼 Top Job Roles")

        top_jobs = (
            filtered_df["Job_Title"]
            .value_counts()
            .head(10)
        )

        fig, ax = plt.subplots(figsize=(8, 4))

        ax.bar(
            top_jobs.index,
            top_jobs.values
        )

        ax.set_xlabel("Job Title")
        ax.set_ylabel("Count")
        ax.set_title("Top Job Roles")

        plt.xticks(rotation=45)
        plt.tight_layout()

        st.pyplot(fig)

# Education Distribution
with col2:
    if (
        "Education_Level" in filtered_df.columns
        and not filtered_df["Education_Level"].dropna().empty
    ):

        st.subheader("🎓 Education Distribution")

        edu = filtered_df["Education_Level"].value_counts()

        fig2, ax2 = plt.subplots(figsize=(6, 6))

        ax2.pie(
            edu.values,
            labels=edu.index,
            autopct="%1.1f%%"
        )

        ax2.set_title("Education Levels")

        st.pyplot(fig2)

st.divider()

# ---------------- SALARY ANALYSIS ----------------
if (
    "Average_Salary" in filtered_df.columns
    and not filtered_df["Average_Salary"].dropna().empty
):

    st.subheader("💰 Salary Distribution")

    fig3, ax3 = plt.subplots(figsize=(10, 4))

    ax3.hist(
        filtered_df["Average_Salary"],
        bins=20
    )

    ax3.set_xlabel("Salary")
    ax3.set_ylabel("Frequency")
    ax3.set_title("Salary Distribution")

    st.pyplot(fig3)

st.divider()

# ---------------- INSIGHTS ----------------
st.subheader("📌 Key Insights")

if (
    "Average_Salary" in filtered_df.columns
    and "Job_Title" in filtered_df.columns
    and not filtered_df.empty
):

    highest_salary = filtered_df.loc[
        filtered_df["Average_Salary"].idxmax()
    ]

    st.success(
        f"Highest paying role: "
        f"{highest_salary['Job_Title']} "
        f"(${highest_salary['Average_Salary']:,.0f})"
    )

st.info(
    "Use the filters in the sidebar to explore specific job roles and trends."
)
