import streamlit as st
import requests
import json

BASE_URL = "https://9ssz6ekjqa.execute-api.ap-south-1.amazonaws.com"

query_params = st.query_params
project_id = query_params.get("projectId", None)

st.title("Infrastructure Request Review")

if project_id:
    st.write(f"Project ID: `{project_id}`")
    st.write("Please choose an action:")

    # Checkbox for human verification
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

    if st.session_state.action_taken in ["approve", "reject"]:
        url = f"{BASE_URL}/{st.session_state.action_taken}"
        payload = {"projectId": project_id}
        
        print("URL ",url)
        
        try:
            response = requests.post(url, json=payload, verify=False)
            print("Response", response.text)

            # Map actions to correct past tense
            past_tense = {
                "approve": "Approved",
                "reject": "Rejected"
            }

            if response.ok:
                st.success(f"{past_tense[st.session_state.action_taken]} successfully!")
            else:
                st.error(f"{st.session_state.action_taken} failed.")

        except Exception as e:
            st.error(f"Request error: {e}")

        st.session_state.action_taken = None
else:
    st.error("Missing `projectId` in the URL. Please open this app with a valid request ID.")
