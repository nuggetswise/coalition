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

if st.button("Analyze with AI") and user_incident.strip():
    with st.spinner("AI is analyzing the incident and generating all outputs..."):
        result = llm_parse_incident_and_generate_all(user_incident)
        st.session_state['llm_result'] = result

# --- Underwriting Checklist (AI-generated) ---
if 'llm_result' not in st.session_state or st.session_state.get('last_incident_text') != user_incident:
    st.session_state['llm_result'] = llm_parse_incident_and_generate_all(user_incident) if user_incident.strip() else None
    st.session_state['last_incident_text'] = user_incident
llm_result = st.session_state.get('llm_result', None)

selected_checklist = []
if llm_result:
    st.markdown("### ✅ Underwriting Checklist (AI-generated)")
    checklist_items = llm_result.get('checklist', [])
    for i, item in enumerate(checklist_items):
        if st.checkbox(item, key=f'checklist_{i}'):
            selected_checklist.append(item)

# --- Broker Questions (dynamic based on checklist) ---
broker_questions = []
broker_answers = []
if selected_checklist:
    # Use LLM to generate broker questions based on selected checklist
    with st.spinner("AI is generating broker questions based on your checklist selections..."):
        from utils import llm_generate_broker_questions_from_checklist
        broker_questions = llm_generate_broker_questions_from_checklist(user_incident, selected_checklist)
    st.markdown("### 🤝 Broker Questions (AI-generated)")
    for i, q in enumerate(broker_questions):
        ans = st.radio(str(q), ['Yes', 'No'], index=0, key=f'broker_q_{i}')
        broker_answers.append(ans)

# --- Risk Mitigation Suggestions & Remediation Steps (dynamic based on broker answers) ---
suggestions = []
remediation = ''
recommendation = ''
confidence = ''
broker_summary = ''
explanation = ''

# Always show results immediately after button click, using latest values
if broker_questions and broker_answers:
    if st.button("Generate Remediation & Recommendation"):
        with st.spinner("AI is generating risk mitigation, remediation, and recommendations based on your answers..."):
            from utils import llm_generate_suggestions_and_remediation
            result = llm_generate_suggestions_and_remediation(user_incident, selected_checklist, broker_questions, broker_answers)
            # Store all relevant context in session state
            st.session_state['last_result'] = {
                'result': result,
                'checklist': selected_checklist.copy(),
                'broker_questions': broker_questions.copy(),
                'broker_answers': broker_answers.copy()
            }
            suggestions = result.get('risk_mitigation', [])
            remediation = result.get('remediation', '')
            recommendation = result.get('recommendation', '')
            confidence = result.get('confidence', '')
            broker_summary = result.get('broker_summary', '')
            explanation = result.get('explanation', '')
    elif 'last_result' in st.session_state:
        # Always show the last result, regardless of changes
        last = st.session_state['last_result']
        suggestions = last['result'].get('risk_mitigation', [])
        remediation = last['result'].get('remediation', '')
        recommendation = last['result'].get('recommendation', '')
        confidence = last['result'].get('confidence', '')
        broker_summary = last['result'].get('broker_summary', '')
        explanation = last['result'].get('explanation', '')

if suggestions:
    st.markdown("### 🛡️ Risk Mitigation Suggestions (AI-generated)")
    for s in suggestions:
        st.write(f"- {s}")
if remediation:
    st.markdown("### 🛠️ Remediation Steps (AI-generated)")
    st.success(remediation)
if recommendation:
    st.markdown("### 📝 Underwriter Recommendation (AI-generated)")
    st.info(f"**Recommendation:** {recommendation}\n\n**Confidence:** {confidence}")
if broker_summary:
    st.markdown("### 📋 Broker Summary (AI-generated)")
    st.text_area("2-line Broker Note", broker_summary, height=68, disabled=True)
if explanation:
    with st.expander("How was this recommendation derived?"):
        st.write("""
        The recommendation is generated by the AI based on:
        - The incident description you provided
        - The underwriting checklist items you selected (which reflect key risk controls and exposures)
        - The broker's Yes/No answers to clarifying questions (which indicate the presence or absence of critical controls)
        - The AI weighs the risk impact, control gaps, and business context to suggest the most appropriate underwriting action (Accept, Request Fix, Decline),
        - The confidence score reflects the AI's certainty based on the completeness and quality of the information provided.
        - The risk mitigation suggestions and remediation steps are tailored to the specific scenario and broker responses, ensuring actionable and relevant guidance for both underwriters and brokers.
        """)

# --- Footnote ---
st.markdown('<hr style="margin-top:2em;">', unsafe_allow_html=True)
st.markdown('<span style="color:red;">This app is for the application of Senior Product Manager, Underwriting AI at Coalition Inc. Only for demo/job application use.</span>', unsafe_allow_html=True)
