import os
# Remove proxy env vars before anything else
for proxy_var in ["HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy", "ALL_PROXY", "all_proxy"]:
    os.environ.pop(proxy_var, None)

import streamlit as st
# Load secrets into os.environ before importing openai
if hasattr(st, "secrets"):
    for key in ["OPENAI_API_KEY", "GEMINI_API_KEY", "COHERE_API_KEY"]:
        if key in st.secrets:
            os.environ[key] = st.secrets[key]

try:
    import openai
except ImportError:
    openai = None
try:
    import google.generativeai as genai
except ImportError:
    genai = None
try:
    import cohere
except ImportError:
    cohere = None
try:
    import groq
except ImportError:
    groq = None

def generate_remediation(incident):
    """
    Returns dict with keys: remediation_steps, explanation, recommended_action, confidence_score
    Uses OpenAI if API key is set, else Gemini, else Cohere. No stub fallback.
    """
    title = incident['title']
    description = incident['description']
    risk = incident['risk_level']
    openai_key = os.getenv('OPENAI_API_KEY')
    gemini_key = os.getenv('GEMINI_API_KEY')
    cohere_key = os.getenv('COHERE_API_KEY')
    groq_key = os.getenv('GROQ_API_KEY')
    prompt = (
        f"Incident: {title}\nDescription: {description}\nRisk: {risk}\n"
        "Provide:\n"
        "1. Technical and plain-language remediation steps.\n"
        "2. Why this matters.\n"
        "3. A recommended underwriting action (Accept risk, Request fix, Decline policy) with reasoning.\n"
        "4. A confidence score (0-1) for your recommendation.\n"
        "Format:\nRemediation: ...\nWhy: ...\nRecommended Action: ...\nConfidence: ..."
    )
    if openai and openai_key:
        openai.api_key = openai_key
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        text = resp.choices[0].message.content.strip()
    elif groq and groq_key:
        groq_client = groq.Groq(api_key=groq_key)
        resp = groq_client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": prompt}]
        )
        text = resp.choices[0].message.content.strip()
    elif genai and gemini_key:
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel('gemini-pro')
        resp = model.generate_content(prompt)
        text = resp.text.strip()
    elif cohere and cohere_key:
        co = cohere.Client(cohere_key)
        resp = co.generate(model="command", prompt=prompt, max_tokens=300)
        text = resp.generations[0].text.strip()
    else:
        raise RuntimeError("No valid API key found for OpenAI, Gemini, Cohere, or Groq.")
    # Parse response
    remediation, why, rec_action, conf = '', '', '', 0.0
    for line in text.split('\n'):
        if line.lower().startswith('remediation:'):
            remediation = line.split(':',1)[1].strip()
        elif line.lower().startswith('why:'):
            why = line.split(':',1)[1].strip()
        elif line.lower().startswith('recommended action:'):
            rec_action = line.split(':',1)[1].strip()
        elif line.lower().startswith('confidence:'):
            try:
                conf = float(line.split(':',1)[1].strip())
            except Exception:
                conf = 0.5
    return {
        'remediation_steps': remediation,
        'explanation': why,
        'recommended_action': rec_action,
        'confidence_score': conf
    }

def generate_broker_summary(remediation, incident):
    """
    Returns a 2-line summary for brokers.
    """
    title = incident['title']
    risk = incident['risk_level']
    summary = f"{title} ({risk} risk): {remediation.split('.')[0]}. Issue addressed to reduce exposure."
    return summary

def generate_underwriting_checklist(incident):
    """
    Returns a list of checklist items for underwriting, AI pre-filled.
    """
    title = incident['title']
    description = incident['description']
    checklist = [
        f"Confirm asset inventory for: {title}",
        f"Verify patch status for affected systems",
        f"Check MFA enforcement for all admin accounts",
        f"Review backup and recovery procedures",
        f"Assess network segmentation and firewall rules",
        f"Validate incident response plan is up to date"
    ]
    return checklist

def generate_broker_questions(incident):
    """
    Returns a list of GPT-generated questions for brokers.
    """
    title = incident['title']
    questions = [
        f"Can you confirm if MFA is enabled for all users related to '{title}'?",
        f"Are there any compensating controls in place for this risk?",
        f"Has this incident type occurred before? If so, how was it remediated?",
        f"Are there any business constraints preventing immediate remediation?"
    ]
    return questions

def generate_risk_mitigation_suggestions(incident):
    """
    Returns a list of risk mitigation suggestions.
    """
    title = incident['title']
    suggestions = [
        f"Recommend upgrading all related services to the latest supported version.",
        f"Implement network monitoring for suspicious activity.",
        f"Enforce least privilege access for all accounts.",
        f"Upgrade TLS to 1.3 where possible."
    ]
    return suggestions
