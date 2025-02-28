import pandas as pd
import plotly.express as px
import streamlit as st
import io

# Streamlit app title
st.title("Gantt Chart Generator")

# File uploader
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

# Text area for copy-pasting CSV data
csv_text = st.text_area("Or paste CSV data here")

# Function to read CSV data
def load_csv(data):
    return pd.read_csv(io.StringIO(data), skip_blank_lines=True, dtype=str)

# Load data from file or text input
data = None
if uploaded_file:
    data = load_csv(uploaded_file.getvalue().decode("utf-8"))
elif csv_text:
    data = load_csv(csv_text)

# If data is loaded, process and display the Gantt chart
if data is not None:
    try:
        # Ensure proper parsing of date columns
        data["Data estimativa inceput"] = pd.to_datetime(data["Data estimativa inceput"], format='%m/%d/%Y', errors='coerce')
        data["Data estimativa finalizare"] = pd.to_datetime(data["Data estimativa finalizare"], format='%m/%d/%Y', errors='coerce')
        
        # Create the Gantt chart
        fig = px.timeline(
            data,
            x_start="Data estimativa inceput",
            x_end="Data estimativa finalizare",
            y="Activitati",
            title="Gantt Chart - Activități Comunitare",
            labels={"Data estimativa inceput": "Start Date", "Data estimativa finalizare": "End Date", "Activitati": "Task"},
        )

        # Update layout to ensure labels for each month
        fig.update_layout(
            xaxis_title="Timeline",
            yaxis_title="Tasks",
            showlegend=False,
            xaxis=dict(
                tickformat="%b %Y",  # Format to show full month and year
                dtick="M1",  # Ensure monthly ticks
            )
        )

        # Display the chart
        st.plotly_chart(fig)
    except Exception as e:
        st.error(f"Error processing CSV data: {e}")
else:
    st.write("Upload a CSV file or paste data to generate the Gantt chart.")
