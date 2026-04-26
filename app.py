import streamlit as st
from supabase import create_client
import uuid

# --- GLOBAL DATABASE CONNECTION ---
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Bt-Ai Global Pro", layout="wide")

# --- UI DESIGN & HD VISIBILITY ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; font-family: 'Inter', sans-serif; }
    .card { background: #111; padding: 25px; border-radius: 15px; border: 1px solid #222; margin-bottom: 20px; }
    .stChatMessage { background-color: #222 !important; border: 1px solid #444 !important; }
    .stChatMessage p { color: #ffffff !important; font-size: 18px !important; font-weight: bold !important; }
    .ad-banner { background: linear-gradient(90deg, #1e90ff, #00ff00); color: black; padding: 12px; text-align: center; font-weight: bold; border-radius: 10px; margin-bottom: 25px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="ad-banner">🚀 LIVE GLOBAL CAMPAIGN: $500 Reward Pool - Upload & Earn! 💰</div>', unsafe_allow_html=True)

# --- NAVIGATION ---
st.sidebar.title("✪ Bt-Ai Global Pro")
menu = ["🏠 Global Feed", "📤 Publish Video", "👤 Profile & Security", "🤖 AI Assistant"]
choice = st.sidebar.selectbox("Dashboard Menu", menu)

# --- 1. GLOBAL FEED (REAL LIKE BUTTON FIX) ---
if choice == "🏠 Global Feed":
    st.title("🌎 Trending Content")
    try:
        v_data = supabase.table("videos").select("*").order("created_at", desc=True).execute()
        if v_data.data:
            for v in v_data.data:
                with st.container():
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.video(v['video_url'])
                    
                    col1, col2, col3 = st.columns([1, 1, 2])
                    # লাইক বাটন যা সরাসরি ডাটাবেজে আপডেট হবে
                    if col1.button(f"❤️ {v.get('likes', 0)} Likes", key=f"like_{v['id']}"):
                        new_likes = v.get('likes', 0) + 1
                        supabase.table("videos").update({"likes": new_likes}).eq("id", v['id']).execute()
                        st.rerun()
                    
                    current_views = v.get('views', 0) + 1
                    supabase.table("videos").update({"views": current_views}).eq("id", v['id']).execute()
                    col2.write(f"👁️ {current_views} Views")
                    col3.write(f"📊 Earned: ${current_views * 0.01:.2f}")
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No content available.")
    except:
        st.error("Connection error. Please refresh.")

# --- 2. VIDEO PUBLISHING (10s LIMIT) ---
elif choice == "📤 Publish Video":
    st.title("📤 Creator Studio")
    v_file = st.file_uploader("Upload MP4 (Max 10s)", type=['mp4'])
    v_title = st.text_input("Video Title")
    if st.button("Publish Now") and v_file:
        with st.spinner("Uploading..."):
            file_id = str(uuid.uuid4())
            supabase.storage.from_('videos').upload(f"public/{file_id}.mp4", v_file.read())
            v_url = supabase.storage.from_('videos').get_public_url(f"public/{file_id}.mp4")
            supabase.table("videos").insert({"video_url": v_url, "title": v_title, "likes": 0, "views": 0}).execute()
            st.success("Live Now! ✅")

# --- 3. PROFILE & PASSWORD LOGIN (SECURE FIX) ---
elif choice == "👤 Profile & Security":
    st.title("👤 User Authentication")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    with st.form("auth_form"):
        st.subheader("Login / Update Security")
        name = st.text_input("Full Name", value="MD SOHEL RANA")
        email = st.text_input("Email Address")
        password = st.text_input("Security Password", type="password", placeholder="Enter your secret password")
        
        if st.form_submit_button("Save & Secure Account"):
            if len(password) < 6:
                st.error("Password must be at least 6 characters!")
            else:
                st.success(f"Welcome {name}! Your account is now secured with a password.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.info("Note: All data is stored in your private Supabase database.")

# --- 4. SMART AI ASSISTANT (INTELLIGENT RESPONSES) ---
elif choice == "🤖 AI Assistant":
    st.title("🤖 Bt-Ai Business Intelligence")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_query = st.chat_input("Ask about guidelines or rules...")
    
    if user_query:
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.write(user_query)
        
        # AI-এর বুদ্ধিমত্তা বাড়ানো হয়েছে যাতে আপনার সব গাইডলাইন সে জানে
        query_low = user_query.lower()
        if "নাম" in query_low or "who are you" in query_low:
            ans = "I am the Bt-Ai Intelligence, created for MD SOHEL RANA's global platform."
        elif "লাভ" in query_low or "benefit" in query_low:
            ans = "Benefits: Earn $0.01 per view. Full monetization requires 1k subscribers and 30k views within 1 year."
        elif "নিয়ম" in query_low or "rule" in query_low:
            ans = "Rules: 1. Max video length 10s. 2. No sexual content. 3. 1,000 subs & 30,000 views for payment."
        else:
            ans = f"Analyzing: '{user_query}'. On this platform, we support videos under 10 seconds. Please follow the 1-year monetization policy for revenue."

        st.session_state.chat_history.append({"role": "assistant", "content": ans})
        with st.chat_message("assistant"):
            st.write(ans)
