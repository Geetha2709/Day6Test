import streamlit as st
import requests
import datetime
import os

st.set_page_config(page_title="Approval Request Portal", layout="centered")

st.title("🚦 Approval Request Portal")

with st.form("approval_form"):
    name = st.text_input("Your Name")
    email = st.text_input("Your Email")
    department = st.selectbox("Department", ["HR", "Engineering", "Finance", "Marketing"])
    request_type = st.selectbox("Request Type", ["Leave", "Resource Access", "Expense Approval", "Task Switch"])
    description = st.text_area("Describe your request")
    urgency = st.select_slider("Urgency", ["Low", "Medium", "High"])
    submitted = st.form_submit_button("Submit Request")

    if submitted:
        data = {
            "name": name,
            "email": email,
            "department": department,
            "request_type": request_type,
            "description": description,
            "urgency": urgency,
            "timestamp": datetime.datetime.now().isoformat()
        }

        n8n_webhook_url = 'https://geetha2709.app.n8n.cloud/webhook-test/e7d01226-e845-433f-a54b-7f9208508262'

        try:
            response = requests.post(n8n_webhook_url, json=data)
            if response.status_code == 200:
                st.success("✅ Request submitted successfully!")
            else:
                st.error("❌ Failed to submit request. Please try again.")
        except Exception as e:
            st.error(f"🚨 Error contacting n8n webhook: {str(e)}")

# Display recent updates from n8n webhook (optional)
st.markdown("### 🗂️ Recent Approvals")
if st.button("🔄 Refresh Updates"):
    updates_url = os.getenv("N8N_UPDATES_URL", "https://YOUR-N8N-INSTANCE/webhook/approval-updates")
    try:
        res = requests.get(updates_url)
        if res.status_code == 200:
            updates = res.json()
            for u in updates:
                st.info(f"📌 {u['timestamp']} - {u['name']} ({u['request_type']}) - **{u['status']}**")
        else:
            st.warning("Couldn't fetch updates.")
    except Exception as e:
        st.error(f"Error fetching updates: {e}")
