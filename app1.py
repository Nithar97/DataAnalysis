import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
from streamlit.components.v1 import html
import base64
import tempfile

# Function to set a background image and change text color
def set_bg_and_text_style():
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://wowslider.com/sliders/demo-31/data1/images/bench560435.jpg");
            background-size: cover;
        }
        /* Add CSS styling to change text color to pink */
        h1, h2, h3, h4, h5, h6, p, .stMarkdown {
            color: #FF10B4;  /* This is a pink color */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Set the background image and text color at the start of your app
set_bg_and_text_style()

# Function to load data
def load_data(uploaded_file):
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)
    else:
        st.error("Unsupported file format: use CSV or Excel.")
        return None
    return df

# Web app title
st.title("Data Analysis Web App with YData Profiling")

# Upload CSV or Excel data
st.header('Upload your data')
uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None:
    data = load_data(uploaded_file)
    if data is not None:
        st.write("Data Overview:")
        st.write(data.head())

        # Generate YData Profiling Report
        st.header('YData Profiling Report')
        profile = ProfileReport(data, title="Report", explorative=True)

        # Convert the report to HTML and display in an iframe
        report_html = profile.to_html()

        # Display the HTML report
        html(report_html, width=1500, height=2800, scrolling=True)

        # Create a temporary file to save the report
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmpfile:
            tmpfile.write(report_html.encode("utf-8"))

        # Download button for the report
        st.download_button(label="Download Profile Report",
                           data=tmpfile.name,
                           file_name="profile_report.html",
                           mime="text/html")
