import streamlit as st
import pandas as pd
import json
from io import BytesIO

# Display the contents of the README.md file
def display_readme():
    try:
        with open("README.md", "r") as f:
            readme_content = f.read()
        st.markdown(readme_content)
    except FileNotFoundError:
        st.error("README.md file not found.")

display_readme()

# Function to preprocess JSON keys
def preprocess_keys(obj, delimiter, replacement):
    if isinstance(obj, dict):
        new_obj = {}
        for k, v in obj.items():
            new_key = k.replace(delimiter, replacement)
            new_obj[new_key] = preprocess_keys(v, delimiter, replacement)
        return new_obj
    elif isinstance(obj, list):
        return [preprocess_keys(item, delimiter, replacement) for item in obj]
    else:
        return obj

# Function to flatten a JSON object
def flatten_json(nested_json, delimiter):
    out = {}

    def flatten(x, name=''):
        if isinstance(x, dict):
            for a in x:
                flatten(x[a], f"{name}{a}{delimiter}")
        elif isinstance(x, list):
            for i, a in enumerate(x):
                flatten(a, f"{name}{i}{delimiter}")
        else:
            out[name[:-len(delimiter)]] = x

    flatten(nested_json)
    return out

# Streamlit app
st.title("JSON to Excel Converter")

# File uploader for JSON input
uploaded_file = st.file_uploader("Choose a JSON file", type="json")

# Input for delimiter
delimiter = st.text_input("Enter delimiter", value="_")

# Input for replacement character
replacement = st.text_input("Enter replacement character for delimiter conflicts", value="-")

# Button to process the file
if st.button("Convert to Excel"):
    if uploaded_file is not None:
        # Load the JSON file
        data = json.load(uploaded_file)

        # Preprocess the JSON object to replace instances of the delimiter
        preprocessed_data = preprocess_keys(data, delimiter, replacement)

        # Flatten the JSON object
        flat = flatten_json(preprocessed_data, delimiter)

        # Convert the flattened JSON object into a DataFrame
        df = pd.DataFrame(list(flat.items()), columns=['Key', 'Value'])

        # Add a new column with the last segment of the key
        df['Last Segment'] = df['Key'].apply(lambda x: x.split(delimiter)[-1])

        # Convert DataFrame to Excel
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
        output.seek(0)

        # Provide download link for the Excel file
        st.download_button(
            label="Download Excel file",
            data=output,
            file_name="output.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.error("Please upload a JSON file.")
