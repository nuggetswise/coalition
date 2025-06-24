import streamlit as st
import json
from utils import (
    generate_remediation, generate_broker_summary,
    generate_underwriting_checklist, generate_broker_questions, generate_risk_mitigation_suggestions
)

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

# --- Underwriting Checklist ---
st.markdown("### ✅ Underwriting Checklist (AI Pre-fill)")
checklist_items = generate_underwriting_checklist(incident)
if 'checklist_state' not in st.session_state or st.session_state.get('last_incident') != incident['id']:
    st.session_state['checklist_state'] = [False] * len(checklist_items)
    st.session_state['last_incident'] = incident['id']
checklist_state = st.session_state['checklist_state']
for i, item in enumerate(checklist_items):
    checklist_state[i] = st.checkbox(item, value=checklist_state[i], key=f"check_{i}")
st.session_state['checklist_state'] = checklist_state

# --- Broker Questions ---
st.markdown("### 🤝 Broker Questions (AI-generated)")
broker_questions = generate_broker_questions(incident)
broker_answers = []
for i, q in enumerate(broker_questions):
    ans = st.text_input(q, key=f"broker_q_{i}")
    broker_answers.append(ans)

# --- Risk Mitigation Suggestions ---
st.markdown("### 🛡️ Risk Mitigation Suggestions")
for s in generate_risk_mitigation_suggestions(incident):
    st.write(f"- {s}")

# --- Remediation & Recommendation ---
if st.button("Generate Remediation & Recommendation") or 'remediation_obj' not in st.session_state:
    remediation_obj = generate_remediation(incident)
    st.session_state['remediation_obj'] = remediation_obj
remediation_obj = st.session_state.get('remediation_obj', {})

st.markdown("### 🛠️ Remediation Steps")
st.success(remediation_obj.get('remediation_steps', ''))

with st.expander("Why was this suggested? (LLM Explainability)"):
    st.write(remediation_obj.get('explanation', ''))

# --- Underwriter Recommendation & Human Override ---
st.markdown("### 📝 Underwriter Recommendation")
rec = remediation_obj.get('recommended_action', '')
conf = remediation_obj.get('confidence_score', 0.0)
st.info(f"**AI Recommendation:** {rec}\n\n**Confidence:** {conf:.2f}")
human_override = st.radio("Human Override (optional)", ["No override", "Accept risk", "Request fix", "Decline policy"], index=0)
final_rec = rec if human_override == "No override" else human_override
st.success(f"**Final Recommendation:** {final_rec}")

# --- Before vs. After: AI vs. Manual Triage ---
st.markdown("### ⏱️ Triage Time Comparison")
st.metric("AI Triage Time", "2 min")
st.metric("Manual Triage Time", "20 min")
st.progress(0.1, text="Manual Triage Quality")
st.progress(0.9, text="AI Triage Quality")

# --- Net Risk After Remediation ---
risk_before = incident.get('risk_contribution_score', 0)
risk_after = 0 if final_rec.lower().startswith('accept') else int(risk_before * (1 - conf))
net_risk = total_risk - (risk_before - risk_after)
st.markdown("### 📉 Net Risk After Remediation")
st.progress(max(1, net_risk) / 100, text=f"Net risk: {net_risk}/100 after remediation")

# --- Broker Summary ---
st.markdown("### 📋 Broker Summary")
broker_summary = generate_broker_summary(remediation_obj.get('remediation_steps', ''), incident)
st.text_area("2-line Broker Note", broker_summary, height=68)

with st.expander("How was this recommendation derived?"):
    st.write(
        """
        The recommendation is based on the incident's risk contribution, remediation cost, and the LLM's confidence in the suggested action. 
        - If the LLM is highly confident and the action is 'Accept risk', risk is considered fully remediated.
        - Otherwise, residual risk is calculated as: risk_after = risk_before × (1 - confidence).
        - The net risk bar shows the updated risk for the underwriter.
        - Human underwriters can override the AI recommendation for full transparency and control.
        """
    )
