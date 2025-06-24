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
    Returns a list of incident-specific Yes/No questions for brokers.
    """
    title = incident['title'].lower()
    description = incident['description'].lower()
    questions = []
    if "mfa" in title or "mfa" in description or "multi-factor" in description:
        questions.append("Is Multi-Factor Authentication (MFA) enabled for all relevant accounts?")
    if "rdp" in title or "remote desktop" in description:
        questions.append("Is RDP access restricted to VPN or internal networks only?")
    if "patch" in title or "outdated" in description or "unpatched" in description:
        questions.append("Are all systems fully patched and up to date?")
    if "public" in title or "exposed" in description:
        questions.append("Are any sensitive resources exposed to the public internet?")
    if not questions:
        questions = [
            "Are there compensating controls in place for this risk?",
            "Has this incident type occurred before? If so, was it remediated?"
        ]
    return questions

def adjust_risk_and_suggestions(incident, broker_answers):
    """
    Adjusts risk mitigation suggestions and remediation steps based on Yes/No broker answers.
    Returns (suggestions, adjusted_remediation, risk_modifier)
    """
    suggestions = generate_risk_mitigation_suggestions(incident)
    adjusted_remediation = None
    risk_modifier = 1.0
    # If any answer is 'No', increase risk and add more suggestions
    if any(ans == 'No' for ans in broker_answers):
        suggestions.append("Escalate to security team for urgent review.")
        adjusted_remediation = "Immediate action required: address all 'No' responses before proceeding."
        risk_modifier = 1.2  # Increase risk by 20%
    elif all(ans == 'Yes' for ans in broker_answers) and broker_answers:
        suggestions.append("No additional broker action required; all controls confirmed.")
        adjusted_remediation = "Proceed with standard remediation as all controls are in place."
        risk_modifier = 0.8  # Decrease risk by 20%
    return suggestions, adjusted_remediation, risk_modifier

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

def generate_dynamic_risk_mitigation_suggestions(incident, broker_answers):
    """
    Uses LLM to generate context-aware risk mitigation suggestions based on incident and broker answers.
    """
    title = incident['title']
    description = incident['description']
    risk = incident.get('risk_level', '')
    openai_key = os.getenv('OPENAI_API_KEY')
    prompt = (
        f"Incident: {title}\nDescription: {description}\nRisk: {risk}\n"
        f"Broker Answers: {broker_answers}\n"
        "Suggest 3-5 specific, actionable risk mitigation steps for this scenario."
    )
    if openai and openai_key:
        openai.api_key = openai_key
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        text = resp.choices[0].message.content.strip()
        suggestions = [line.strip('- ').strip() for line in text.split('\n') if line.strip()]
        return suggestions
    # fallback to static if no LLM
    return generate_risk_mitigation_suggestions(incident)

def llm_parse_incident_and_generate_all(incident_text):
    """
    Uses LLM to parse a free-text incident and generate:
    - checklist (list of strings)
    - broker_questions (list of strings)
    - risk_mitigation (list of strings)
    - remediation (string)
    - recommendation (string)
    - confidence (float or string)
    - broker_summary (string)
    - explanation (string)
    """
    openai_key = os.getenv('OPENAI_API_KEY')
    prompt = (
        f"Incident: {incident_text}\n"
        "Parse the above incident and generate the following as JSON:\n"
        "{\n"
        "  'checklist': [list of underwriting checklist items],\n"
        "  'broker_questions': [list of yes/no questions for brokers],\n"
        "  'risk_mitigation': [list of risk mitigation suggestions],\n"
        "  'remediation': 'remediation steps',\n"
        "  'recommendation': 'underwriter recommendation',\n"
        "  'confidence': confidence_score (0-1),\n"
        "  'broker_summary': '2-line broker summary',\n"
        "  'explanation': 'explain how the recommendation was derived'\n"
        "}\n"
        "Respond with only the JSON."
    )
    if openai and openai_key:
        openai.api_key = openai_key
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        import json as pyjson
        try:
            data = pyjson.loads(resp.choices[0].message.content.strip().replace("'", '"'))
        except Exception:
            data = {}
        return data
    # fallback: static stub
    return {
        'checklist': ["Confirm asset inventory", "Verify patch status", "Check MFA enforcement"],
        'broker_questions': ["Is MFA enabled?", "Are all systems patched?"],
        'risk_mitigation': ["Upgrade all services", "Implement monitoring"],
        'remediation': "Disable public access and enforce MFA.",
        'recommendation': "Request fix",
        'confidence': 0.8,
        'broker_summary': "Incident triaged, remediation in progress.",
        'explanation': "Recommendation is based on risk and missing controls."
    }

def llm_generate_broker_questions_from_checklist(incident_text, checklist_items):
    openai_key = os.getenv('OPENAI_API_KEY')
    prompt = (
        f"Incident: {incident_text}\n"
        f"Selected Underwriting Checklist: {checklist_items}\n"
        "Generate a list of yes/no broker questions that clarify the status of the selected controls. Respond as a JSON list."
    )
    if openai and openai_key:
        openai.api_key = openai_key
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        import json as pyjson
        try:
            questions = pyjson.loads(resp.choices[0].message.content.strip().replace("'", '"'))
        except Exception:
            questions = []
        return questions
    # fallback
    return ["Is MFA enabled?", "Are all systems patched?"]

def llm_generate_suggestions_and_remediation(incident_text, checklist_items, broker_questions, broker_answers):
    openai_key = os.getenv('OPENAI_API_KEY')
    prompt = (
        f"Incident: {incident_text}\n"
        f"Selected Underwriting Checklist: {checklist_items}\n"
        f"Broker Questions: {broker_questions}\n"
        f"Broker Answers: {broker_answers}\n"
        "Based on the above, generate the following as JSON:\n"
        "{\n"
        "  'risk_mitigation': [list of risk mitigation suggestions],\n"
        "  'remediation': 'remediation steps',\n"
        "  'recommendation': 'underwriter recommendation',\n"
        "  'confidence': confidence_score (0-1),\n"
        "  'broker_summary': '2-line broker summary',\n"
        "  'explanation': 'explain how the recommendation was derived'\n"
        "}\n"
        "Respond with only the JSON."
    )
    if openai and openai_key:
        openai.api_key = openai_key
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        import json as pyjson
        try:
            data = pyjson.loads(resp.choices[0].message.content.strip().replace("'", '"'))
        except Exception:
            data = {}
        return data
    # fallback
    return {
        'risk_mitigation': ["Upgrade all services", "Implement monitoring"],
        'remediation': "Disable public access and enforce MFA.",
        'recommendation': "Request fix",
        'confidence': 0.8,
        'broker_summary': "Incident triaged, remediation in progress.",
        'explanation': "Recommendation is based on risk and missing controls."
    }
