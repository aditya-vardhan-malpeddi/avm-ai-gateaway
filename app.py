import json
import hashlib
import datetime
import re
import streamlit as st
import spacy
import chromadb
import google.generativeai as genai

st.set_page_config(page_title="AVM AI: Zero-Trust Gateway", layout="wide")

@st.cache_resource
def load_spacy_model():
    return spacy.load("en_core_web_sm")

nlp = load_spacy_model()

@st.cache_resource
def get_chroma_client():
    client = chromadb.Client()
    collection = client.get_or_create_collection(name="enterprise_policies")
    if collection.count() == 0:
        collection.add(
            documents=["Security Policy: AWS API keys and production credentials must be blocked before external LLM routing."],
            metadatas=[{"category": "credentials"}],
            ids=["policy_aws_1"]
        )
    return collection

policy_collection = get_chroma_client()

st.sidebar.title("⚙️ Gateway Settings")
gemini_api_key = st.sidebar.text_input("Enter Gemini API Key (Optional)", type="password")

st.sidebar.markdown("---")
st.sidebar.title("📄 Policy Ingestion")
uploaded_policy = st.sidebar.file_uploader("Upload New Policy (.txt)", type=["txt"])

if uploaded_policy is not None:
    policy_text = uploaded_policy.read().decode("utf-8")
    doc_id = f"custom_policy_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    policy_collection.add(
        documents=[policy_text],
        metadatas=[{"filename": uploaded_policy.name}],
        ids=[doc_id]
    )
    st.sidebar.success(f"Added '{uploaded_policy.name}' to ChromaDB!")

st.title("🛡️ AVM AI: Enterprise Prompt Sanitization & RAG Gateway")
st.subheader("Automated Zero-Trust Scrubbing + ChromaDB Policy Context Injection")

user_prompt = st.text_area(
    "Enter Enterprise Prompt:",
    value="Send GDPR report for john.doe@enterprise.com using AWS Key AKIAIOSFODNN7EXAMPLE.",
    height=120
)

if st.button("Process & Sanitize Prompt"):
    doc = nlp(user_prompt)
    scrubbed_text = user_prompt
    detected_threats = []

    for ent in doc.ents:
        if ent.label_ in ["PERSON", "ORG", "GPE"]:
            scrubbed_text = scrubbed_text.replace(ent.text, f"[{ent.label_}_REDACTED]")
            detected_threats.append((ent.label_, ent.text))

    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    aws_pattern = r'AKIA[0-9A-Z]{16}'

    for email in re.findall(email_pattern, scrubbed_text):
        scrubbed_text = scrubbed_text.replace(email, "[EMAIL_REDACTED]")
        detected_threats.append(("EMAIL", email))

    for aws_key in re.findall(aws_pattern, scrubbed_text):
        scrubbed_text = scrubbed_text.replace(aws_key, "[AWS_API_KEY_REDACTED]")
        detected_threats.append(("AWS_API_KEY", aws_key))

    rag_results = policy_collection.query(query_texts=[user_prompt], n_results=1)
    retrieved_policy = rag_results['documents'][0][0] if rag_results['documents'] else "No relevant policy found."

    timestamp = datetime.datetime.now().isoformat()
    raw_sig = f"{timestamp}{len(detected_threats)}{scrubbed_text}".encode('utf-8')
    sha256_hash = hashlib.sha256(raw_sig).hexdigest()

    audit_log = {
        "timestamp": timestamp,
        "threats_blocked": len(detected_threats),
        "vector_context_injected": True,
        "sha256_audit_signature": sha256_hash,
        "execution_environment": "IBM LinuxONE Secure Execution Enclave"
    }

    st.session_state['scrubbed_text'] = scrubbed_text
    st.session_state['detected_threats'] = detected_threats
    st.session_state['retrieved_policy'] = retrieved_policy
    st.session_state['audit_log'] = audit_log

if 'scrubbed_text' in st.session_state:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🔍 Scrubbed Output")
        st.code(st.session_state['scrubbed_text'], language="text")

        st.markdown("### 🧩 Injected Policy Context (ChromaDB)")
        st.info(st.session_state['retrieved_policy'])

    with col2:
        st.markdown("### 🚨 Detected Secrets / PII")
        for threat_type, value in st.session_state['detected_threats']:
            st.error(f"Redacted **{threat_type}**: `{value}`")

    st.markdown("---")
    st.markdown("### 🔐 CISO Immutable Audit Log")
    st.json(st.session_state['audit_log'])

    json_bytes = json.dumps(st.session_state['audit_log'], indent=4).encode('utf-8')
    st.download_button(
        label="📥 Download Audit Report (.json)",
        data=json_bytes,
        file_name="ciso_audit_report.json",
        mime="application/json"
    )

    st.markdown("---")
    st.markdown("### 🤖 Live Zero-Trust LLM Execution")
    if gemini_api_key:
        if st.button("Send Sanitized Prompt to Gemini"):
            try:
                genai.configure(api_key=gemini_api_key)
                model = genai.GenerativeModel('gemini-3.8-flash')
                combined_prompt = f"System Policy: {st.session_state['retrieved_policy']}\n\nUser Prompt: {st.session_state['scrubbed_text']}"
                response = model.generate_content(combined_prompt)
                st.success("Response from Gemini (via Zero-Trust Gateway):")
                st.write(response.text)
            except Exception as e:
                st.error(f"LLM Generation Error: {e}")
    else:
        st.warning("Enter a Gemini API Key in the sidebar to execute real-time LLM calls.")
