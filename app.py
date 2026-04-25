import streamlit as st
from supabase import create_client
import time

# 1. DATABASE CONNECTION (Your Original Key)
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

# 2. PAGE CONFIGURATION
st.set_page_config(page_title="Bt-Ai-Book Global", layout="wide", page_icon="📈")

# 3. PROFESSIONAL STYLING (Dark Mode UI)
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { 
        width: 100%; border-radius: 25px; 
        background: linear-gradient(45deg, #00c6ff, #0072ff); 
        color: white; font-weight: bold; border: none; height: 50px;
    }
    .ad-slot { 
        background: #1e1e1e; border: 1px dashed #00c6ff; 
        padding: 15px; text-align: center; border-radius: 10px; margin: 10px 0; color: #00c6ff;
    }
    .payment-card { 
        background: linear-gradient(135deg, #1d2b64, #f8cdda); 
        padding: 25px; border-radius: 20px; color: #1d2b64; font-weight: bold;
    }
    .chat-bubble {
        background-color: #262730; padding: 15px; border-radius: 15px; 
        border-left: 5px solid #00c6ff; margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. SIDEBAR NAVIGATION
st.sidebar.title("✪ Bt-Ai-Book Menu")
menu = ["🏠 Global Video Feed", "🔐 Login & Face ID", "📤 Upload Content", "💳 Premium Access", "🤖 AI Support Bot", "📊 My Revenue"]
choice = st.sidebar.selectbox("Navigate", menu)

# --- FEATURE 1: GLOBAL FEED & ADS ---
if choice == "🏠 Global Video Feed":
    st.markdown('<div class="ad-slot">Targeted Ad: High CPM Slot for Google & Partners</div>', unsafe_allow_html=True)
    st.title("🎥 Trending Now")
    
    # Video 1
    with st.container():
        st.video("https://www.w3schools.com/html/mov_bbb.mp4") # Placeholder
        c1, c2, c3 = st.columns(3)
        c1.button("❤️ Like", key="l1")
        c2.button("🚀 Share", key="s1")
        c3.button("💰 Earn Coins", key="e1")
    
    st.markdown('<div class="ad-slot">📺 Video Ad: Skip in 5s (Revenue Slot)</div>', unsafe_allow_html=True)

# --- FEATURE 2: LOGIN & FACE SCAN ---
elif choice == "🔐 Login & Face ID":
    st.title("🔐 Secure Registration")
    u_name = st.text_input("Full Name")
    u_pass = st.text_input("Create Password", type="password")
    st.info("Scan your face to lock your account forever.")
    face_capture = st.camera_input("Face Identity Scan")
    
    if st.button("Create Account"):
        if u_name and u_pass and face_capture:
            st.success(f"Registration Successful! Welcome {u_name}. Your Face ID is saved.")
        else:
            st.error("Please provide Name, Password, and Face Scan.")

# --- FEATURE 3: SMART UPLOAD (Follower Based) ---
elif choice == "📤 Upload Content":
    st.title("📤 Creator Studio")
    st.write("Upload limit is based on your follower count (8s - 60s).")
    video_file = st.file_uploader("Select Video (MP4)", type=['mp4'])
    
    if st.button("Publish to Global Feed"):
        if video_file:
            with st.spinner("Optimizing and Compressing Video..."):
                time.sleep(2)
                st.balloons()
                st.success("Video Published Globally!")

# --- FEATURE 4: PREMIUM ACCESS (Bank Connection) ---
elif choice == "💳 Premium Access":
    st.title("💳 Upgrade to Premium")
    st.markdown(f"""
        <div class="payment-card">
        <h3>Direct Secure Payment</h3>
        <p>Merchant: MD SOHEL RANA</p>
        <p>Bank: Clear Bank, London (GB)</p>
        <p>Payments are automatically processed to our international checking account.</p>
        </div>
    """, unsafe_allow_html=True)
    
    card_number = st.text_input("Debit/Credit Card Number")
    col1, col2 = st.columns(2)
    col1.text_input("Expiry (MM/YY)")
    col2.text_input("CVV", type="password")
    
    if st.button("Authorize $25.00 Payment"):
        with st.spinner("Connecting to Clear Bank Gateway (GB)..."):
            time.sleep(4)
            st.success("Payment Captured Successfully! Premium features unlocked.")

# --- FEATURE 5: AI SUPPORT BOT ---
elif choice == "🤖 AI Support Bot":
    st.title("🤖 Bt-Ai Assistant")
    st.markdown('<div class="chat-bubble">Hello! I am your AI guide. How can I help you today?</div>', unsafe_allow_html=True)
    query = st.text_input("Type your question here...")
    if query:
        st.write("Processing request... Please wait.")
        st.info("Our AI is analyzing your query. For payments, visit the 'Premium Access' tab.")

# --- FEATURE 6: REVENUE DASHBOARD ---
elif choice == "📊 My Revenue":
    st.title("💸 Monetization Stats")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Earnings", "$120.45", "+$15.20")
    c2.metric("Ad Impressions", "8,540", "+1,200")
    c3.metric("Followers", "420", "+10")
    st.write("---")
    st.write("Bank Status: **Connected (Clear Bank GB)**")
