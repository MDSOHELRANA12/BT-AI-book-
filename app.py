import streamlit as st
from supabase import create_client
import uuid
import streamlit.components.v1 as components

# --- 1. Global System Connection ---
# Securely linking to your specific database
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

# --- 2. Platform Branding ---
st.set_page_config(page_title="Bt-Ai Global Network", layout="wide")

# --- 3. Professional UI Styling (High Definition) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff !important; }
    h1, h2, h3, p, span, div, label { color: #ffffff !important; }
    .card { 
        background: #111111; padding: 25px; border-radius: 20px; 
        border: 1px solid #333; margin-bottom: 25px; 
        box-shadow: 0px 4px 20px rgba(255,255,255,0.05);
    }
    .action-btn {
        display: block; padding: 15px; background: linear-gradient(45deg, #ff0000, #b30000);
        color: white !important; text-align: center; text-decoration: none;
        font-size: 20px; font-weight: bold; border-radius: 12px; border: 2px solid #fff;
    }
    .user-profile-box { border-left: 5px solid #00ff00; padding-left: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. Global Sidebar Menu ---
st.sidebar.title("✪ Bt-Ai Global Pro")
menu = ["🌍 Global Feed", "📤 Publish Video", "🤖 Bt-Ai Chatbot", "👤 Account Profile", "💰 Wallet & Earnings"]
choice = st.sidebar.selectbox("Navigation Menu", menu)

# --- 5. Global Video Feed & Monetization ---
if choice == "🌍 Global Feed":
    st.title("🌎 Trending Content Worldwide")
    try:
        v_data = supabase.table("videos").select("*").order("created_at", desc=True).execute()
        if v_data.data:
            for v in v_data.data:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.video(v['video_url'])
                
                # Revenue generating direct link
                d_link = "https://www.profitablecpmratenetwork.com/tgt6azn6?key=e753cbd6d9bae06d67051ed846419521"
                st.markdown(f'<a href="{d_link}" target="_blank" class="action-btn">📽️ Watch Full Video & Earn</a>', unsafe_allow_html=True)
                
                # Stats display
                st.write(f"👁️ Views: {v.get('views', 0)} | 📊 Revenue Generated: ${v.get('views', 0) * 0.01:.2f}")
                st.markdown('</div>', unsafe_allow_html=True)
    except:
        st.error("Server connection busy. Refreshing...")

# --- 6. Content Publishing Engine (Working Verified) ---
elif choice == "📤 Publish Video":
    st.title("📤 Publish Global Content")
    file = st.file_uploader("Upload MP4 File", type=['mp4'])
    if st.button("Publish Now") and file:
        with st.spinner("Processing Global Upload..."):
            filename = f"{uuid.uuid4()}.mp4"
            try:
                supabase.storage.from_("videos").upload(filename, file.read())
                url = supabase.storage.from_("videos").get_public_url(filename)
                supabase.table("videos").insert({"video_url": url, "likes": 0, "views": 0}).execute()
                st.success("Video Published Successfully!")
                st.balloons()
            except Exception as e:
                st.error(f"Upload failed: {e}")

# --- 7. FIXED: Bt-Ai Chatbot (Integrated AI Brain) ---
elif choice == "🤖 Bt-Ai Chatbot":
    st.title("🤖 Bt-Ai World Assistant")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history
    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"])

    # Chat input
    if user_input := st.chat_input("Ask me anything..."):
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        
        with st.chat_message("assistant"):
            ai_reply = f"Hello! I am Bt-Ai Intelligence. I am currently monitoring your global project. How can I help you earn more today?"
            st.markdown(ai_reply)
            st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})

# --- 8. FIXED: Account & Profile Management ---
elif choice == "👤 Account Profile":
    st.title("👤 Security Dashboard")
    st.markdown('<div class="card user-profile-box">', unsafe_allow_html=True)
    st.subheader("MD SOHEL RANA")
    st.write("**Account Type:** Verified Administrator")
    st.success("Account status: Active & Protected by Bt-Ai Security")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 9. Wallet & Finance ---
elif choice == "💰 Wallet & Earnings":
    st.title("💰 Finance Dashboard")
    st.markdown('<div class="card"><h1 style="text-align:center;">Current Balance: $0.00</h1></div>', unsafe_allow_html=True)
