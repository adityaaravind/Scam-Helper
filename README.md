

# 🔊 Deepfake & Voice Scam Detection Helper

👋 **Welcome!**
This project is a simple, beginner-friendly tool that helps you detect **scams**, **phishing messages**, and even **voice deepfakes** in just a few clicks.

---

## 🌟 What This App Does

✅ **Analyzes text or audio messages** for scam clues
🚩 **Flags suspicious words & phrases** (e.g., “urgent,” “transfer funds”)
🤖 **Checks similarity** to known scam patterns
🎨 **Shows color-coded risk scores** (Green = Safe, Red = High Risk)
🛡 **Gives you practical next steps** (verify with official contacts, don’t click links)

---

## 🖼 How It Works (Visual Guide)

| Step | What You Do                                   | What You See                                      |
| ---- | --------------------------------------------- | ------------------------------------------------- |
| 1️⃣  | 📝 Paste a message OR 🎧 upload an audio file | Your input shows in the app                       |
| 2️⃣  | 🔍 Click **Analyze**                          | The tool scans for red flags                      |
| 3️⃣  | 🚩 See warnings + risk score                  | Green 🟢, Yellow 🟡, or Red 🔴 risk badge         |
| 4️⃣  | 📋 Follow recommended actions                 | e.g., "Verify with your CEO," "Don’t click links" |

---

## 🚀 Getting Started (Quick)

### ▶️ Run Locally

1. **Install Python** (3.9+ recommended)
2. **Create a virtual environment** (optional but recommended):

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```
4. **Run the app**:

   ```bash
   streamlit run deepfake_scam_helper.py
   ```
5. Open your browser → go to `http://localhost:8501`

---

### 🌐 Run Online (Streamlit Cloud)

If deployed on Streamlit Cloud, just click the app link and start using — no install needed! 🎉

---

## 🧪 Try These Example Scenarios

| Scenario       | Example Input                                        | What You Learn                         |
| -------------- | ---------------------------------------------------- | -------------------------------------- |
| 💼 CEO Fraud   | “Hello, this is your CEO. Please transfer \$25,000…” | 🚨 High risk – shows finance red flags |
| 🎣 Phishing    | “Your account is locked. Click here to reset…”       | 🕵️ Warns about phishing links         |
| 💸 Crypto Scam | “Send Bitcoin to this wallet to secure your funds…”  | 💰 Flags crypto scam keywords          |
| ✅ Safe Message | “Team, meeting at 10 AM. No action needed.”          | 🟢 No warnings                         |

---

## 🛡️ Why This Matters

Deepfake calls and scam messages are **on the rise**.
Scammers use fear, urgency, and trickery to get you to act fast.
This tool helps you **slow down**, spot the warning signs, and protect yourself.

---

## 🧠 Tech Behind the Scenes

* **Streamlit** for the web interface
* **SpeechRecognition + pydub** for converting audio to text
* **Simple heuristics + fuzzy matching** for scam detection
* **Dynamic risk scoring & tips** to guide users

---

## 🙌 Credits & Disclaimer

Made with ❤️ to help people stay safe online.
⚠️ **Disclaimer:** This tool is for **educational purposes only** — always verify suspicious requests through official channels before acting.

---
