import streamlit as st
import requests

BASE_URL= "https://9ssz6ekjqa.execute-api.ap-south-1.amazonaws.com"

# Use the updated query param method
query_params = st.query_params
project_id = query_params.get("projectId", None)

st.title("Infrastructure Request Review")

if project_id:
    st.write(f"Project ID: `{project_id}`")
    st.write("Please choose an action:")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("✅ Approve"):
            print(f"{BASE_URL}/approve?projectId={project_id}")
            response = requests.get(f"{BASE_URL}/approve?projectId={project_id}",verify=False)
            print("Approval Response",response.text)
            if response.ok:
                st.success("Approved successfully!")
            else:
                st.error("Approval failed.")

    with col2:
        if st.button("❌ Reject"):
            response = requests.get(f"{BASE_URL}/reject?projectId={project_id}",verify=False)
            if response.ok:
                st.success("Rejected successfully!")
            else:
                st.error("Rejection failed.")
else:
    st.error("Missing `id` in the URL. Please open this app with a valid request ID.")
