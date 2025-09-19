import streamlit as st
import re
import difflib
import tempfile
import os
try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except ModuleNotFoundError:
    SR_AVAILABLE = False

st.set_page_config(page_title="Deepfake / Voice Scam Detection Helper", page_icon="🔊", layout="wide")

st.title("🔊 Deepfake / Voice Scam Detection Helper")

st.markdown("""
## 🧐 What This App Does
This tool helps **anyone** quickly spot possible scams or impersonation attempts.
""")

colA, colB, colC, colD = st.columns(4)
with colA:
    st.markdown("### 1️⃣ Input\n📝 Paste message or 🎧 upload voice clip")
with colB:
    st.markdown("### 2️⃣ Analyze\n🔍 The app scans for ⚠️ red flags & suspicious keywords")
with colC:
    st.markdown("### 3️⃣ Results\n🚩 Flags + 🤖 similarity to known scams")
with colD:
    st.markdown("### 4️⃣ Next Steps\n📋 Safe tips & ✅ verify before acting")

st.markdown("> 💡 **Why it matters:** Deepfake calls and AI-generated scams are growing threats. This app shows you **exactly** what looks risky so you can pause and confirm.")

def detect_impersonation_clues(text: str):
    warnings = []
    text_lower = text.lower()

    suspicious_keywords = [
        ("urgent", "Urgent language often creates pressure to act fast.", "general"),
        ("transfer", "Requests for transfers can indicate payment fraud.", "finance"),
        ("wire", "Wire transfers are common in business email compromise scams.", "finance"),
        ("password", "Asking for passwords is a phishing red flag.", "phishing"),
        ("account locked", "Fake account lockouts are used to scare users.", "phishing"),
        ("gift cards", "Gift card scams are common – asking you to buy cards.", "finance"),
        ("crypto", "Crypto is hard to trace and is used by scammers.", "finance"),
        ("bitcoin", "Bitcoin requests often indicate scams.", "finance"),
        ("bank details", "Scammers may ask for bank details for fraud.", "finance"),
        ("social security", "Never share SSNs in chat – ID theft risk.", "pii"),
        ("confidential", "Emphasizing secrecy is a manipulation tactic.", "general"),
        ("secret", "Secrecy requests may be social engineering.", "general"),
        ("verification", "Fake verification links steal credentials.", "phishing"),
        ("reset", "Password reset prompts may be phishing.", "phishing"),
        ("immediately", "Urgency tries to bypass critical thinking.", "general")
    ]

    for kw, explanation, category in suspicious_keywords:
        if kw in text_lower:
            icon = "💰" if category == "finance" else "🕵️" if category == "phishing" else "🔒" if category == "pii" else "⚠️"
            warnings.append((f"{icon} Contains suspicious keyword: '{kw}'", explanation, category))

    if re.search(r"(?i)click\s+here|verify\s+now|act\s+fast", text):
        warnings.append(("🕵️ Contains call-to-action phrases common in scams", "Links like 'click here' can lead to phishing sites.", "phishing"))

    if len(text.split()) < 10:
        warnings.append(("⚠️ Very short message – could be AI-generated or phishing", "Scam messages can be unusually brief.", "general"))

    if re.search(r"(?i)boss|ceo|manager|director|hr", text):
        warnings.append(("⚠️ Mentions authority figures – watch for impersonation", "Attackers impersonate bosses to force quick action.", "general"))

    return warnings

def similarity_to_known_phrases(text: str, known_phrases):
    matches = []
    for phrase in known_phrases:
        ratio = difflib.SequenceMatcher(None, text.lower(), phrase.lower()).ratio()
        if ratio > 0.6:
            matches.append((phrase, round(ratio, 2)))
    return matches

def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio_data = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            return ""

def calculate_risk_score(warnings, matches):
    score = len(warnings) * 20 + len(matches) * 15
    return min(score, 100)

def display_risk_badge(score):
    st.progress(score / 100)
    if score == 0:
        st.success(f"🟢 Risk Score: {score}/100 — Looks Safe")
    elif score <= 50:
        st.warning(f"🟡 Risk Score: {score}/100 — Be Cautious")
    else:
        st.error(f"🔴 Risk Score: {score}/100 — High Risk")

def show_dynamic_recommendations(categories):
    st.subheader("🛡️ Recommended Next Steps")
    priority_order = ["finance", "phishing", "pii", "general"]
    sorted_categories = [cat for cat in priority_order if cat in categories]

    for i, cat in enumerate(sorted_categories):
        prefix = "🔥" if i == 0 else "➡️"
        if cat == "finance":
            st.markdown(f"{prefix} 💰 **Double-check financial requests** through official channels before transferring money.")
        elif cat == "phishing":
            st.markdown(f"{prefix} 🕵️ **Avoid clicking links** or entering credentials until verified.")
        elif cat == "pii":
            st.markdown(f"{prefix} 🔒 **Never share personal data** (SSN, bank info, passwords) over untrusted messages.")
        elif cat == "general":
            st.markdown(f"{prefix} ⚠️ **Verify requests** by calling back on a known number and report to IT/security.")

    if not categories:
        st.markdown("✅ No specific actions needed, but stay vigilant.")

st.markdown("### 🎯 Try an Example")
examples = {
    "CEO Fraud": "Hello, this is your CEO. Please transfer $25,000 to a new vendor immediately. Do not tell anyone until this is done.",
    "Phishing Link": "We detected a problem with your account. Click here to verify and reset your password.",
    "Crypto Scam": "Urgent: Your crypto wallet is compromised. Send Bitcoin to this address to secure your funds.",
    "Safe Message": "Team, reminder that our all-hands is tomorrow at 10 AM. No action needed."
}
selected_example = st.radio("Select an example to auto-fill:", list(examples.keys()), horizontal=True)

example_text = examples[selected_example]
st.info("💡 **Tip:** You can edit the example or paste your own text before analyzing.")

tab1, tab2 = st.tabs(["📝 Text Analysis", "🎙️ Voice Analysis"])

with tab1:
    text_input = st.text_area("Enter transcript or message:", example_text, height=200)
    if st.button("🔍 Analyze Text"):
        if not text_input.strip():
            st.warning("⚠️ Please enter some text.")
        else:
            warnings = detect_impersonation_clues(text_input)
            matches = similarity_to_known_phrases(text_input, [
                "This is urgent, wire funds now",
                "We have locked your account, click here to reset",
                "Please purchase gift cards and send the codes"
            ])
            risk_score = calculate_risk_score(warnings, matches)
            display_risk_badge(risk_score)

            categories = set([c for _, _, c in warnings])

            st.subheader("🚩 Potential Warning Flags")
            if warnings:
                for w, explanation, _ in warnings:
                    with st.expander(w):
                        st.write(f"ℹ️ {explanation}")
            else:
                st.success("✅ No obvious red flags detected.")

            st.subheader("🤖 Similarity to Known Scam Phrases")
            if matches:
                for phrase, score in matches:
                    st.warning(f"🔎 Similar to: '{phrase}' (similarity: {score})")
            else:
                st.info("ℹ️ No strong similarity to known scam phrases.")

            show_dynamic_recommendations(categories)

with tab2:
    if not SR_AVAILABLE:
        st.error("🎧 Audio analysis is unavailable. Install `SpeechRecognition` to enable this feature.")
    else:
        uploaded_file = st.file_uploader("🎧 Upload audio file (wav/mp3)", type=["wav", "mp3"])
        if st.button("🔊 Analyze Audio"):
           if uploaded_file is None:
                st.warning("⚠️ Please upload an audio file.")
            else:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                    tmp.write(uploaded_file.read())
                    temp_path = tmp.name

            if transcript:
                warnings = detect_impersonation_clues(transcript)
                matches = similarity_to_known_phrases(transcript, [
                    "This is urgent, wire funds now",
                    "We have locked your account, click here to reset",
                    "Please purchase gift cards and send the codes"
                ])
                risk_score = calculate_risk_score(warnings, matches)
                display_risk_badge(risk_score)

                categories = set([c for _, _, c in warnings])

                st.write("**📝 Transcript:**", transcript)
                st.subheader("🚩 Potential Warning Flags")
                if warnings:
                    for w, explanation, _ in warnings:
                        with st.expander(w):
                            st.write(f"ℹ️ {explanation}")
                else:
                    st.success("✅ No obvious red flags detected.")

                st.subheader("🤖 Similarity to Known Scam Phrases")
                if matches:
                    for phrase, score in matches:
                        st.warning(f"🔎 Similar to: '{phrase}' (similarity: {score})")
                else:
                    st.info("ℹ️ No strong similarity to known scam phrases.")

                show_dynamic_recommendations(categories)
            else:
                st.error("❌ Could not transcribe audio. Please try again with clearer audio.")

st.markdown("---")
st.caption("📢 **Reminder:** This is an educational tool. Always verify suspicious requests through official contacts before taking action.")
