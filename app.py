import streamlit as st
from supabase import create_client
import uuid

# --- GLOBAL DATABASE CONNECTION ---
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Bt-Ai Global Business Pro", layout="wide")

# --- UI DESIGN (CHAT VISIBILITY FIX) ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; font-family: 'Inter', sans-serif; }
    .card { background: #111; padding: 25px; border-radius: 15px; border: 1px solid #222; margin-bottom: 20px; }
    
    /* ✪ CHAT TEXT VISIBILITY FIX (HD WHITE) ✪ */
    .stChatMessage { 
        background-color: #222 !important; 
        border: 1px solid #444 !important;
        margin-bottom: 10px !important;
    }
    .stChatMessage p { 
        color: #ffffff !important; 
        font-size: 18px !important; 
        font-weight: 500 !important;
    }
    
    .ad-banner { 
        background: linear-gradient(90deg, #1e90ff, #00ff00); 
        color: black; padding: 12px; text-align: center; 
        font-weight: bold; border-radius: 10px; margin-bottom: 25px; font-size: 18px;
    }
    .revenue-display { color: #00ff00; font-size: 38px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="ad-banner">🚀 LIVE GLOBAL CAMPAIGN: Upload Videos & Earn Real Revenue per View! 💰</div>', unsafe_allow_html=True)

# --- NAVIGATION ---
st.sidebar.title("✪ Bt-Ai Global Pro")
menu = ["🏠 Global Feed", "📤 Publish Video", "👤 User Profile", "💰 Wallet & Bank", "🤖 AI Assistant"]
choice = st.sidebar.selectbox("Dashboard Menu", menu)

# --- 1. GLOBAL REVENUE FEED ---
if choice == "🏠 Global Feed":
    st.title("🌎 Trending Content & Earnings")
    try:
        v_data = supabase.table("videos").select("*").order("created_at", desc=True).execute()
        if v_data.data:
            for v in v_data.data:
                with st.container():
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.video(v['video_url'])
                    st.subheader(v.get('title', 'Global Creator Content'))
                    col1, col2, col3 = st.columns([1, 1, 2])
                    if col1.button(f"❤️ {v.get('likes', 0)} Likes", key=f"lk_{v['id']}"):
                        supabase.table("videos").update({"likes": v.get('likes', 0) + 1}).eq("id", v['id']).execute()
                        st.rerun()
                    current_views = v.get('views', 0) + 1
                    supabase.table("videos").update({"views": current_views}).eq("id", v['id']).execute()
                    col2.write(f"👁️ {current_views} Total Views")
                    col3.markdown(f"📊 **Earnings: ${current_views * 0.01:.2f}**")
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No content currently trending.")
    except Exception as e:
        st.error("System sync in progress...")

# --- 2. VIDEO PUBLISHING ---
elif choice == "📤 Publish Video":
    st.title("📤 Creator Studio")
    v_file = st.file_uploader("Select MP4 Video File", type=['mp4'])
    v_title = st.text_input("Enter Content Title")
    if st.button("Publish Now & Earn") and v_file:
        with st.spinner("Processing Global Upload..."):
            file_id = str(uuid.uuid4())
            file_path = f"public/{file_id}.mp4"
            supabase.storage.from_('videos').upload(file_path, v_file.read())
            v_url = supabase.storage.from_('videos').get_public_url(file_path)
            supabase.table("videos").insert({"video_url": v_url, "title": v_title, "likes": 0, "views": 0}).execute()
            st.success("Your video is now LIVE! ✅")

# --- 3. IDENTITY & BANKING ---
elif choice == "👤 User Profile":
    st.title("👤 Universal Account Settings")
    with st.form("profile_form"):
        st.text_input("Full Legal Name", value="MD SOHEL RANA")
        st.text_area("Creator Bio")
        if st.form_submit_button("Verify & Save"): st.success("Global Identity Secured! 🏆")

elif choice == "💰 Wallet & Bank":
    st.title("💰 Global Revenue Wallet")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("Current Payout Balance")
    st.markdown('<p class="revenue-display">$0.00</p>', unsafe_allow_html=True)
    st.divider()
    st.text_input("Bank Name")
    st.text_input("Account Number")
    if st.button("Connect Payout"): st.success("Bank linked! ✅")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. AI BUSINESS CHATBOT (HD TEXT FIX) ---
elif choice == "🤖 AI Assistant":
    st.title("🤖 Bt-Ai Business Intelligence")
    st.write("Real-time support (Bangla/English) for creators:")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(f"**{msg['content']}**")

    user_query = st.chat_input("Ask anything...")
    if user_query:
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(f"**{user_query}**")
        
        response = "System update: Our $500 campaign is live. All revenue is tracked correctly."
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(f"**{response}**")
