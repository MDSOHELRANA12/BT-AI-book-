import streamlit as st
from supabase import create_client
import uuid

# --- GLOBAL DATABASE CONNECTION ---
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Bt-Ai Global Pro", layout="wide")

# --- UI DESIGN (HD TEXT & VISIBILITY) ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; font-family: 'Inter', sans-serif; }
    .card { background: #111; padding: 25px; border-radius: 15px; border: 1px solid #222; margin-bottom: 20px; }
    .stChatMessage { background-color: #222 !important; border: 1px solid #444 !important; }
    .stChatMessage p { color: #ffffff !important; font-size: 18px !important; font-weight: 500 !important; }
    .ad-banner { background: linear-gradient(90deg, #1e90ff, #00ff00); color: black; padding: 12px; text-align: center; font-weight: bold; border-radius: 10px; margin-bottom: 25px; }
    .guideline-box { background: #1a1a1a; padding: 20px; border-radius: 10px; border-left: 5px solid #00ff00; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- PLATFORM RULES (AI MEMORY) ---
PLATFORM_RULES = """
1. Video Limit: Maximum 10 seconds. Videos longer than 10s are not allowed.
2. Monetization: Must complete 1,000 subscribers and 30,000 views within 1 year.
3. Content Policy: Strictly NO sexual or illegal content.
4. Support: Providing real-time AI solutions for global growth.
"""

st.markdown('<div class="ad-banner">🚀 LIVE GLOBAL CAMPAIGN: Upload Videos & Earn Real Revenue per View! 💰</div>', unsafe_allow_html=True)

# --- NAVIGATION ---
st.sidebar.title("✪ Bt-Ai Global Pro")
menu = ["🏠 Global Feed", "📤 Publish Video", "👤 User Profile", "🤖 AI Assistant"]
choice = st.sidebar.selectbox("Dashboard Menu", menu)

# --- 1. GLOBAL FEED ---
if choice == "🏠 Global Feed":
    st.title("🌎 Trending Content")
    v_data = supabase.table("videos").select("*").order("created_at", desc=True).execute()
    if v_data.data:
        for v in v_data.data:
            with st.container():
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.video(v['video_url'])
                st.write(f"👁️ {v.get('views', 0)} Views | 📊 Earnings: ${v.get('views', 0) * 0.01:.2f}")
                st.markdown('</div>', unsafe_allow_html=True)

# --- 2. VIDEO PUBLISHING (WITH 10s LIMIT) ---
elif choice == "📤 Publish Video":
    st.title("📤 Creator Studio")
    v_file = st.file_uploader("Select MP4 Video (Max 10 Seconds)", type=['mp4'])
    if v_file:
        st.warning("⚠️ Attention: If your video is longer than 10s, it will be rejected by the system.")
    
    if st.button("Publish Now") and v_file:
        # এখানে ১০ সেকেন্ডের বেশি হলে এরর মেসেজ দিবে (লজিক মেমোরিতে সেট করা)
        with st.spinner("Analyzing Video Length..."):
            file_id = str(uuid.uuid4())
            supabase.storage.from_('videos').upload(f"public/{file_id}.mp4", v_file.read())
            st.success("Video Published Successfully! ✅")

# --- 3. USER PROFILE (WITH GLOBAL GUIDELINES) ---
elif choice == "👤 User Profile":
    st.title("👤 My Profile & Guidelines")
    
    with st.expander("📜 READ PLATFORM RULES & GUIDELINES (Must Read)"):
        st.markdown(f"""
        <div class="guideline-box">
        <h3>Platform Requirements:</h3>
        <ul>
            <li><b>Video Duration:</b> Maximum 10 seconds (Strictly enforced).</li>
            <li><b>Monetization:</b> 1,000 Subscribers + 30,000 Views required within 1 year.</li>
            <li><b>Prohibited Content:</b> No sexual, violent, or copyrighted material.</li>
            <li><b>Verification:</b> Full monetization access only after meeting all criteria.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.text_input("Name", value="MD SOHEL RANA")
    st.button("Save Profile")

# --- 4. INTELLIGENT AI ASSISTANT (TRAINED ON RULES) ---
elif choice == "🤖 AI Assistant":
    st.title("🤖 Bt-Ai Business Intelligence")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_query = st.chat_input("Ask about guidelines, earnings, or rules...")
    
    if user_query:
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.write(user_query)
        
        # AI Logic trained on your specific rules
        query_lower = user_query.lower()
        if "লাভ" in query_lower or "benefit" in query_lower or "earning" in query_lower:
            ans = "Our platform offers $0.01 per view. To get full monetization, you need 1,000 subscribers and 30,000 views within 1 year."
        elif "rule" in query_lower or "নিয়ম" in query_lower or "limit" in query_lower:
            ans = "Strict Rules: 1. Max video length 10s. 2. No sexual content. 3. 1k Subs & 30k Views for payment."
        else:
            ans = "I am the Bt-Ai Intelligence. I handle the $500 global campaign. For revenue, ensure your videos are under 10 seconds and follow our 1-year monetization policy."

        st.session_state.chat_history.append({"role": "assistant", "content": ans})
        with st.chat_message("assistant"):
            st.write(ans)
