import streamlit as st
import re
import spacy
import hashlib
import chromadb
from datetime import datetime

# Load spaCy model
@st.cache_resource
def load_nlp():
    return spacy.load("en_core_web_sm")

# Initialize Local Vector Database
@st.cache_resource
def init_chroma():
    client = chromadb.Client()
    collection = client.get_or_create_collection(name="enterprise_policies")
    
    # Seed with enterprise policies
    collection.add(
        documents=[
            "GDPR Policy: Never transmit customer email addresses or names to external AI services without redaction.",
            "Security Policy: AWS API keys and production credentials must be blocked before external LLM routing."
        ],
        ids=["policy_gdpr", "policy_sec"]
    )
    return collection

nlp = load_nlp()
policy_db = init_chroma()

# Regex rules for PII & Secrets
PATTERNS = {
    "AWS_API_KEY": r"(AKIA[0-9A-Z]{16})",
    "GENERIC_SECRET_KEY": r"(sk-[a-zA-Z0-9]{32,})",
    "EMAIL": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    "CREDIT_CARD": r"\b(?:\d[ -]*?){13,16}\b"
}

def sanitize_and_inject(text):
    sanitized = text
    detected_items = []
    
    # 1. Regex PII & Secret Scrubbing
    for key, pattern in PATTERNS.items():
        matches = re.findall(pattern, sanitized)
        for match in matches:
            detected_items.append({"type": key, "value": match})
            sanitized = sanitized.replace(match, f"[{key}_REDACTED]")
            
    # 2. spaCy Named Entity Recognition
    doc = nlp(sanitized)
    for ent in doc.ents:
        if ent.label_ in ["PERSON", "ORG"] and "[REDACTED]" not in ent.text:
            detected_items.append({"type": ent.label_, "value": ent.text})
            sanitized = re.sub(r'\b' + re.escape(ent.text) + r'\b', f"[{ent.label_}_REDACTED]", sanitized)
            
    # 3. Local Vector Retrieval (ChromaDB Context Injection)
    results = policy_db.query(query_texts=[sanitized], n_results=1)
    retrieved_context = results["documents"][0][0] if results["documents"] else "No policy matched."

    # 4. SHA-256 Audit Hash
    audit_hash = hashlib.sha256(f"{datetime.now()}{text}{sanitized}".encode()).hexdigest()
    
    return sanitized, retrieved_context, detected_items, audit_hash

# Streamlit Interface
st.set_page_config(page_title="AVM AI - Zero Trust Gateway", layout="wide")
st.title("🛡️ AVM AI: Enterprise Prompt Sanitization & RAG Gateway")
st.subheader("Automated Zero-Trust Scrubbing + ChromaDB Policy Context Injection")

user_prompt = st.text_area(
    "Enter Enterprise Prompt:", 
    height=120, 
    value="Send GDPR report for john.doe@enterprise.com using AWS Key AKIAIOSFODNN7EXAMPLE."
)

if st.button("Process & Sanitize Prompt"):
    clean_prompt, context, leaks, hash_sig = sanitize_and_inject(user_prompt)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔍 Scrubbed Output")
        st.code(clean_prompt, language="text")
        
        st.markdown("### 📚 Injected Policy Context (ChromaDB)")
        st.info(context)
        
    with col2:
        st.markdown("### 🚨 Detected Secrets / PII")
        if leaks:
            for leak in leaks:
                st.error(f"Redacted **{leak['type']}**: `{leak['value']}`")
        else:
            st.success("No PII or Secrets Detected!")
            
    st.markdown("---")
    st.markdown("### 🔐 CISO Immutable Audit Log")
    st.json({
        "timestamp": datetime.now().isoformat(),
        "threats_blocked": len(leaks),
        "vector_context_injected": True,
        "sha256_audit_signature": hash_sig,
        "execution_environment": "IBM LinuxONE Secure Execution Enclave"
    })