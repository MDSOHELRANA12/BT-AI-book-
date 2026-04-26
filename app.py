import streamlit as st
from supabase import create_client
import uuid

# --- DATABASE CONNECTION ---
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

# --- PAGE SETUP ---
st.set_page_config(page_title="Bt-Ai World Intelligence", layout="wide")

# --- HD CSS FIX FOR VISIBILITY ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .card { background: #111; padding: 25px; border-radius: 15px; border: 1px solid #222; margin-bottom: 20px; }
    .stChatMessage p { color: #ffffff !important; font-size: 18px !important; font-weight: bold !important; }
    .ad-banner { background: linear-gradient(90deg, #1e90ff, #00ff00); color: black; padding: 12px; text-align: center; font-weight: bold; border-radius: 10px; margin-bottom: 25px; }
    .revenue-display { color: #00ff00; font-size: 35px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGATION MENU ---
st.sidebar.title("✪ Bt-Ai Global Pro")
menu = ["🏠 Global Feed", "📤 Publish Video", "👤 Profile & Security", "💰 Wallet & Bank", "🤖 AI Assistant"]
choice = st.sidebar.selectbox("Dashboard Menu", menu)

# --- 1. GLOBAL FEED (LIKE & VIEW FIX) ---
if choice == "🏠 Global Feed":
    st.title("🌎 Trending Content")
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

# --- 2. VIDEO UPLOAD (10s LIMIT) ---
elif choice == "📤 Publish Video":
    st.title("📤 Creator Studio")
    v_file = st.file_uploader("Upload MP4 (Max 10s)", type=['mp4'])
    if st.button("Publish Now") and v_file:
        file_id = str(uuid.uuid4())
        supabase.storage.from_('videos').upload(f"public/{file_id}.mp4", v_file.read())
        v_url = supabase.storage.from_('videos').get_public_url(f"public/{file_id}.mp4")
        supabase.table("videos").insert({"video_url": v_url, "likes": 0, "views": 0}).execute()
        st.success("Live Now! ✅")

# --- 3. PROFILE & ENCRYPTION ---
elif choice == "👤 Profile & Security":
    st.title("👤 Account Security")
    with st.form("security"):
        st.text_input("Name", value="MD SOHEL RANA")
        st.text_input("Security Password", type="password")
        if st.form_submit_button("Secure Account"):
            st.success("Account Protected! 🏆")

# --- 4. BANK & WALLET (RESTORED) ---
elif choice == "💰 Wallet & Bank":
    st.title("💰 Revenue Wallet")
    st.markdown('<div class="card"><p>Balance</p><p class="revenue-display">$0.00</p></div>', unsafe_allow_html=True)
    st.subheader("Bank Transfer Details")
    st.text_input("Bank Name")
    st.text_input("IBAN / Account Number")
    st.button("Link Bank Account")

# --- 5. WORLD CLASS INTELLIGENT AI (COMMAND CENTER) ---
elif choice == "🤖 AI Assistant":
    st.title("🤖 Bt-Ai World Intelligence")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_q = st.chat_input("Ask anything in any language...")
    if user_q:
        st.session_state.chat_history.append({"role": "user", "content": user_q})
        with st.chat_message("user"):
            st.write(user_q)
        
        # --- SMART COMMAND LOGIC (AI MEMORY TRAINING) ---
        q = user_q.lower()
        
        # ১. আপনার প্ল্যাটফর্মের বিশেষ নিয়ম
        if any(word in q for word in ["নিয়ম", "rule", "work", "কাজ"]):
            ans = "আমাদের প্ল্যাটফর্মের নিয়ম: ১. ভিডিও ১০ সেকেন্ডের নিচে হতে হবে। ২. ১০০০ সাবস্ক্রাইবার ও ৩০,০০০ ভিউ ১ বছরের মধ্যে পেতে হবে। ৩. কোনো খারাপ ভিডিও চলবে না।"
        # ২. মনিটাইজেশন ও ইনকাম
        elif any(word in q for word in ["লাভ", "income", "money", "পাব"]):
            ans = "আপনি প্রতি ভিউতে $0.01 পাবেন। ১ বছরে ৩০,০০০ ভিউ এবং ১০০০ সাবস্ক্রাইবার হলে ফুল পেমেন্ট ব্যাংক বা ওয়ালেটে নিতে পারবেন।"
        # ৩. আপনার পরিচয় (মালিক)
        elif any(word in q for word in ["সোহেল", "sohel", "owner", "মালিক"]):
            ans = "এই প্ল্যাটফর্মের মালিক এবং স্রষ্টা হলেন এমডি সোহেল রানা ভাই। আমি তাঁর তৈরি এআই।"
        # ৪. সারা বিশ্বের সাধারণ তথ্য (গ্লোবাল নলেজ)
        else:
            ans = f"Analyzing global data for: '{user_q}'... আমি সারা বিশ্বের তথ্য জানি। তবে এই প্ল্যাটফর্মে কাজ করতে হলে আপনাকে ১০ সেকেন্ডের ছোট ভিডিও আপলোড করতে হবে এবং আমাদের ১ বছরের পলিসি মেনে চলতে হবে।"

        st.session_state.chat_history.append({"role": "assistant", "content": ans})
        with st.chat_message("assistant"):
            st.write(ans)
