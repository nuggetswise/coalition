# Remediation Copilot for Coalition Inc.

A Streamlit-based demo app simulating an AI assistant for cybersecurity incident remediation, inspired by Coalition’s Security Copilot.

## Features
- **Incident Selector:** Choose from sample cybersecurity incidents.
- **AI Remediation Suggestions:** Uses OpenAI (if API key set), else Gemini, else Cohere to suggest technical and plain-language remediation steps, with explanations. **No stub fallback—an API key is required.**
- **Broker Summary Generator:** Condenses remediation into a 2-line summary for brokers, with copy-to-clipboard.
- **Explainability Toggle:** Shows reasoning behind suggestions.
- **Risk Score Simulator:** Simulate risk score improvement after remediation.

## Files
- `app.py` — Main Streamlit app
- `data/sample_incidents.json` — Mock incident data
- `utils.py` — LLM logic
- `requirements.txt` — Dependencies
- `.streamlit/config.toml` — Streamlit config (add if deploying)
- `.streamlit/secrets.toml` — API keys (add if using LLMs)

## Setup & Run
1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Add your API key(s) to `.streamlit/secrets.toml` or as environment variables:
   ```toml
   OPENAI_API_KEY = "sk-..."      # Preferred
   GEMINI_API_KEY = "..."         # Fallback
   COHERE_API_KEY = "..."         # Last fallback
   ```
   - At least one key is required. The app will use OpenAI if available, else Gemini, else Cohere.
3. Run the app:
   ```sh
   streamlit run app.py
   ```
   - The app will open in your browser. If no valid API key is set, you will see an error.

## Deployment
- Ready for [Streamlit Community Cloud](https://streamlit.io/cloud). Ensure `config.toml` and `secrets.toml` are in `.streamlit/`.
- In the Streamlit Cloud UI, set your secrets under “App settings” → “Secrets”.

## Context
This app was built as a demo for a job application to [Coalition Inc.](https://www.coalitioninc.com). It demonstrates AI-powered remediation, explainability, and broker communication for cyber insurance scenarios.


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
