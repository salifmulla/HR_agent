# HR Assistant Agent

## Overview
The **HR Assistant Agent** is an AI-powered tool designed to instantly answer employee queries regarding company policies, leave entitlements, benefits, and remote work guidelines. Built for the **48-Hour AI Agent Development Challenge**, this agent leverages Google's Gemini 2.0 Flash model to provide accurate, context-aware responses based on the company's internal handbook.

## Features
- **Instant Policy Answers**: Queries the HR handbook to answer questions about leave, insurance, etc.
- **Context-Aware**: Uses the provided `hr_policy.txt` as a ground-truth knowledge base.
- **User-Friendly Interface**: Built with Streamlit for a clean, chat-like experience.
- **Voice Interface**: Supports speech-to-text for hands-free querying.
- **Email Drafter**: Auto-generates professional emails (e.g., Sick Leave, Resignation) based on policy.
- **Admin Dashboard**: Dedicated panel for HR to update policies dynamically.
- **Secure**: Requires an API key for usage, ensuring control.

## Tech Stack
- **Frontend**: Streamlit (Python)
- **AI Model**: Google Gemini 2.0 Flash (via `google-generativeai`)
- **Data Storage**: Local Text File (Simulated Knowledge Base)

## Setup & Run Instructions

### Prerequisites
- Python 3.8 or higher
- A Google Gemini API Key (Get it [here](https://aistudio.google.com/app/apikey))

### Installation
1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd HR_Assistant_Agent
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Agent
1. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
2. The application will open in your browser (usually at `http://localhost:8501`).
3. Enter your **Google Gemini API Key** in the sidebar.
4. Start asking questions! (e.g., "How many sick leaves do I have?", "Is there gym reimbursement?")

## Architecture
The agent follows a simple RAG-lite (Retrieval-Augmented Generation) architecture:
1. **User Input**: Captures the query via Streamlit.
2. **Context Retrieval**: Loads the `hr_policy.txt` content.
3. **Prompt Engineering**: Combines the role (HR Assistant), the policy context, and the user question.
4. **Inference**: Sends the prompt to Google Gemini 2.0 Flash.
5. **Response**: Displays the AI's answer to the user.

## Future Improvements
- **Vector Database**: Migrate from text file to a Vector DB (e.g., ChromaDB) for handling large documents.
- **Multi-Language Support**: Add support for non-English queries.
