# AI Scam & Manipulation Detector

A small but functional AI demo project that detects manipulation, scams, and psychological pressure in chat conversations.

The demo simulates a WhatsApp-style chat interface, using **Streamlit** for the UI, **Gemini API** for AI reasoning, **FAISS & Sentence Transformers** for vector memory, and **Synrix Memory Engine logic** for state tracking.

## Installation

1. Clone or download this project.
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```
3. Get a Gemini API Key from [Google AI Studio](https://aistudio.google.com).

## Running the Demo

1. Run the Streamlit app:
```bash
streamlit run app.py
```
2. Open the URL provided in your terminal (usually `http://localhost:8501`).
3. Enter your Gemini API key in the sidebar.
4. Add messages to the chat interface or use the custom message tester to see the AI detect scams, psychological pressure, and context-based manipulation!
