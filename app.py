import streamlit as st
import pandas as pd
import json
from memory_engine import SynrixMemoryEngine
from scam_detector import ScamDetector

# Initialize session state for memory and engine
if "memory_engine" not in st.session_state:
    st.session_state.memory_engine = SynrixMemoryEngine()
    st.session_state.last_analysis = None
    
    # Load dummy data
    try:
        with open("dummy_chat_data.json", "r") as f:
            dummy_data = json.load(f)
            for msg in dummy_data:
                st.session_state.memory_engine.add_message(
                    sender=msg["sender"],
                    text=msg["text"],
                    risk_score=msg.get("risk_score"),
                    classification=msg.get("classification")
                )
    except Exception as e:
        pass # Fine if it doesn't exist yet

def get_color(score):
    if score is None:
        return "gray"
    if score < 40:
        return "green"
    elif score < 70:
        return "orange"
    else:
        return "red"

st.set_page_config(page_title="AI Scam & Manipulation Detector", layout="wide")

st.title("🛡️ AI Scam & Manipulation Detector")
st.markdown("A lightweight WhatsApp-style demo powered by **Synrix Memory Engine** logic + **Gemini API**.")

api_key = st.sidebar.text_input("Gemini API Key", type="password")

if api_key:
    scam_detector = ScamDetector(api_key=api_key)
else:
    scam_detector = ScamDetector()
    st.sidebar.warning("Please enter your Gemini API Key above to enable LLM analysis.")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("💬 Chat Interface")
    
    # Display chat
    chat_container = st.container(height=550)
    
    with chat_container:
        for msg in st.session_state.memory_engine.lattice:
            score = msg.get("risk_score")
            color = get_color(score)
            
            is_user = msg["sender"] == "User"
            align = "right" if is_user else "left"
            bg_color = "#DCF8C6" if is_user else "#FFFFFF" # WhatsApp-style colors
            border_color = color if score is not None else "lightgray"
            avatar = "👤" if is_user else "🤖" if msg["sender"] == "Bank Support" else "📱" if msg["sender"] == "Friend" else "❓"
            
            st.markdown(
                f"""
                <div style="text-align: {align}; margin-bottom: 12px; font-family: sans-serif;">
                    <div style="display: inline-block; padding: 12px 16px; border-radius: 12px; background-color: {bg_color}; border: 2px solid {border_color}; max-width: 75%; text-align: left; box-shadow: 1px 1px 3px rgba(0,0,0,0.1);">
                        <div style="font-size: 0.8em; color: gray; margin-bottom: 4px;">{avatar} <b>{msg['sender']}</b></div>
                        <div style="font-size: 1em; color: #333;">{msg['text']}</div>
                        {"<div style='margin-top: 6px; font-size: 0.8em; font-weight: bold; color: "+color+"'>🔍 Risk Score: "+str(score)+" </div>" if score is not None else ""}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
    # Input area
    with st.form("chat_form", clear_on_submit=True):
        new_msg = st.text_input("Type a message or paste a suspicious text...")
        sender = st.selectbox("Sender", ["Unknown Contact", "User", "Bank Support", "Friend"])
        submit_btn = st.form_submit_button("Send & Analyze")
        
        if submit_btn and new_msg:
            # Add to memory
            msg_id = st.session_state.memory_engine.add_message(sender, new_msg)
            
            # Context
            recent_context = st.session_state.memory_engine.get_recent_context(3)
            similar_past = st.session_state.memory_engine.search_similar_messages(new_msg)
            
            # Always analyze even if API key is invalid (falls back to taxonomy)
            with st.spinner("Analyzing message..."):
                analysis = scam_detector.analyze_message(new_msg, recent_context, similar_past)
                st.session_state.memory_engine.update_message_analysis(
                    msg_id, 
                    analysis.get("Final Risk Score", 0), 
                    analysis.get("Taxonomy Classification", "NORMAL")
                )
                st.session_state.last_analysis = analysis
            st.rerun()

    if st.session_state.last_analysis:
        with st.expander("🔍 View Latest Detailed AI Analysis", expanded=True):
            if not api_key:
                 st.warning("⚠️ No valid API Key provided. Only Rule-Based Taxonomy is active.")
            st.json(st.session_state.last_analysis)

with col2:
    st.subheader("Memory & Analytics Viewer")
    
    lattice = st.session_state.memory_engine.lattice
    if lattice:
        df = pd.DataFrame(lattice)
        
        st.write("📊 **Scam Type Statistics**")
        if 'classification' in df.columns and not df['classification'].isnull().all():
            stats = df['classification'].value_counts()
            st.bar_chart(stats)
            
        st.write("🧠 **Conversation Memory (Synrix Style)**")
        st.dataframe(df[['id', 'sender', 'text', 'risk_score', 'classification']].tail(10))
    else:
        st.info("No messages in memory yet.")

    st.subheader("🧪 Custom Message Tester")
    test_msg = st.text_area("Paste suspicious message here to test purely via vectors & taxonomy (without adding to chat)")
    if st.button("Test Message"):
        if not api_key:
            st.error("Please enter Gemini API Key.")
        elif test_msg:
            recent_context = st.session_state.memory_engine.get_recent_context(3)
            similar_past = st.session_state.memory_engine.search_similar_messages(test_msg)
            with st.spinner("Running deep analysis..."):
                analysis = scam_detector.analyze_message(test_msg, recent_context, similar_past)
                st.markdown(f"**Risk Score:** {analysis.get('Final Risk Score')} ({get_color(analysis.get('Final Risk Score')).upper()})")
                st.markdown(f"**Category:** {analysis.get('Taxonomy Classification')}")
                st.markdown(f"**AI Explanation:** {analysis.get('Explanation')}")
                st.markdown(f"**Recommended Action:** {analysis.get('Advice')}")
