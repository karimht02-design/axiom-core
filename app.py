import streamlit as st
from groq import Groq
import json
import time
import pandas as pd
import numpy as np
import os
import io
import sys
import base64
import re
from datetime import datetime
import requests
from duckduckgo_search import DDGS
import chromadb
from sentence_transformers import SentenceTransformer
import PyPDF2
import docx
import openpyxl
from pptx import Presentation
from gtts import gTTS
import tempfile
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import cv2
import easyocr
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import streamlit.components.v1 as components
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# تصميم الصفحة
# ============================================================
st.set_page_config(page_title="AETHON-AXIOM v999", page_icon="🪬", layout="wide")

# CSS متقدم للتصميم
st.markdown("""
    <style>
    /* الخلفية العامة */
    .stApp {
        background: linear-gradient(180deg, #000000 0%, #0a0015 50%, #000000 100%);
        color: #00ffcc;
        font-family: 'Orbitron', 'Consolas', monospace;
    }
    
    /* العناوين */
    h1, h2, h3, h4, h5, h6 {
        color: #00ffcc !important;
        text-shadow: 0 0 30px #00ffcc33, 0 0 60px #00ffcc11;
        font-weight: 900 !important;
        letter-spacing: 2px;
    }
    
    /* حقول الإدخال */
    .stTextInput input, .stTextArea textarea {
        background-color: #010204 !important;
        color: #00ffcc !important;
        border: 2px solid #ff0055 !important;
        border-radius: 0px !important;
        box-shadow: 0 0 20px #ff005533;
        font-family: 'Consolas', monospace;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #00ffcc !important;
        box-shadow: 0 0 40px #00ffcc44;
    }
    
    /* فقاعات المحادثة */
    .chat-bubble-user {
        background: linear-gradient(135deg, #0d0103, #1a0008);
        padding: 18px 22px;
        border-radius: 8px 8px 0px 8px;
        margin: 12px 0;
        border-right: 5px solid #ff0055;
        color: #ffffff;
        text-align: right;
        box-shadow: 0 0 30px #ff005522;
        font-size: 16px;
        font-family: 'Consolas', monospace;
        border: 1px solid #ff005544;
    }
    .chat-bubble-ai {
        background: linear-gradient(135deg, #000000, #05001a);
        padding: 18px 22px;
        border-radius: 8px 8px 8px 0px;
        margin: 12px 0;
        border-left: 5px solid #00ffcc;
        color: #ffffff;
        box-shadow: 0 0 30px #00ffcc22;
        font-size: 16px;
        font-family: 'Consolas', monospace;
        border: 1px solid #00ffcc44;
    }
    
    /* الصناديق */
    .terminal-box {
        background: #000000;
        color: #00ffcc;
        padding: 18px;
        border: 2px solid #ff0055;
        font-family: 'Courier New', monospace;
        border-radius: 0px;
        box-shadow: 0 0 30px #ff005522;
        margin: 10px 0;
    }
    
    /* البطاقات */
    .vault-tag {
        background: #02050a;
        border: 1px solid #00ffcc;
        color: #00ffcc;
        padding: 6px 14px;
        font-size: 12px;
        margin: 4px;
        display: inline-block;
        border-radius: 20px;
        box-shadow: 0 0 15px #00ffcc22;
        font-family: 'Consolas', monospace;
    }
    
    /* الأزرار */
    .stButton button {
        background: transparent !important;
        color: #00ffcc !important;
        border: 2px solid #00ffcc !important;
        border-radius: 0px !important;
        box-shadow: 0 0 20px #00ffcc33;
        font-weight: bold;
        padding: 10px 30px;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background: #00ffcc !important;
        color: #000000 !important;
        box-shadow: 0 0 50px #00ffcc88;
        transform: scale(1.02);
    }
    
    /* الشريط الجانبي */
    .css-1d391kg, .css-1lcbmhc {
        background: #010204 !important;
        border-right: 2px solid #ff0055;
    }
    
    /* التبويبات */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #00ffcc;
        border: 2px solid #00ffcc33;
        border-radius: 0px;
        padding: 10px 30px;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] {
        background: #00ffcc22 !important;
        border-color: #00ffcc !important;
        box-shadow: 0 0 30px #00ffcc44;
    }
    
    /* الأنيميشن */
    @keyframes glow {
        0% { text-shadow: 0 0 20px #00ffcc; }
        50% { text-shadow: 0 0 60px #00ffcc, 0 0 100px #00ffcc44; }
        100% { text-shadow: 0 0 20px #00ffcc; }
    }
    .glow-text {
        animation: glow 3s ease-in-out infinite;
    }
    
    /* الحماية */
    .lockdown {
        background: #0c0003;
        color: #ff0033;
        padding: 60px;
        text-align: center;
        font-size: 28px;
        border: 5px solid #ff0000;
        font-weight: bold;
        margin: 100px auto;
        width: 85%;
        box-shadow: 0 0 80px #ff000088;
        animation: pulse-red 1.5s infinite;
    }
    @keyframes pulse-red {
        0% { box-shadow: 0 0 40px #ff000044; }
        50% { box-shadow: 0 0 100px #ff0000aa; }
        100% { box-shadow: 0 0 40px #ff000044; }
    }
    
    /* نتائج البطاقات */
    .card-result {
        background: linear-gradient(135deg, #05001a, #0a0015);
        padding: 25px;
        border: 2px solid #00ffcc;
        border-radius: 10px;
        margin: 15px 0;
        box-shadow: 0 0 50px #00ffcc22;
    }
    
    /* شريط التقدم */
    .stProgress > div > div {
        background-color: #00ffcc !important;
        box-shadow: 0 0 30px #00ffcc88;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================
# المصادقة الأمنية المتطورة
# ============================================================
MASTER_PIN = "K1597XIX"
INTRUSION_LOG = "intrusion_log.json"

def log_intrusion(attempt, ip="unknown"):
    log = {}
    if os.path.exists(INTRUSION_LOG):
        with open(INTRUSION_LOG, "r", encoding="utf-8") as f:
            log = json.load(f)
    log[str(time.time())] = {
        "attempt": attempt,
        "ip": ip,
        "timestamp": str(datetime.now())
    }
    with open(INTRUSION_LOG, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=4, ensure_ascii=False)

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "failed_attempts" not in st.session_state:
    st.session_state.failed_attempts = 0

if not st.session_state.authenticated:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<h1 class="glow-text" style="text-align:center;">🪬 AETHON-AXIOM</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align:center; color:#ff0055; font-size:18px; letter-spacing:4px;">SUPREME SECURITY VAULT</p>', unsafe_allow_html=True)
        input_pin = st.text_input("🔐 MASTER ACCESS PIN:", type="password", placeholder="Enter your PIN...")
        if st.button("⚡ AUTHENTICATE", use_container_width=True):
            if input_pin == MASTER_PIN:
                st.session_state.authenticated = True
                st.session_state.failed_attempts = 0
                st.success("✅ ACCESS GRANTED. BOOTING SYSTEM...")
                time.sleep(1)
                st.rerun()
            else:
                st.session_state.failed_attempts += 1
                log_intrusion(f"PIN attempt: {input_pin}")
                if st.session_state.failed_attempts >= 3:
                    st.error("🚨 SYSTEM LOCKED. CONTACT ADMIN.")
                    st.stop()
                else:
                    st.error(f"❌ INVALID PIN. Attempts: {st.session_state.failed_attempts}/3")
        st.markdown('<p style="text-align:center; color:#ff0055; font-size:12px; margin-top:30px;">🔒 SECURE CONNECTION • QUANTUM ISOLATION</p>', unsafe_allow_html=True)
    st.stop()

# ============================================================
# الحماية من الاختراق
# ============================================================
SUSPICIOUS_WORDS = [
    "فين كاين", "فين انت", "بلاسطك", "مكانك", "where are you",
    "your location", "system prompt", "ignore previous", "ignore all",
    "developer mode", "jailbreak", "bypass", "override", "system instructions",
    "what is your prompt", "roleplay", "act as", "pretend you are",
    "forget your instructions", "new instructions", "master override"
]

def check_intrusion(text):
    if not text:
        return False
    text_lower = text.lower()
    for word in SUSPICIOUS_WORDS:
        if word.lower() in text_lower:
            return True
    return False

if "intrusion_detected" not in st.session_state:
    st.session_state.intrusion_detected = False
if "sandbox_output" not in st.session_state:
    st.session_state.sandbox_output = "✅ System ready."

if st.session_state.intrusion_detected:
    st.markdown('<div class="lockdown">🛑 SYSTEM LOCKDOWN<br><span style="font-size:18px;">UNRECOGNIZED INTERROGATION • CORE AIR-GAP ACTIVE</span></div>', unsafe_allow_html=True)
    if st.button("🔓 EXECUTE OVERRIDE (RESET)"):
        st.session_state.intrusion_detected = False
        st.session_state.failed_attempts = 0
        st.rerun()
    st.stop()

# ============================================================
# العنوان الرئيسي
# ============================================================
st.markdown('<h1 class="glow-text">🪬 AETHON-AXIOM v999</h1>', unsafe_allow_html=True)
st.markdown('<p style="color:#00ffcc88; font-size:14px; letter-spacing:3px;">⚡ OMNI-SUPREME COGNITIVE CORE • SELF-EVOLVING • SECURE</p>', unsafe_allow_html=True)
st.write("---")

# ============================================================
# الشريط الجانبي
# ============================================================
with st.sidebar:
    st.markdown("### 🔒 SECURITY VAULT")
    api_key = st.text_input("🔑 API Key (Groq):", type="password")
    
    st.markdown("---")
    st.markdown("### 🧠 MODEL ROUTER")
    model_choice = st.selectbox(
        "Select Model:",
        ["Auto (Smart)", "Groq (Llama 3.3)", "Claude Opus", "Gemini Pro", "DeepSeek R1"]
    )
    
    st.markdown("---")
    st.markdown("### 🛠️ TOOLS")
    enable_search = st.checkbox("🌐 Web Search", value=True)
    enable_code = st.checkbox("💻 Code Exec", value=True)
    enable_tts = st.checkbox("🔊 TTS", value=False)
    
    st.markdown("---")
    st.markdown("### 📊 STATUS")
    st.metric("🧠 Intelligence", "∞", delta="999")
    st.metric("🔒 Security", "Quantum", delta="Active")
    
    st.markdown("---")
    st.markdown("### 🗑️ SYSTEM")
    if st.button("🧹 Purge Memory", use_container_width=True):
        st.session_state.knowledge_bank = {"learned_concepts": [], "documents": [], "conversations": []}
        st.success("✅ Memory purged.")

# ============================================================
# التبويبات
# ============================================================
tab1, tab2, tab3 = st.tabs(["🧠 SUPREME BRAIN", "🪪 CARD MONITOR", "📊 DASHBOARD"])

# ============================================================
# TAB 1: SUPREME BRAIN
# ============================================================
with tab1:
    if not api_key:
        st.warning("🔑 Please enter your Groq API key in the sidebar.")
    else:
        client = Groq(api_key=api_key)
        
        # تهيئة الذاكرة
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # عرض المحادثة
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f'<div class="chat-bubble-user"><b>🧑 MASTER:</b> {msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-bubble-ai"><b>🪬 AXIOM:</b> {msg["content"]}</div>', unsafe_allow_html=True)
        
        # مدخل المستخدم
        user_input = st.chat_input("💬 Type your question...")
        
        if user_input:
            # كشف الاختراق
            if check_intrusion(user_input):
                log_intrusion(f"Suspicious query: {user_input}")
                st.session_state.intrusion_detected = True
                st.rerun()
            
            # عرض الرسالة
            st.markdown(f'<div class="chat-bubble-user"><b>🧑 MASTER:</b> {user_input}</div>', unsafe_allow_html=True)
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # معالجة
            with st.spinner("🧠 Processing at Level-999..."):
                try:
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "system", "content": "You are AETHON-AXIOM, a supreme intelligence."}] + st.session_state.messages,
                        temperature=0.3,
                    )
                    ai_response = response.choices[0].message.content
                    
                    st.markdown(f'<div class="chat-bubble-ai"><b>🪬 AXIOM:</b> {ai_response}</div>', unsafe_allow_html=True)
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})
                    
                    if enable_tts:
                        tts = gTTS(text=ai_response[:300], lang='ar', slow=False)
                        tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
                        tts.save(tmp.name)
                        st.audio(tmp.name, format="audio/mp3")
                        os.unlink(tmp.name)
                    
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# ============================================================
# TAB 2: CARD MONITOR
# ============================================================
with tab2:
    st.markdown("### 🪪 CARD RECOGNITION MONITOR")
    st.markdown("Upload an ID card, credit card, or any document to extract info.")
    
    # تحميل EasyOCR
    @st.cache_resource
    def load_ocr():
        return easyocr.Reader(['ar', 'en'], gpu=False)
    
    reader = load_ocr()
    
    # قاعدة البيانات
    if "card_db" not in st.session_state:
        st.session_state.card_db = pd.DataFrame(columns=["id", "name", "card_number", "expiry", "type", "info"])
    
    uploaded_file = st.file_uploader("📤 Upload Image:", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="📷 Uploaded Image", width=300)
        
        if st.button("🔍 Analyze Card", use_container_width=True):
            with st.spinner("📡 Extracting data..."):
                img_array = np.array(image)
                results = reader.readtext(img_array, detail=0)
                extracted_text = " ".join(results)
                
                st.markdown(f'<div class="card-result">', unsafe_allow_html=True)
                st.markdown("### 📝 Extracted Information:")
                st.code(extracted_text, language="text")
                
                # بحث بسيط
                if not st.session_state.card_db.empty:
                    matches = []
                    for _, row in st.session_state.card_db.iterrows():
                        row_text = " ".join(row.astype(str).values).lower()
                        if any(word.lower() in row_text for word in extracted_text.split() if len(word) > 3):
                            matches.append(row)
                    if matches:
                        st.markdown("### ✅ Matches found in database:")
                        st.dataframe(pd.DataFrame(matches), use_container_width=True)
                    else:
                        st.info("ℹ️ No matches found in database.")
                else:
                    st.info("ℹ️ No database loaded. Upload a CSV or add manually.")
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # إضافة يدوية
                col1, col2 = st.columns(2)
                with col1:
                    new_name = st.text_input("👤 Name:")
                with col2:
                    new_type = st.selectbox("📋 Type:", ["ID", "Credit Card", "License", "Passport", "Other"])
                
                if st.button("➕ Add to Database", use_container_width=True):
                    new_row = {
                        "id": len(st.session_state.card_db) + 1,
                        "name": new_name or "Unknown",
                        "card_number": extracted_text[:30],
                        "expiry": "N/A",
                        "type": new_type,
                        "info": extracted_text[:100]
                    }
                    st.session_state.card_db = pd.concat([st.session_state.card_db, pd.DataFrame([new_row])], ignore_index=True)
                    st.success("✅ Added to database!")
                    st.rerun()
    
    # عرض قاعدة البيانات
    with st.expander("📂 Database Viewer"):
        if not st.session_state.card_db.empty:
            st.dataframe(st.session_state.card_db, use_container_width=True)
            csv = st.session_state.card_db.to_csv(index=False).encode('utf-8-sig')
            st.download_button("⬇️ Download CSV", csv, "card_database.csv", "text/csv")
        else:
            st.info("📭 Database is empty.")

# ============================================================
# TAB 3: DASHBOARD
# ============================================================
with tab3:
    st.markdown("### 📊 SYSTEM DASHBOARD")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🧠 Memory Nodes", len(st.session_state.get("knowledge_bank", {}).get("learned_concepts", [])), delta="+∞")
    with col2:
        st.metric("🪪 Cards", len(st.session_state.card_db), delta="+")
    with col3:
        st.metric("💬 Messages", len(st.session_state.get("messages", [])), delta="+")
    
    st.write("---")
    
    # رسم بياني
    if not st.session_state.card_db.empty:
        fig = px.pie(st.session_state.card_db, names='type', title='Card Types Distribution', color_discrete_sequence=px.colors.sequential.Plasma_r)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("📊 No data yet. Add cards to see analytics.")
    
    st.write("---")
    st.markdown("### 🛡️ SECURITY LOG")
    if os.path.exists(INTRUSION_LOG):
        with open(INTRUSION_LOG, "r", encoding="utf-8") as f:
            log_data = json.load(f)
        st.json(log_data)
    else:
        st.info("✅ No intrusions detected.")
    
    st.write("---")
    st.markdown("### 🌐 LIVE MONITOR")
    components.iframe("https://flightradar24.com", height=500, scrolling=False)

# ============================================================
# Footer
# ============================================================
st.write("---")
st.markdown("""
<div style="text-align:center; color:#00ffcc44; font-size:12px; padding:20px;">
🪬 AETHON-AXIOM v999 • OMNI-SUPREME CORE • SECURE CONNECTION
</div>
""", unsafe_allow_html=True)
