import streamlit as st
from supabase import create_client
import uuid

# 1. SERVER CONNECTION
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

# 2. PAGE SETTINGS
st.set_page_config(page_title="Bt-Ai-Book Global", layout="centered", page_icon="💰")

# 3. PREMIUM UI DESIGN (TikTok Dark Mode)
st.markdown("""
    <style>
    .main { background-color: #000; color: white; }
    .stApp { background-color: #000; }
    .stVideo { height: 600px !important; border-radius: 20px; border: 2px solid #fe2c55; }
    .stButton>button { 
        border-radius: 30px; background: linear-gradient(45deg, #fe2c55, #ff1e56); 
        color: white; border: none; font-weight: bold; width: 100%; height: 50px;
    }
    .bank-card {
        background: #111; padding: 20px; border-radius: 15px; 
        border-left: 6px solid #00c6ff; margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. SIDEBAR NAVIGATION
st.sidebar.title("✪ Bt-Ai-Book")
st.sidebar.write("Global Business Platform")
menu = ["🔥 Global Feed", "📤 Post Reel", "🔐 Face ID Security", "🤖 Bt-Ai Assistant", "💰 Bank & Earnings"]
choice = st.sidebar.selectbox("Navigate Menu", menu)

# --- SECTION 1: GLOBAL VIDEO FEED ---
if choice == "🔥 Global Feed":
    st.title("🌎 Trending Globally")
    try:
        res = supabase.table("videos").select("*").order("created_at", desc=True).execute()
        if res.data:
            for v in res.data:
                st.video(v['video_url'])
                st.button(f"❤️ Like & Support", key=f"l_{v['id']}")
                st.write("---")
        else:
            st.info("Feed is empty. Be the first to post!")
    except:
        st.error("Connecting to server... Please wait.")

# --- SECTION 2: VIDEO UPLOADER ---
elif choice == "📤 Post Reel":
    st.title("📤 Creator Studio")
    st.write("Upload TikTok size vertical videos to earn revenue.")
    vid = st.file_uploader("Choose Video (MP4)", type=['mp4'])
    if st.button("Publish to Global Feed") and vid:
        with st.spinner("Uploading to Global Server..."):
            try:
                fname = f"public/{uuid.uuid4()}.mp4"
                supabase.storage.from_('videos').upload(fname, vid.read())
                v_url = supabase.storage.from_('videos').get_public_url(fname)
                supabase.table("videos").insert({"video_url": v_url}).execute()
                st.balloons()
                st.success("Your video is LIVE now!")
            except Exception as e:
                st.error("Error! Please check if 'videos' bucket is PUBLIC in Supabase.")

# --- SECTION 3: FACE ID SECURITY ---
elif choice == "🔐 Face ID Security":
    st.title("🔐 Face ID Registration")
    st.write("Secure your earnings with face verification.")
    st.camera_input("Scan your face identity")
    st.button("Save Face Data")

# --- SECTION 4: AI ASSISTANT ---
elif choice == "🤖 Bt-Ai Assistant":
    st.title("🤖 Global Smart Bot")
    query = st.chat_input("Ask me anything about your earnings...")
    if query:
        st.chat_message("assistant").write("Bt-Ai is monitoring your global traffic. Your bank account is ready for withdrawal.")

# --- SECTION 5: BANK DETAILS & EARNINGS ---
elif choice == "💰 Bank & Earnings":
    st.title("💰 Revenue Center")
    col1, col2 = st.columns(2)
    col1.metric("Current Balance", "$120.45", "+$15.20")
    col2.metric("Total Views", "8,540")
    
    st.markdown(f"""
        <div class="bank-card">
        <h3>🏦 Verified Bank Account</h3>
        <p><strong>Account Holder:</strong> MD SOHEL RANA</p>
        <p><strong>Bank Name:</strong> Clear Bank</p>
        <p><strong>Location:</strong> London, United Kingdom (GB)</p>
        <p><strong>Status:</strong> Connected ✅</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    if st.button("Withdraw Funds to Bank"):
        st.warning("Minimum withdrawal amount is $200. You are $79.55 away.")
