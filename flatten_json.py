import streamlit as st
import pandas as pd
import json
from io import BytesIO

# Function to flatten a JSON object
def flatten_json(nested_json, delimiter):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + delimiter)
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + delimiter)
                i += 1
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

# Button to process the file
if st.button("Convert to Excel"):
    if uploaded_file is not None:
        # Load the JSON file
        data = json.load(uploaded_file)

        # Flatten the JSON object
        flat = flatten_json(data, delimiter)

        # Convert the flattened JSON object into a DataFrame
        df = pd.DataFrame(list(flat.items()), columns=['Key', 'Value'])

        # Convert DataFrame to Excel
        output = BytesIO()
        df.to_excel(output, index=False)
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
