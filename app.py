import streamlit as st
import json
from utils import (
    llm_parse_incident_and_generate_all
)

st.set_page_config(page_title="Remediation Copilot", layout="wide")
st.title("Remediation Copilot for Coalition Inc.")

# --- Incident Free-Text Input ---
st.markdown("#### Enter a cybersecurity incident description:")
example_prompts = [
    "A public S3 bucket with sensitive configs was found by our cloud scanner on June 10, 2025.",
    "Multiple admin accounts were found using weak passwords and no MFA on June 12, 2025.",
    "An unpatched Apache server (2.4.29) with critical CVEs was detected by a vulnerability scan.",
    "A phishing email impersonating IT support was reported by several users last week."
]
st.markdown(
    "<span style='color:gray'>e.g. " + "<br>e.g. ".join(example_prompts) + "</span>",
    unsafe_allow_html=True
)
user_incident = st.text_area("Incident Description", height=100)

if st.button("Analyze Incident with AI") and user_incident.strip():
    with st.spinner("AI is analyzing the incident and generating all outputs..."):
        result = llm_parse_incident_and_generate_all(user_incident)
        st.session_state['llm_result'] = result

llm_result = st.session_state.get('llm_result', None)
if llm_result:
    st.markdown("### ✅ Underwriting Checklist (AI-generated)")
    for item in llm_result.get('checklist', []):
        st.checkbox(item, value=False, disabled=True)

    st.markdown("### 🤝 Broker Questions (AI-generated)")
    for q in llm_result.get('broker_questions', []):
        st.radio(q, ['Yes', 'No'], index=0, disabled=True)

    st.markdown("### 🛡️ Risk Mitigation Suggestions (AI-generated)")
    for s in llm_result.get('risk_mitigation', []):
        st.write(f"- {s}")

    st.markdown("### 🛠️ Remediation Steps (AI-generated)")
    st.success(llm_result.get('remediation', ''))

    st.markdown("### 📝 Underwriter Recommendation (AI-generated)")
    st.info(f"**Recommendation:** {llm_result.get('recommendation', '')}\n\n**Confidence:** {llm_result.get('confidence', 'N/A')}")

    st.markdown("### 📋 Broker Summary (AI-generated)")
    st.text_area("2-line Broker Note", llm_result.get('broker_summary', ''), height=68, disabled=True)

    with st.expander("How was this recommendation derived?"):
        st.write(llm_result.get('explanation', ''))

st.markdown('<hr style="margin-top:2em;">', unsafe_allow_html=True)
st.caption("This app is for the application of Senior Product Manager, Underwriting AI at Coalition Inc. Only for demo/job application use.")
