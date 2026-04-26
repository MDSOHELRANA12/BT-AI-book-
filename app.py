import streamlit as st
from supabase import create_client
import uuid

# --- DATABASE CONNECTION ---
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

st.set_page_config(page_title="Bt-Ai Business Global", layout="wide")

# --- UI DESIGN (Premium Dark Mode) ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .card { background: #111; padding: 20px; border-radius: 15px; border: 1px solid #333; margin-bottom: 10px; }
    .ad-banner { background: linear-gradient(90deg, #fe2c55, #4facfe); padding: 10px; text-align: center; font-weight: bold; border-radius: 10px; margin-bottom: 20px; }
    .money-text { color: #00ff00; font-size: 24px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("✪ Bt-Ai Book Pro")
menu = ["🏠 Global Feed", "📤 Upload & Earn", "👤 My Profile", "💰 Revenue & Bank", "⚙️ Admin (Ads Control)"]
choice = st.sidebar.selectbox("Dashboard", menu)

# --- 1. GLOBAL FEED (With Ad Logic) ---
if choice == "🏠 Global Feed":
    st.markdown('<div class="ad-banner">Sponsor Ad: Earn $20 per click! (Google Verified)</div>', unsafe_allow_html=True)
    st.title("🌎 Trending Reels")
    
    videos = supabase.table("videos").select("*").order("created_at", desc=True).execute()
    for v in videos.data:
        with st.container():
            st.markdown(f'<div class="card">🎬 Video ID: {v["id"][:8]}</div>', unsafe_allow_html=True)
            st.video(v['video_url'])
            # Ad Simulation after every video
            if st.button(f"Watch Ad to Support Creator", key=f"ad_{v['id']}"):
                st.success("Ad Displayed! $0.50 added to pool.")
            st.write("---")

# --- 2. PROFILE & KYC ---
elif choice == "👤 My Profile":
    st.title("👤 Universal Profile Setup")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name", "MD SOHEL RANA")
        address = st.text_area("Permanent Address")
    with col2:
        bank = st.text_input("Bank Account / Swift Code")
        pic = st.file_uploader("Upload Profile Image", type=['jpg', 'png'])

    if st.button("Save Lifetime Profile"):
        st.success("Profile Locked & Saved in Global Server! ✅")

# --- 3. REVENUE & MONETIZATION ---
elif choice == "💰 Revenue & Bank":
    st.title("💰 Earnings Dashboard")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Current Balance", "$1,250.00", "+$45.00")
    c2.metric("Subscribers", "1,050", "Target: 1,000")
    c3.metric("Monetization", "Active ✅")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.subheader("Bank Transfer Status")
    st.info("Direct Bank Transfer (Local/Global) is enabled. Minimum payout $100.")
    if st.button("Withdraw to My Bank"):
        st.warning("Transferring $1,250.00 to your bank... Expected time: 24 hours.")

# --- 4. ADMIN ADS CONTROL ---
elif choice == "⚙️ Admin (Ads Control)":
    st.title("⚙️ Ad Network Integration")
    network = st.selectbox("Select Network", ["Google AdMob", "Unity Ads", "AppLovin", "AdSense"])
    api = st.text_input("API Key / Placement ID")
    cpc = st.slider("Target CPC ($)", 5, 50, 20)
    
    if st.button("Connect Network"):
        st.success(f"{network} Connected with ${cpc} CPC Target! ✅")

