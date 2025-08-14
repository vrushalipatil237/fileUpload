import streamlit as st
import pandas as pd
import json
from io import BytesIO

FIELD_MAP = {
    "PAN": ["ITR", "ITR3", "PartA_GEN1", "PersonalInfo", "PAN"],
    "GST Number": ["ITR", "ITR3", "ScheduleGST", "TurnoverGrsRcptForGSTIN", 0, "GSTINNo"],
    # ... rest of your FIELD_MAP ...
}

def get_value(data, path):
    if path == "":
        return ""
    try:
        if isinstance(path, list) and len(path) > 2 and isinstance(path[-2], int):
            container = data
            for p in path[:-2]:
                container = container[p]
            if isinstance(container, list) and len(container) > path[-2]:
                return container[path[-2]].get(path[-1], "")
            return ""
        for p in path:
            data = data[p]
        return data
    except (KeyError, IndexError, TypeError):
        return 0

def run_json_extractor():
    uploaded_json = st.file_uploader("Upload JSON File", type="json")
    if uploaded_json is not None:
        json_data = json.load(uploaded_json)
        output = {field: get_value(json_data, path) for field, path in FIELD_MAP.items()}

        df = pd.DataFrame(output.items(), columns=["Particulars", "Amount"])
        st.dataframe(df, use_container_width=True)

        excel_bytes = BytesIO()
        with pd.ExcelWriter(excel_bytes, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name="Computation")

        st.download_button(
            label="📥 Download Excel File",
            data=excel_bytes.getvalue(),
            file_name="ITR_Computation_Formatted.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
