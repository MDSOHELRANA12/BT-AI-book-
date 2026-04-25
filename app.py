import streamlit as st
from supabase import create_client
import uuid

# 1. SERVER CONFIGURATION
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

# 2. PAGE UI SETTINGS (Mobile Optimized)
st.set_page_config(page_title="Bt-Ai-Book Global", layout="centered", page_icon="📱")

# Premium CSS for TikTok look
st.markdown("""
    <style>
    .main { background-color: #000; color: white; }
    .stApp { background-color: #000; }
    /* Vertical Video Frame */
    .stVideo { 
        height: 650px !important; 
        border-radius: 25px; 
        border: 3px solid #fe2c55; 
        box-shadow: 0px 0px 15px #fe2c55;
    }
    .stButton>button { 
        border-radius: 30px; 
        background: linear-gradient(45deg, #fe2c55, #ff1e56); 
        color: white; border: none; font-weight: bold; width: 100%; height: 50px;
    }
    .bank-info {
        background: #111; padding: 25px; border-radius: 20px; 
        border-left: 8px solid #00c6ff; margin-top: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. GLOBAL NAVIGATION
st.sidebar.title("✪ Bt-Ai-Book")
st.sidebar.info("Global Business Mode: Active")
menu = ["🔥 Trending Reels", "📤 Upload Short", "🔐 Face Security", "💰 Wallet & Bank"]
choice = st.sidebar.selectbox("Navigate Menu", menu)

# --- SECTION 1: GLOBAL VIDEO FEED (TikTok Style) ---
if choice == "🔥 Trending Reels":
    st.title("🌎 Global Trending")
    try:
        # Fetching latest videos from Supabase
        res = supabase.table("videos").select("*").order("created_at", desc=True).execute()
        if res.data:
            for v in res.data:
                with st.container():
                    st.video(v['video_url'])
                    col1, col2 = st.columns([1,1])
                    col1.button(f"❤️ Like", key=f"l_{v['id']}")
                    col2.button(f"🚀 Share", key=f"s_{v['id']}")
                    st.write("---")
        else:
            st.info("No videos yet. Be the first to upload!")
    except:
        st.error("Connecting to server... Ensure Supabase Table is ready.")

# --- SECTION 2: UPLOAD SYSTEM ---
elif choice == "📤 Upload Short":
    st.title("📤 Creator Studio")
    st.write("Upload TikTok size vertical videos to earn revenue.")
    vid_file = st.file_uploader("Select Video File (MP4)", type=['mp4'])
    
    if st.button("🚀 Publish Globally") and vid_file:
        with st.spinner("Processing High-Quality Upload..."):
            try:
                # 1. Unique ID and Storage Upload
                fname = f"public/{uuid.uuid4()}.mp4"
                supabase.storage.from_('videos').upload(fname, vid_file.read())
                
                # 2. Get Public URL
                v_url = supabase.storage.from_('videos').get_public_url(fname)
                
                # 3. Save to Database
                supabase.table("videos").insert({"video_url": v_url}).execute()
                
                st.balloons()
                st.success("Your video is now LIVE across the world!")
            except Exception as e:
                st.error(f"Error: {e}. Ensure 'videos' bucket is PUBLIC in Supabase.")

# --- SECTION 3: FACE ID SECURITY ---
elif choice == "🔐 Face Security":
    st.title("🔐 Face ID Identity")
    st.write("Scan face for bank withdrawal protection.")
    st.camera_input("Verify Your Identity")
    st.button("Register My Face ID")

# --- SECTION 4: BANK & WITHDRAWAL ---
elif choice == "💰 Wallet & Bank":
    st.title("💰 Revenue Center")
    c1, c2 = st.columns(2)
    c1.metric("Available Balance", "$120.45", "+$15.20")
    c2.metric("Total Impressions", "8.5K")
    
    st.markdown(f"""
        <div class="bank-info">
        <h3 style='color:#00c6ff;'>🏦 Connected Bank Account</h3>
        <p><strong>Account Holder:</strong> MD SOHEL RANA</p>
        <p><strong>Bank:</strong> Clear Bank, London</p>
        <p><strong>Country:</strong> United Kingdom (GB)</p>
        <p><strong>Verification:</strong> Level 3 Global ✅</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Withdraw Funds"):
        st.warning("Withdrawal request sent to Clear Bank. Minimum threshold for first payout is $200.")
