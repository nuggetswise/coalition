# Remediation Copilot for Coalition Inc.

A Streamlit-based demo app simulating an AI assistant for cybersecurity incident remediation and full underwriting pipeline coverage, inspired by Coalition’s Security Copilot.

## Features
- **Incident Selector:** Choose from sample cybersecurity incidents.
- **AI Remediation Suggestions:** Uses OpenAI, Groq, Gemini, or Cohere (if API key set) to suggest technical and plain-language remediation steps, with explanations. No stub fallback—an API key is required.
- **Editable Underwriting Checklist:** AI pre-fills a checklist for underwriters to review and mark as complete.
- **GPT-Generated Broker Questions:** AI suggests clarifying questions for brokers to answer.
- **Risk Mitigation Suggestions:** AI recommends additional risk reduction steps.
- **Before/After Triage Comparison:** Visualizes time and quality difference between AI and manual triage.
- **Confidence Score + Human Override:** Shows AI confidence and allows underwriter to override the recommendation.
- **Broker Summary Generator:** Condenses remediation into a 2-line summary for brokers, with copy-to-clipboard.
- **Explainability:** Shows reasoning behind suggestions and recommendations.
- **Net Risk Visualization:** See risk reduction after remediation and recommendation.

## How to Use
1. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
2. **Set your API keys:**
   - For local use, create `.streamlit/secrets.toml` (not committed to git):
     ```toml
     OPENAI_API_KEY = "sk-..."
     GROQ_API_KEY = "gsk-..."
     GEMINI_API_KEY = "..."
     COHERE_API_KEY = "..."
     ```
   - For Streamlit Community Cloud, set secrets in the app’s “Settings” → “Secrets” UI.
3. **Run the app:**
   ```sh
   streamlit run app.py
   ```
4. **Workflow:**
   - Select an incident from the dropdown.
   - Review and edit the AI-generated underwriting checklist.
   - Answer AI-generated broker questions.
   - Review risk mitigation suggestions.
   - Click “Generate Remediation & Recommendation” for AI-powered remediation, explanation, and recommendation.
   - Optionally override the AI recommendation as a human underwriter.
   - Compare AI vs. manual triage time/quality.
   - See net risk after remediation and a broker summary note.

## Use Cases
- **Underwriter Triage:** Rapidly assess and document incident risk, remediation, and underwriting actions with AI assistance.
- **Broker Collaboration:** Generate clarifying questions and summaries for brokers to streamline communication.
- **Risk Mitigation Planning:** Get actionable, AI-driven suggestions to reduce cyber risk exposure.
- **Audit & Explainability:** Provide transparent, explainable recommendations and allow human override for compliance.
- **Demo for Cyber Insurance:** Showcase how AI can accelerate and improve the underwriting pipeline for cyber insurance products.

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
