# Remediation Copilot for Coalition Inc.

A Streamlit-based demo app simulating an AI assistant for cybersecurity incident remediation and full underwriting pipeline coverage, inspired by Coalition’s Security Copilot.

## Features
- **Free-text Incident Input:** Enter any incident scenario; the AI parses and drives the workflow.
- **AI-Generated Underwriting Checklist:** LLM suggests checklist items based on the incident.
- **Interactive Checklist Selection:** User selects relevant controls; AI uses these for downstream logic.
- **Dynamic Broker Questions:** LLM generates Yes/No questions tailored to selected checklist items.
- **Risk Mitigation & Remediation:** LLM generates context-aware suggestions and remediation steps based on broker answers.
- **AI Underwriter Recommendation:** LLM provides a recommendation (Accept, Request Fix, Decline) and confidence score.
- **Broker Summary:** LLM condenses the scenario and actions into a 2-line note for brokers.
- **Explainability:** Detailed section explains how the recommendation was derived.
- **Demo Footnote:** App is for the Senior Product Manager, Underwriting AI application at Coalition Inc.

## How to Use
1. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
2. **Set your API keys:**
   - For local use, create `.streamlit/secrets.toml` (not committed to git):
     ```toml
     OPENAI_API_KEY = "sk-..."
     ```
   - For Streamlit Community Cloud, set secrets in the app’s “Settings” → “Secrets” UI.
3. **Run the app:**
   ```sh
   streamlit run app.py
   ```
4. **Workflow:**
   - Enter a free-text incident description (see gray examples in the app).
   - Review and select relevant underwriting checklist items.
   - Answer AI-generated Yes/No broker questions.
   - Click “Generate Remediation & Recommendation” to get AI-driven risk mitigation, remediation, and recommendations.
   - Review the detailed explanation and broker summary.

## Example Prompts
- "A public S3 bucket with sensitive configs was found by our cloud scanner on June 10, 2025."
- "Multiple admin accounts were found using weak passwords and no MFA on June 12, 2025."
- "An unpatched Apache server (2.4.29) with critical CVEs was detected by a vulnerability scan."
- "A phishing email impersonating IT support was reported by several users last week."

## Use Cases
- **Underwriter Triage:** Rapidly assess and document incident risk, remediation, and underwriting actions with AI assistance.
- **Broker Collaboration:** Generate clarifying questions and summaries for brokers to streamline communication.
- **Risk Mitigation Planning:** Get actionable, AI-driven suggestions to reduce cyber risk exposure.
- **Audit & Explainability:** Provide transparent, explainable recommendations and allow human override for compliance.
- **Demo for Cyber Insurance:** Showcase how AI can accelerate and improve the underwriting pipeline for cyber insurance products.

## How the AI Pipeline Works
1. **Incident Parsing:** The LLM parses the free-text incident and generates a tailored underwriting checklist.
2. **Checklist Selection:** User selects controls relevant to the scenario.
3. **Broker Questions:** LLM generates Yes/No questions based on selected checklist items.
4. **Broker Answers:** User answers each question; these responses are used as context for the next step.
5. **Risk Mitigation & Remediation:** LLM generates context-aware suggestions and remediation steps based on the incident, checklist, and broker answers.
6. **Recommendation & Confidence:** LLM provides an underwriting recommendation and confidence score, with a detailed explanation of its reasoning.
7. **Broker Summary:** LLM condenses the scenario and actions into a concise note for brokers.

## Deployment
- Ready for [Streamlit Community Cloud](https://streamlit.io/cloud). Do not commit real secrets—set them in the Cloud UI.

## Context
This app was built as a demo for a job application to [Coalition Inc.](https://www.coalitioninc.com). It demonstrates AI-powered remediation, explainability, and full underwriting workflow for cyber insurance scenarios.


# Remediation Copilot Demo Script

1. **Intro**
   - “This is Remediation Copilot, an AI-powered Streamlit app for underwriters and brokers, inspired by Coalition’s Security Copilot.”

2. **Select an Incident**
   - Use the dropdown to pick an incident (e.g., “RDP Port 3389 Exposed”).

3. **Show Incident Details**
   - Point out the risk contribution, remediation cost, and description.

4. **Generate Remediation**
   - Click “Generate Remediation & Recommendation”.
   - Read out the technical and plain-language remediation steps.

5. **Explainability**
   - Expand “Why was this suggested?” to show the LLM’s reasoning.

6. **Underwriter Recommendation**
   - Highlight the recommended action (e.g., “Request fix”) and confidence score.

7. **Net Risk Visualization**
   - Show the “Net Risk After Remediation” bar and explain how risk is reduced.

8. **Broker Summary**
   - Show the concise broker note.

9. **Explain Recommendation Logic**
   - Expand “How was this recommendation derived?” for transparency.

10. **Wrap Up**
    - “This app demonstrates explainable, AI-driven remediation and risk simulation for cyber insurance workflows.”
