import streamlit as st
import requests

BASE_URL = "https://9ssz6ekjqa.execute-api.ap-south-1.amazonaws.com"

query_params = st.query_params
project_id = query_params.get("projectId", None)

st.title("Infrastructure Request Review")

if project_id:
    st.write(f"Project ID: `{project_id}`")
    st.write("Please choose an action:")

    # Checkbox to verify human
    verified = st.checkbox("✅ I am not a robot")

    if "action_taken" not in st.session_state:
        st.session_state.action_taken = None

    col1, col2 = st.columns(2)

    with col1:
        if st.button("✅ Approve", disabled=not verified):
            st.session_state.action_taken = "approve"

    with col2:
        if st.button("❌ Reject", disabled=not verified):
            st.session_state.action_taken = "reject"

    if st.session_state.action_taken == "approve":
        response = requests.get(f"{BASE_URL}/approve?projectId={project_id}", verify=False)
        if response.ok:
            st.success("Approved successfully!")
        else:
            st.error("Approval failed.")
        st.session_state.action_taken = None  # Reset after action

    elif st.session_state.action_taken == "reject":
        response = requests.get(f"{BASE_URL}/reject?projectId={project_id}", verify=False)
        if response.ok:
            st.success("Rejected successfully!")
        else:
            st.error("Rejection failed.")
        st.session_state.action_taken = None
else:
    st.error("Missing `projectId` in the URL. Please open this app with a valid request ID.")
