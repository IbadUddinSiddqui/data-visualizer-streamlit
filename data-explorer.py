import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

st.title("Data Explorer & Visualizer")
st.write("Upload your data and explore it better")

with st.sidebar:
    st.header("Upload your file")
    uploaded_file = st.file_uploader("Choose a CSV or Excel file type",type=["csv","xlsx"])
    
    st.header("Settings")
    sample_data = st.checkbox("Load sample data",value=True)
if sample_data:
    df = px.data.iris()
    st.session_state.df = df
    
    st.success("Sample Iris dataset loaded!")
elif uploaded_file:
    
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file,engine="openpyxl")
    st.session_state.df = df
    st.success("File Uploaded successfully!")
else:
    st.warning("Uploaded a file or use sample data.")
    st.stop()   
st.subheader("Your Data")
st.write(st.session_state.df)

st.subheader("Filter Data")
columns = st.session_state.df.columns.tolist()
selected_columns = st.multiselect("Select COlumns to display",columns,default=columns)
filtered_df = st.session_state.df[selected_columns]
st.write(filtered_df)

st.subheader("Visualize Data")

x_axis = st.selectbox("X-axis",columns)
y_axis = st.selectbox("Y-axis",columns)
color_col = st.selectbox("Color by {optional}",[None] + columns)

# Chart type selector
chart_type = st.selectbox("Chart Type", ["Scatter", "Bar", "Line", "Histogram"])
    
# Generate chart
if chart_type == "Scatter":
    fig = px.scatter(filtered_df, x=x_axis, y=y_axis, color=color_col)
elif chart_type == "Bar":
    fig = px.bar(filtered_df, x=x_axis, y=y_axis, color=color_col)
elif chart_type == "Line":
    fig = px.line(filtered_df, x=x_axis, y=y_axis, color=color_col)
elif chart_type == "Histogram":
    fig = px.histogram(filtered_df, x=x_axis, color=color_col)

st.plotly_chart(fig)

# New File Conversion Section
st.markdown("---")  # Add a visual separator
st.header("File Format Converter")
st.write("Convert your files between CSV and Excel formats")

convert_file = st.file_uploader("Upload file to convert", type=["csv", "xlsx"], key="converter")

if convert_file is not None:
    # Determine file type and load accordingly
    if convert_file.name.endswith('.csv'):
        # Converting from CSV to Excel
        df_to_convert = pd.read_csv(convert_file)
        
        # Convert to Excel
        excel_buffer = BytesIO()
        with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
            df_to_convert.to_excel(writer, index=False)
        excel_bytes = excel_buffer.getvalue()
        
        st.download_button(
            label="Download as Excel",
            data=excel_bytes,
            file_name=convert_file.name.replace('.csv', '.xlsx'),
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        st.success("CSV file ready to be downloaded as Excel!")
        
    elif convert_file.name.endswith('.xlsx'):
        # Converting from Excel to CSV
        df_to_convert = pd.read_excel(convert_file, engine="openpyxl")
        
        # Convert to CSV
        csv = df_to_convert.to_csv(index=False).encode()
        
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name=convert_file.name.replace('.xlsx', '.csv'),
            mime="text/csv"
        )
        st.success("Excel file ready to be downloaded as CSV!")

    # Show preview of the data
    st.subheader("File Preview")
    st.write(df_to_convert.head())