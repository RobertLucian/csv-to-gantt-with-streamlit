import pandas as pd
import plotly.express as px
import streamlit as st
import io

# Streamlit app title
st.title("Ruxi's Personal Gantt Chart Generator")

st.markdown("""
When you realize what technology can actually do for you...
""")

# Display meme image
st.image("artifacts/funny_cat.jpg", width=250)

# Display input restrictions
st.markdown("""
#### CSV Input Requirements
- The CSV must contain the following columns:
  - **Activitati** (Task Name)
  - **Data estimativa inceput** (Start Date) in **MM/DD/YYYY** format
  - **Data estimativa finalizare** (End Date) in **MM/DD/YYYY** format
- Dates must be valid and the start date must not be after the end date.
- Extra columns will be ignored automatically.
            
#### Gantt Chart Generation
""")

# File uploader for multiple CSV files
uploaded_files = st.file_uploader("Upload one or more CSV files", type=["csv"], accept_multiple_files=True)

# Text area for copy-pasting CSV data
csv_text = st.text_area("Or paste CSV data here")

# Function to read CSV data
def load_csv(data):
    df = pd.read_csv(io.StringIO(data), skip_blank_lines=True, dtype=str)
    
    # Validate required columns
    required_columns = {"Activitati", "Data estimativa inceput", "Data estimativa finalizare"}
    if not required_columns.issubset(df.columns):
        missing_columns = required_columns - set(df.columns)
        st.error(f"Missing required columns: {', '.join(missing_columns)}")
        return None
    
    # Drop any additional columns not required
    df = df[list(required_columns)]
    
    return df

# Load data from files or text input
data_frames = []
if uploaded_files:
    for uploaded_file in uploaded_files:
        df = load_csv(uploaded_file.getvalue().decode("utf-8"))
        if df is not None:
            data_frames.append((uploaded_file.name, df))
elif csv_text:
    df = load_csv(csv_text)
    if df is not None:
        data_frames.append(("Pasted Data", df))

# If data is loaded, process and display multiple Gantt charts
if data_frames:
    try:
        for file_name, data in data_frames:
            # Ensure proper parsing of date columns
            data["Data estimativa inceput"] = pd.to_datetime(data["Data estimativa inceput"], format='%m/%d/%Y', errors='coerce')
            data["Data estimativa finalizare"] = pd.to_datetime(data["Data estimativa finalizare"], format='%m/%d/%Y', errors='coerce')
            
            # Check for invalid dates
            if data["Data estimativa inceput"].isna().any() or data["Data estimativa finalizare"].isna().any():
                st.error(f"Invalid date format detected in {file_name}. Ensure dates are in MM/DD/YYYY format.")
                continue
            
            # Check for logical inconsistencies
            if (data["Data estimativa inceput"] > data["Data estimativa finalizare"]).any():
                st.error(f"Some tasks in {file_name} have start dates after end dates. Please correct them.")
                continue
            
            # Create the Gantt chart
            fig = px.timeline(
                data,
                x_start="Data estimativa inceput",
                x_end="Data estimativa finalizare",
                y="Activitati",
                title=f"Gantt Chart - {file_name}",
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
            st.subheader(f"Gantt Chart for {file_name}")
            st.plotly_chart(fig)
    except Exception as e:
        st.error(f"Error processing CSV data: {e}")
else:
    st.write("Upload one or more CSV files or paste data to generate Gantt charts.")