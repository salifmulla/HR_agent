import streamlit as st
import google.generativeai as genai
import os
from streamlit_mic_recorder import speech_to_text

# FOR TESTING ONLY: Enter your API key here. Leave empty for production/submission.
HARDCODED_API_KEY = ""

# Page Config
st.set_page_config(page_title="HR Assistant Agent", page_icon="👔", layout="centered")

# Title and Description
st.title("👔 HR Assistant Agent")
st.markdown("""
This agent helps you with questions regarding company policies, leave, benefits, and more.
It uses the **Gemini 2.0 Flash** model to answer your queries based on the company handbook.
""")

# Sidebar for API Key
with st.sidebar:
    st.header("Configuration")
    if HARDCODED_API_KEY:
        api_key = HARDCODED_API_KEY
        st.success("Using hardcoded API key")
    else:
        api_key = st.text_input("Enter Google Gemini API Key", type="password")
    st.markdown("[Get your API Key here](https://aistudio.google.com/app/apikey)")
    st.markdown("---")
    st.markdown("### About")
    st.markdown("Built for the **48-Hour AI Agent Development Challenge**.")

# Load Knowledge Base
def load_policy():
    try:
        with open("hr_policy.txt", "r") as f:
            return f.read()
    except FileNotFoundError:
        return "Error: hr_policy.txt not found."

def save_policy(text):
    with open("hr_policy.txt", "w") as f:
        f.write(text)

# --- Interfaces ---

def employee_interface(api_key):
    st.header("💬 Employee Helpdesk")
    
    # Tabs for different features
    tab1, tab2 = st.tabs(["Ask a Question", "📧 Email Drafter"])
    
    policy_text = load_policy()

    with tab1:
        st.markdown("Ask questions about company policies, leave, and benefits.")
        # Chat Interface
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Input Area
        prompt = st.chat_input("Ask about leave, benefits, or remote work...")
        
        # Voice Input in Sidebar
        with st.sidebar:
            st.markdown("### 🎙️ Voice Input")
            # speech_to_text returns the transcribed text directly
            voice_text = speech_to_text(language='en', start_prompt="Start Recording", stop_prompt="Stop Recording", just_once=False, key='STT')
        
        # Handle Input
        if prompt or voice_text:
            if not api_key:
                st.error("Please enter your Google Gemini API Key in the sidebar to proceed.")
            else:
                if prompt:
                    user_input = prompt
                elif voice_text:
                    user_input = voice_text
                    st.sidebar.success(f"Heard: '{user_input}'")
                
                # Add user message to state
                st.session_state.messages.append({"role": "user", "content": user_input})
                with st.chat_message("user"):
                    st.markdown(user_input)

                # Generate Response
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-2.0-flash')
                    
                    # Construct System Prompt
                    system_prompt = f"""
                    You are a helpful and professional HR Assistant for a company.
                    Your goal is to answer employee questions based STRICTLY on the provided policy document below.
                    
                    If the answer is not in the document, politely say you don't have that information and suggest contacting HR directly.
                    Keep answers concise and friendly.
                    
                    ---
                    POLICY DOCUMENT:
                    {policy_text}
                    ---
                    """
                    
                    with st.chat_message("assistant"):
                        with st.spinner("Thinking..."):
                            # Always text-only request now (since voice is converted to text)
                            full_prompt = f"{system_prompt}\n\nUser Question: {user_input}\nAnswer:"
                            response = model.generate_content(full_prompt)
                                
                            st.markdown(response.text)
                    
                    st.session_state.messages.append({"role": "assistant", "content": response.text})

                except Exception as e:
                    st.error(f"An error occurred: {e}")

    with tab2:
        st.header("Email Drafter")
        st.markdown("Generate professional emails based on company policy.")
        
        col1, col2 = st.columns(2)
        with col1:
            recipient = st.text_input("Recipient Name (e.g., Manager)")
        with col2:
            email_type = st.selectbox("Email Type", ["Sick Leave", "Annual Leave", "Remote Work Request", "Resignation", "General Inquiry"])
            
        details = st.text_area("Additional Details (e.g., dates, reason, specific questions)")
        
        if st.button("Draft Email"):
            if not api_key:
                st.error("Please enter your API Key first.")
            else:
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-2.0-flash')
                    
                    email_prompt = f"""
                    You are a professional HR Assistant. Draft a formal email for an employee based on the following details and the company policy.
                    
                    Recipient: {recipient}
                    Type: {email_type}
                    Details: {details}
                    
                    Ensure the email adheres to the following policy:
                    {policy_text}
                    
                    If the request violates policy (e.g., too many leave days), mention it politely in the draft or add a note.
                    """
                    
                    with st.spinner("Drafting email..."):
                        response = model.generate_content(email_prompt)
                        st.text_area("Generated Draft", value=response.text, height=300)
                except Exception as e:
                    st.error(f"Error: {e}")

def admin_interface():
    st.header("🔒 HR Admin Panel")
    st.markdown("Update the company policy document directly from here.")
    
    # Simple Password Protection
    password = st.text_input("Enter Admin Password", type="password")
    
    if password == "admin123":  # Simple hardcoded password for demo
        st.success("Access Granted")
        
        current_policy = load_policy()
        new_policy = st.text_area("Edit Policy Document", value=current_policy, height=400)
        
        if st.button("Save Changes"):
            save_policy(new_policy)
            st.success("Policy updated successfully! The agent will now use the new information.")
            st.rerun()
    elif password:
        st.error("Incorrect Password")

# --- Main App Logic ---

# Sidebar Navigation
with st.sidebar:
    st.markdown("---")
    app_mode = st.radio("Navigate", ["Employee Chat", "HR Admin"])

if app_mode == "Employee Chat":
    employee_interface(api_key)
elif app_mode == "HR Admin":
    admin_interface()
