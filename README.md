# 🛡️ AVM AI – Enterprise Zero-Trust Governance & RAG Gateway

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://avm-ai-gateaway-ygws33apofjmpmuwghvkyu.streamlit.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

🚀 **Live Deployment:** [Access AVM AI Gateway](https://avm-ai-gateaway-ygws33apofjmpmuwghvkyu.streamlit.app/)

---

## 📌 Problem Statement
As enterprises adopt Generative AI, employees frequently process internal data through public LLMs. This introduces critical security risks, including:
* **Data Leakage**: Unintentional disclosure of Personally Identifiable Information (PII), API keys, and server infrastructure[cite: 1].
* **Compliance Violations**: Non-compliance with enterprise policy guidelines (e.g., spending limits, authorization matrices)[cite: 6].
* **Lack of Auditability**: Inability for CISOs and security officers to trace or verify prompts sent to cloud LLM providers.

---

## 💡 Solution Architecture: AVM AI Gateway
**AVM AI** operates as a confidential Zero-Trust Proxy between internal users and public LLM providers[cite: 1]. It processes every prompt through a dual-pipeline governance engine:

1. **Real-time PII & Secret Redaction Engine**: Employs spaCy Named Entity Recognition (NER) and regex patterns to strip sensitive PII, email addresses, production URLs, and API credentials before sending prompts upstream.
2. **RAG-based Dynamic Policy Injection**: Integrates ChromaDB vector storage to perform semantic retrieval of corporate compliance policies and automatically append active constraints into the system context[cite: 6].
3. **Cryptographic CISO Audit Telemetry**: Generates an immutable audit trail tagged with SHA-256 signatures and execution environment metadata simulating an **IBM LinuxONE Secure Execution Enclave**[cite: 5].

---

## 🛠️ Tech Stack
* **Frontend / UI**: Streamlit[cite: 1]
* **NLP & Redaction**: spaCy (`en_core_web_sm`), Regex Engine[cite: 1, 6]
* **Vector Store (RAG)**: ChromaDB[cite: 1]
* **Model Integration**: Google Generative AI (`gemini-3.8-flash` via API)[cite: 1]
* **Security & Auditing**: SHA-256 Hash Signature Generator, JSON Telemetry Exporter[cite: 5]

---

## 🚀 Quickstart & Local Setup

### Prerequisites
* Python 3.10+
* Google Gemini API Key

### Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/aditya-vardhan-malpeddi/avm-ai-gateaway.git](https://github.com/aditya-vardhan-malpeddi/avm-ai-gateaway.git)
   cd avm-ai-gateawaypip install -r requirements.txt
python -m spacy download en_core_web_sm
streamlit run app.py
Copy and paste the entire block below directly into your **`README.md`** file on GitHub:

```markdown
# 🛡️ AVM AI – Enterprise Zero-Trust Governance & RAG Gateway

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://avm-ai-gateaway-ygws33apofjmpmuwghvkyu.streamlit.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

🚀 **Live Deployment:** [Access AVM AI Gateway](https://avm-ai-gateaway-ygws33apofjmpmuwghvkyu.streamlit.app/)

---

## 📌 Problem Statement
As enterprises adopt Generative AI, employees frequently process internal data through public LLMs. This introduces critical security risks, including:
* **Data Leakage**: Unintentional disclosure of Personally Identifiable Information (PII), API keys, and server infrastructure[cite: 1].
* **Compliance Violations**: Non-compliance with enterprise policy guidelines (e.g., spending limits, authorization matrices)[cite: 6].
* **Lack of Auditability**: Inability for CISOs and security officers to trace or verify prompts sent to cloud LLM providers[cite: 5].

---

## 💡 Solution Architecture: AVM AI Gateway
**AVM AI** operates as a confidential Zero-Trust Proxy between internal users and public LLM providers[cite: 1]. It processes every prompt through a dual-pipeline governance engine:

1. **Real-time PII & Secret Redaction Engine**: Employs spaCy Named Entity Recognition (NER) and regex patterns to strip sensitive PII, email addresses, production URLs, and API credentials before sending prompts upstream[cite: 1, 6].
2. **RAG-based Dynamic Policy Injection**: Integrates ChromaDB vector storage to perform semantic retrieval of corporate compliance policies and automatically append active constraints into the system context[cite: 6].
3. **Cryptographic CISO Audit Telemetry**: Generates an immutable audit trail tagged with SHA-256 signatures and execution environment metadata simulating an **IBM LinuxONE Secure Execution Enclave**[cite: 5].

---

## 🛠️ Tech Stack
* **Frontend / UI**: Streamlit[cite: 1]
* **NLP & Redaction**: spaCy (`en_core_web_sm`), Regex Engine[cite: 1, 6]
* **Vector Store (RAG)**: ChromaDB[cite: 1]
* **Model Integration**: Google Generative AI (`gemini-3.8-flash` via API)[cite: 1]
* **Security & Auditing**: SHA-256 Hash Signature Generator, JSON Telemetry Exporter[cite: 5]

---

## 🚀 Quickstart & Local Setup

### Prerequisites
* Python 3.10+
* Google Gemini API Key

### Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/aditya-vardhan-malpeddi/avm-ai-gateaway.git](https://github.com/aditya-vardhan-malpeddi/avm-ai-gateaway.git)
   cd avm-ai-gateaway

```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm

```


3. **Launch the app:**
```bash
streamlit run app.py

```



---

## 🔒 Security & Compliance

All user prompt inputs are sanitized prior to network transport. Cryptographic hash outputs can be exported directly as `.json` reports to fulfill SOC2, HIPAA, and GDPR audit logging requirements.

```

---

### Steps on GitHub:
1. Open your repository at `[github.com/aditya-vardhan-malpeddi/avm-ai-gateaway](https://github.com/aditya-vardhan-malpeddi/avm-ai-gateaway)`.
2. Click **`README.md`**, then click the **Pencil icon** (Edit file) at the top right[cite: 1].
3. Delete everything currently in the file, paste the block above, and click **Commit changes...**[cite: 1].

```
