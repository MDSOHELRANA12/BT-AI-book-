import streamlit as st
from supabase import create_client
import datetime
import uuid

# 1. DATABASE CONNECTION
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

# 2. PAGE CONFIGURATION
st.set_page_config(page_title="Bt-Ai-Book Global", layout="centered", page_icon="📱")

# 3. VERTICAL VIDEO STYLING (TikTok Style)
st.markdown("""
    <style>
    .main { background-color: #000000; color: white; }
    .stApp { background-color: #000000; }
    /* TikTok Frame Style */
    .video-container { 
        width: 100%; 
        max-width: 400px; 
        margin: auto; 
        border-radius: 20px; 
        overflow: hidden; 
        border: 2px solid #333;
        background: #111;
    }
    .stVideo {
        width: 100% !important;
        height: 650px !important; /* TikTok Vertical Height */
        object-fit: cover;
    }
    .stButton>button { 
        border-radius: 25px; background: linear-gradient(45deg, #fe2c55, #ff1e56); 
        color: white; border: none; font-weight: bold; width: 100%;
    }
    .sidebar .sidebar-content { background: #111; }
    </style>
    """, unsafe_allow_html=True)

# 4. NAVIGATION
st.sidebar.title("✪ Bt-Ai-Book")
menu = ["🔥 Trending Reels", "🔐 Security Vault", "📤 Post Short", "🤖 AI Support", "💰 Revenue"]
choice = st.sidebar.selectbox("Go to", menu)

# --- FEATURE 1: VERTICAL FEED (TikTok Size) ---
if choice == "🔥 Trending Reels":
    st.title("🌎 Global Shorts")
    
    try:
        response = supabase.table("videos").select("*").order("created_at", desc=True).execute()
        videos = response.data
        
        if videos:
            for v in videos:
                with st.container():
                    st.markdown('<div class="video-container">', unsafe_allow_html=True)
                    st.video(v['video_url']) # This will now show as vertical
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Social Buttons below the video
                    col1, col2, col3 = st.columns([1,1,1])
                    col1.button("❤️", key=f"lk_{v['id']}")
                    col2.button("🚀", key=f"sh_{v['id']}")
                    col3.button("💰", key=f"earn_{v['id']}")
                    st.write("---")
        else:
            st.info("No shorts uploaded yet.")
    except Exception as e:
        st.error("Server connecting... Please wait.")

# --- FEATURE 2: POSTING NEW SHORTS ---
elif choice == "📤 Post Short":
    st.title("📤 Upload TikTok Size Video")
    st.write("Please upload vertical videos (9:16 ratio) for the best look.")
    
    video_file = st.file_uploader("Select MP4 Video", type=['mp4'])
    
    if st.button("Publish Reel"):
        if video_file:
            with st.spinner("Uploading to Global Server..."):
                file_name = f"{uuid.uuid4()}.mp4"
                storage_res = supabase.storage.from_('videos').upload(f"public/{file_name}", video_file.read())
                video_url = f"{URL}/storage/v1/object/public/videos/public/{file_name}"
                supabase.table("videos").insert({"video_url": video_url}).execute()
                
                st.balloons()
                st.success("Your Short Video is now LIVE!")

# --- FEATURE 3: AI ASSISTANT ---
elif choice == "🤖 AI Support":
    st.title("🤖 Assistant")
    user_query = st.chat_input("How can I help you?")
    if user_query:
        st.chat_message("assistant").write("The Bt-Ai system is optimized for TikTok-style vertical videos. Your bank account is ready for earnings.")

# --- FEATURE 4: WALLET ---
elif choice == "💰 Revenue":
    st.title("💰 Earnings")
    st.metric("Balance", "$120.45")
    st.info("Bank: Clear Bank, London (GB) Connected")
    st.button("Request Payout")
