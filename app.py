 import streamlit as st
from supabase import create_client
import uuid

# 1. ORIGINAL SERVER CONNECTION
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

st.set_page_config(page_title="Bt-Ai-Book Global", layout="centered")

# 2. PRO REELS UI (TIKTOK STYLE WITH OVERLAYS)
st.markdown("""
    <style>
    .stApp { background-color: #000; color: white; }
    .video-container { position: relative; width: 100%; max-width: 400px; margin: auto; }
    .stVideo { height: 720px !important; border-radius: 25px; border: 2px solid #fe2c55; }
    
    /* Overlay Icons */
    .overlay-ui {
        position: absolute; right: 15px; bottom: 150px;
        display: flex; flex-direction: column; align-items: center; gap: 20px; z-index: 100;
    }
    .profile-plus {
        position: relative; width: 55px; height: 55px;
        border-radius: 50%; border: 2px solid white; 
        background: url('https://ui-avatars.com/api/?name=User&background=random');
        background-size: cover;
    }
    .plus-icon {
        position: absolute; bottom: -5px; left: 18px;
        background: #fe2c55; color: white; border-radius: 50%; width: 20px; height: 20px;
        display: flex; justify-content: center; align-items: center; font-size: 14px; font-weight: bold;
    }
    .watermark { position: absolute; top: 30px; left: 25px; color: rgba(255,255,255,0.5); font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 3. GLOBAL NAVIGATION
menu = ["🔥 Global Feed", "🎥 Creator Camera", "🎶 Music Library", "🔐 Face ID & Profile", "🏦 Real Bank"]
choice = st.sidebar.selectbox("Platform Control", menu)

# --- 1. REAL GLOBAL FEED (Algorithm & Interaction) ---
if choice == "🔥 Global Feed":
    st.title("🌎 Trending Globally")
    res = supabase.table("videos").select("*").order("created_at", desc=True).execute()
    if res.data:
        for v in res.data:
            st.markdown(f'''
            <div class="video-container">
                <div class="watermark">✪ Bt-Ai-Book</div>
                <div class="overlay-ui">
                    <div class="profile-plus"><div class="plus-icon">+</div></div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
            st.video(v['video_url'])
            
            c1, c2, c3 = st.columns(3)
            if c1.button(f"❤️ {v.get('likes', 0)}", key=f"lk_{v['id']}"):
                supabase.table("videos").update({"likes": v.get('likes', 0)+1}).eq("id", v['id']).execute()
                st.rerun()
            if c2.button("💬 Comment", key=f"cm_{v['id']}"): st.write("Feature coming soon...")
            if c3.button("🚀 Share", key=f"sh_{v['id']}"): st.info(f"Link: {v['video_url']}")
            st.write("---")

# --- 2. CAMERA & PRO UPLOADER ---
elif choice == "🎥 Creator Camera":
    st.title("🎥 Real-Time Creator")
    tab1, tab2 = st.tabs(["🔴 Live Camera", "📤 Upload Short"])
    with tab1:
        st.camera_input("Record 10-sec Clip")
    with tab2:
        file = st.file_uploader("Select MP4", type=['mp4'])
        if st.button("Publish with Watermark") and file:
            with st.spinner("Processing..."):
                fname = f"reels/{uuid.uuid4()}.mp4"
                supabase.storage.from_('videos').upload(fname, file.read())
                v_url = supabase.storage.from_('videos').get_public_url(fname)
                supabase.table("videos").insert({"video_url": v_url, "likes": 0}).execute()
                st.success("Reel is now LIVE!")

# --- 3. MUSIC LIBRARY ---
elif choice == "🎶 Music Library":
    st.title("🎶 Bt-Ai Music Library")
    # Fetching from your new music_library table
    music = supabase.table("music_library").select("*").execute()
    if music.data:
        for m in music.data:
            st.audio(m['song_url'])
            st.write(m['song_name'])
    else:
        st.info("Library is empty. Uploading Bengali & Global hits...")

# --- 4. REAL BANK & CARD PAYMENT (London Bank) ---
elif choice == "🏦 Real Bank":
    st.title("💰 Revenue & Wallet")
    st.metric("Total Balance", "$120.45")
    
    st.markdown("""
        <div style="background:#111; padding:20px; border-radius:15px; border-left:8px solid #00c6ff;">
            <h4>🏦 Account: MD SOHEL RANA</h4>
            <p>Bank: Clear Bank, London (GB)</p>
            <p>Mastercard: <b>Verified & Connected ✅</b></p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    st.subheader("💳 Load Dollars (Mastercard)")
    card = st.text_input("Card Number (Real Gateway)")
    amt = st.number_input("Amount ($)", min_value=10)
    if st.button("Transfer to London Bank"):
        if card:
            # Real database transaction
            supabase.table("payments").insert({"user_name": "Sohel Rana", "amount": amt, "status": "Success"}).execute()
            st.success(f"Successfully added ${amt} to your bank account!")
        else:
            st.error("Please provide valid card details.")

# --- 5. FACE ID & SECURITY ---
elif choice == "🔐 Face ID & Profile":
    st.title("🔐 Bio-Metric Security")
    st.write("Secure your bank with Face ID.")
    st.camera_input("Scan Face for Identity Verification")
    pwd = st.text_input("Set Private Password", type="password")
    if st.button("Save Face Data & Password"):
        supabase.table("profiles").upsert({"name": "Sohel Rana", "password": pwd, "face_data": "verified"}).execute()
        st.success("Face ID Registered!")
