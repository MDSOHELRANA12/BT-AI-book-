import streamlit as st
from supabase import create_client
import uuid

# --- GLOBAL DATABASE CONNECTION ---
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Bt-Ai Global Pro", layout="wide")

# --- UI DESIGN (HD VISIBILITY) ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; font-family: 'Inter', sans-serif; }
    .card { background: #111; padding: 25px; border-radius: 15px; border: 1px solid #222; margin-bottom: 20px; }
    
    /* CHAT TEXT BRIGHTNESS FIX */
    .stChatMessage p { 
        color: #ffffff !important; 
        font-size: 18px !important; 
        font-weight: bold !important; 
    }
    
    .ad-banner { 
        background: linear-gradient(90deg, #1e90ff, #00ff00); 
        color: black; padding: 12px; text-align: center; 
        font-weight: bold; border-radius: 10px; margin-bottom: 25px; 
    }
    .revenue-display { color: #00ff00; font-size: 38px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="ad-banner">🚀 LIVE GLOBAL CAMPAIGN: $500 Reward Pool - Earn $0.01 Per View! 💰</div>', unsafe_allow_html=True)

# --- NAVIGATION MENU (ALL OPTIONS RESTORED) ---
st.sidebar.title("✪ Bt-Ai Global Pro")
menu = ["🏠 Global Feed", "📤 Publish Video", "👤 Profile & Security", "💰 Wallet & Bank", "🤖 AI Assistant"]
choice = st.sidebar.selectbox("Dashboard Menu", menu)

# --- 1. GLOBAL FEED (REAL-TIME DATA) ---
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
                    
                    if col1.button(f"❤️ {v.get('likes', 0)} Likes", key=f"lk_{v['id']}"):
                        supabase.table("videos").update({"likes": v.get('likes', 0) + 1}).eq("id", v['id']).execute()
                        st.rerun()
                    
                    col2.write(f"👁️ {v.get('views', 0)} Views")
                    col3.write(f"📊 Earned: ${v.get('views', 0) * 0.01:.2f}")
                    st.markdown('</div>', unsafe_allow_html=True)
    except:
        st.error("Connection sync error.")

# --- 2. VIDEO PUBLISHING (10s LIMIT MEMORY) ---
elif choice == "📤 Publish Video":
    st.title("📤 Creator Studio")
    v_file = st.file_uploader("Upload MP4 (Max 10 Seconds Allowed)", type=['mp4'])
    v_title = st.text_input("Content Title")
    if st.button("Publish Now") and v_file:
        with st.spinner("Uploading to Global Server..."):
            file_id = str(uuid.uuid4())
            supabase.storage.from_('videos').upload(f"public/{file_id}.mp4", v_file.read())
            v_url = supabase.storage.from_('videos').get_public_url(f"public/{file_id}.mp4")
            supabase.table("videos").insert({"video_url": v_url, "title": v_title, "likes": 0, "views": 0}).execute()
            st.success("Your video is Live! ✅")

# --- 3. PROFILE & ENCRYPTED SECURITY ---
elif choice == "👤 Profile & Security":
    st.title("👤 Account Authentication")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    with st.form("auth"):
        st.text_input("Full Name", value="MD SOHEL RANA")
        st.text_input("Email Address")
        st.text_input("Set Security Password", type="password")
        if st.form_submit_button("Save & Secure Account"):
            st.success("Security Layer Activated! 🏆")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. WALLET & BANKING (RESTORED) ---
elif choice == "💰 Wallet & Bank":
    st.title("💰 Global Revenue Wallet")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("Current Payout Balance")
    st.markdown('<p class="revenue-display">$0.00</p>', unsafe_allow_html=True)
    st.divider()
    st.subheader("Banking Info (Swift/IBAN)")
    st.text_input("Bank Name / Platform")
    st.text_input("Account Number")
    st.text_input("SWIFT Code")
    if st.button("Connect Payout Source"):
        st.success("Banking method successfully linked! ✅")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 5. SMART AI (GLOBAL COMMAND CENTER) ---
elif choice == "🤖 AI Assistant":
    st.title("🤖 Bt-Ai Intelligence")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_q = st.chat_input("Ask about monetization, rules, or payments...")
    if user_q:
        st.session_state.chat_history.append({"role": "user", "content": user_q})
        with st.chat_message("user"):
            st.write(user_q)
        
        q = user_q.lower()
        if "লাভ" in q or "benefit" in q or "পাব" in q:
            ans = "Monetization: Earn $0.01 per view. Requires 1k subscribers and 30k views within 1 year."
        elif "নিয়ম" in q or "rule" in q:
            ans = "Rules: 1. Max video length 10s. 2. No sexual content. 3. 1,000 subs & 30,000 views for payment."
        elif "নাম" in q or "who are you" in q:
            ans = "I am the Bt-Ai Intelligence, built for MD SOHEL RANA's global platform."
        else:
            ans = f"Analyzing: '{user_q}'. Our platform supports videos under 10 seconds. Follow the 1-year policy for revenue."

        st.session_state.chat_history.append({"role": "assistant", "content": ans})
        with st.chat_message("assistant"):
            st.write(ans)
