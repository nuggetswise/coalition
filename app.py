import streamlit as st
import json
from utils import generate_remediation, generate_broker_summary

# Load incidents from JSON
def load_incidents(path='data/sample_incidents.json'):
    with open(path, 'r') as f:
        return json.load(f)

st.set_page_config(page_title="Remediation Copilot", layout="wide")
st.title("Remediation Copilot for Coalition Inc.")

# Load incidents
data_path = 'data/sample_incidents.json'
incidents = load_incidents(data_path)
incident_titles = [f"{i['title']} (Risk: {i['risk_level']})" for i in incidents]

# Simulate total risk for demo (sum of all risk_contribution_scores in sample)
total_risk = sum(i.get('risk_contribution_score', 0) for i in incidents if 'risk_contribution_score' in i)

# UI: Dropdown for incident selection
idx = st.selectbox("Select Incident", range(len(incidents)), format_func=lambda i: incident_titles[i])
incident = incidents[idx]

# Card: Incident metadata
st.markdown(f"### 🛡️ Incident Details")
st.info(f"**Description:** {incident['description']}\n\n**Risk Level:** {incident['risk_level']}\n\n**Risk Contribution:** {incident.get('risk_contribution_score', 'N/A')} / 100\n\n**Remediation Cost:** ${incident.get('remediation_cost', 'N/A')}")

# Generate LLM output
if st.button("Generate Remediation & Recommendation") or 'remediation_obj' not in st.session_state:
    remediation_obj = generate_remediation(incident)
    st.session_state['remediation_obj'] = remediation_obj
remediation_obj = st.session_state.get('remediation_obj', {})

# Card: Remediation steps
st.markdown("### 🛠️ Remediation Steps")
st.success(remediation_obj.get('remediation_steps', ''))

# Card: Explanation
with st.expander("Why was this suggested? (LLM Explainability)"):
    st.write(remediation_obj.get('explanation', ''))

# Card: Underwriter Recommendation
st.markdown("### 📝 Underwriter Recommendation")
rec = remediation_obj.get('recommended_action', '')
conf = remediation_obj.get('confidence_score', 0.0)
st.info(f"**Recommendation:** {rec}\n\n**Confidence:** {conf:.2f}")

# Simulate risk reduction
risk_before = incident.get('risk_contribution_score', 0)
risk_after = 0 if rec.lower().startswith('accept') else int(risk_before * (1 - conf))
net_risk = total_risk - (risk_before - risk_after)

st.markdown("### 📉 Net Risk After Remediation")
st.progress(max(1, net_risk) / 100, text=f"Net risk: {net_risk}/100 after remediation")

# Card: Broker summary
st.markdown("### 📋 Broker Summary")
broker_summary = generate_broker_summary(remediation_obj.get('remediation_steps', ''), incident)
st.text_area("2-line Broker Note", broker_summary, height=60)

# Explain recommendation logic
with st.expander("How was this recommendation derived?"):
    st.write(
        """
        The recommendation is based on the incident's risk contribution, remediation cost, and the LLM's confidence in the suggested action. 
        - If the LLM is highly confident and the action is 'Accept risk', risk is considered fully remediated.
        - Otherwise, residual risk is calculated as: risk_after = risk_before × (1 - confidence).
        - The net risk bar shows the updated risk for the underwriter.
        """
    )
