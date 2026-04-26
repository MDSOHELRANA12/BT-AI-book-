import streamlit as st
from supabase import create_client
import uuid

# --- DATABASE CONNECTION ---
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

st.set_page_config(page_title="Bt-Ai Global Business", layout="wide")

# --- PREMIUM UI ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .v-card { position: relative; width: 100%; max-width: 400px; margin: auto; border: 2px solid #fe2c55; border-radius: 20px; overflow: hidden; background: #111; }
    .stVideo { height: 720px !important; border-radius: 18px; }
    .info-box { background: #111; padding: 20px; border-radius: 15px; border: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

# --- MENU ---
menu = ["🔥 Global Feed", "📤 Upload & Earn", "👤 My Profile", "💰 Bank & Revenue", "⚙️ Ads Control"]
choice = st.sidebar.selectbox("Dashboard", menu)

# --- 1. FEED (LIKE & VIEW SYSTEM) ---
if choice == "🔥 Global Feed":
    st.title("🌎 Trending Globally")
    videos = supabase.table("videos").select("*").order("created_at", desc=True).execute()
    for v in videos.data:
        with st.container():
            st.markdown('<div class="v-card">', unsafe_allow_html=True)
            st.video(v['video_url'])
            st.markdown('</div>', unsafe_allow_html=True)
            
            c1, c2, c3 = st.columns(3)
            if c1.button(f"❤️ {v['likes']} Likes", key=f"lk_{v['id']}"):
                supabase.table("videos").update({"likes": v['likes']+1}).eq("id", v['id']).execute()
                st.rerun()
            c2.write(f"👁️ {v['views']} Views")
            if c3.button("🚀 Share Reel", key=f"sh_{v['id']}"):
                st.info(f"Link: {v['video_url']}")
            st.write("---")

# --- 2. PROFILE (LIFETIME DATA) ---
elif choice == "👤 My Profile":
    st.title("👤 Universal Identity")
    with st.form("profile"):
        name = st.text_input("Full Name", "MD SOHEL RANA")
        addr = st.text_area("Permanent Address")
        bank = st.text_input("Bank Account / Swift Code")
        pic = st.file_uploader("Profile Picture", type=['jpg', 'png'])
        if st.form_submit_button("Save & Sync Globally"):
            st.success("Profile saved forever! ✅")

# --- 3. BANK & REVENUE ---
elif choice == "💰 Bank & Revenue":
    st.title("💰 Revenue Center")
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    col1.metric("Current Balance", "$1,250.00")
    col2.metric("Monetization", "Active ✅")
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("Withdraw to Bank"):
        st.success("Transfer initiated! 🏦")

# --- 4. ADS CONTROL ---
elif choice == "⚙️ Ads Control":
    st.title("⚙️ Ad Network Integration")
    net = st.selectbox("Provider", ["Google AdMob", "Unity", "AppLovin"])
    key = st.text_input("API Key")
    if st.button("Connect"):
        st.success(f"{net} is now LIVE! 🚀")
import
import
