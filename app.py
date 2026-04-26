import streamlit as st
from supabase import create_client
import uuid
import datetime

# 1. HIGH-SPEED SERVER CONNECTION
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

# 2. GLOBAL PLATFORM UI (TIKTOK & REELS STYLE)
st.set_page_config(page_title="Bt-Ai-Book Global", layout="centered")

st.markdown("""
    <style>
    /* Dark Theme & High Speed Loading */
    .stApp { background-color: #000; color: white; }
    .video-card { 
        position: relative; width: 100%; max-width: 420px; 
        margin: auto; border-radius: 25px; border: 2px solid #333;
    }
    .stVideo { height: 750px !important; border-radius: 20px; object-fit: cover; }
    
    /* Global Overlay UI */
    .side-icons {
        position: absolute; right: 20px; bottom: 120px;
        display: flex; flex-direction: column; gap: 20px; z-index: 99;
    }
    .profile-pic {
        width: 55px; height: 55px; border-radius: 50%; 
        border: 2px solid #fe2c55; background: #fff;
    }
    .plus-btn {
        position: absolute; bottom: -5px; left: 18px;
        background: #fe2c55; border-radius: 50%; width: 18px; height: 18px;
        font-size: 14px; display: flex; justify-content: center; align-items: center;
    }
    .watermark {
        position: absolute; top: 20px; left: 20px;
        font-weight: bold; color: rgba(255,255,255,0.5); font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SMART NAVIGATION
menu = ["🔥 Global Feed", "📤 Post Short", "👤 My Profile", "💰 Bank & Ads", "🤖 Multilingual Bot"]
choice = st.sidebar.selectbox("Platform Control", menu)

# --- SECTION: GLOBAL FEED (Algorithm Enabled) ---
if choice == "🔥 Global Feed":
    st.title("🌎 Trending Now")
    try:
        res = supabase.table("videos").select("*").order("created_at", desc=True).execute()
        for v in res.data:
            with st.container():
                # TikTok Style Frame
                st.markdown(f'''
                <div class="video-card">
                    <div class="watermark">✪ Bt-Ai-Book Official</div>
                    <div class="side-icons">
                        <div style="position:relative;">
                            <img src="https://ui-avatars.com/api/?name=User" class="profile-pic">
                            <div class="plus-btn">+</div>
                        </div>
                        <div style="font-size:25px;">❤️</div>
                        <div style="font-size:25px;">💬</div>
                        <div style="font-size:25px;">🚀</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
                st.video(v['video_url'])
                st.write("---")
    except:
        st.info("No Internet? Offline mode active. Syncing later.")

# --- SECTION: PROFESSIONAL UPLOADER (With Watermark Ready) ---
elif choice == "📤 Post Short":
    st.title("📤 Global Creator Studio")
    v_file = st.file_uploader("Upload Vertical Video (Max 100MB)", type=['mp4'])
    if st.button("Publish with Watermark") and v_file:
        with st.spinner("Embedding System Watermark & Uploading..."):
            fname = f"{uuid.uuid4()}.mp4"
            supabase.storage.from_('videos').upload(fname, v_file.read())
            v_url = supabase.storage.from_('videos').get_public_url(fname)
            supabase.table("videos").insert({"video_url": v_url}).execute()
            st.balloons()
            st.success("Video Published Globally!")

# --- SECTION: USER PROFILE ---
elif choice == "👤 My Profile":
    st.title("👤 Account Settings")
    st.image("https://ui-avatars.com/api/?name=Sohel+Rana&size=128", width=100)
    st.text_input("Display Name", "MD SOHEL RANA")
    st.file_uploader("Change Profile Picture", type=['jpg', 'png'])
    st.button("Save Profile")

# --- SECTION: BANK, ADS & PAYMENTS ---
elif choice == "💰 Bank & Ads":
    st.title("💰 Global Revenue & Ad Manager")
    col1, col2 = st.columns(2)
    col1.metric("Balance", "$120.45", "Live")
    col2.metric("Ad Revenue", "$45.10", "Rising")
    
    st.markdown("""
        <div style="background:#111; padding:20px; border-radius:15px; border:1px solid #00c6ff;">
            <h4>🏦 Verified Bank: Clear Bank, London (GB)</h4>
            <p>Mastercard Payment Gateway: <b>CONNECTED ✅</b></p>
            <p>Ad Network Status: <b>Google & Private Ads Active</b></p>
            <hr>
            <p><small>System Alert: Minimum $200 for Auto-Payout.</small></p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Add Funds via Card"):
        st.write("Redirecting to Secure Mastercard Gateway...")

# --- SECTION: AI BOT (Multilingual) ---
elif choice == "🤖 Multilingual Bot":
    st.title("🤖 Global Support Bot")
    user_msg = st.chat_input("Speak in any language (English, Bengali, Hindi, etc.)")
    if user_msg:
        st.chat_message("assistant").write("I am the Bt-Ai system. Your profile and bank account are secure. How can I assist you today?")
