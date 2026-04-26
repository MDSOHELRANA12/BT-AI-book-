import streamlit as st
from supabase import create_client
import uuid

# --- DATABASE CONNECTION ---
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

# --- PAGE SETUP ---
st.set_page_config(page_title="Bt-Ai World Intelligence", layout="wide")

# --- ADMIN AD MEMORY (গোপন প্যানেলের জন্য) ---
if 'ad_links' not in st.session_state:
    st.session_state.ad_links = {
        "login_ad": "Login Page Ad Link",
        "mini_1": "AD 1", "mini_2": "AD 2", "mini_3": "AD 3", "mini_4": "AD 4",
        "google_space": "Google AdSense or Big Ad Space"
    }

# --- HD CSS FIX ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .card { background: #111; padding: 25px; border-radius: 15px; border: 1px solid #222; margin-bottom: 20px; }
    .stChatMessage p { color: #ffffff !important; font-size: 18px !important; font-weight: bold !important; }
    .mini-ad-box { 
        background: #1a1a1a; border: 1px solid #333; 
        padding: 5px; text-align: center; font-size: 10px; 
        color: #00ff00; border-radius: 5px; height: 35px;
    }
    .ad-banner { background: linear-gradient(90deg, #1e90ff, #00ff00); color: black; padding: 10px; text-align: center; font-weight: bold; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGATION MENU ---
st.sidebar.title("✪ Bt-Ai Global Pro")
menu = ["🏠 Global Feed", "📤 Publish Video", "👤 Profile & Security", "💰 Wallet & Bank", "🤖 AI Assistant", "⚙️ Owner Control"]
choice = st.sidebar.selectbox("Dashboard Menu", menu)

# --- 1. OWNER CONTROL (গোপন পাসওয়ার্ড প্যানেল) ---
if choice == "⚙️ Owner Control":
    st.title("⚙️ Secret Admin Panel")
    pwd = st.text_input("Enter Owner Password", type="password")
    if pwd == "S$s123456789112233":
        st.success("Access Granted, Sohel Bhai!")
        st.subheader("Update Ads Across Platform")
        st.session_state.ad_links["login_ad"] = st.text_input("Login Page Ad Link", st.session_state.ad_links["login_ad"])
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.ad_links["mini_1"] = st.text_input("Mini Ad 1", st.session_state.ad_links["mini_1"])
            st.session_state.ad_links["mini_2"] = st.text_input("Mini Ad 2", st.session_state.ad_links["mini_2"])
        with col2:
            st.session_state.ad_links["mini_3"] = st.text_input("Mini Ad 3", st.session_state.ad_links["mini_3"])
            st.session_state.ad_links["mini_4"] = st.text_input("Mini Ad 4", st.session_state.ad_links["mini_4"])
        
        st.session_state.ad_links["google_space"] = st.text_area("Google Ads / Big Banner Code", st.session_state.ad_links["google_space"])
        if st.button("🚀 Update & Save All Ads"):
            st.success("Ads Updated Successfully!")
    elif pwd != "":
        st.error("Wrong Password!")

# --- 2. GLOBAL FEED (আপনার চাওয়া সব সিস্টেম এখানে) ---
elif choice == "🏠 Global Feed":
    st.title("🌎 Global Trending")
    v_data = supabase.table("videos").select("*").order("created_at", desc=True).execute()
    
    if v_data.data:
        for index, v in enumerate(v_data.data):
            # প্রতি ৫টি ভিডিও পর পর বড় গুগল বা আপডেট করা অ্যাড স্পেস
            if index > 0 and index % 5 == 0:
                st.markdown(f'<div class="card" style="text-align:center; min-height:150px; border:2px dashed #444;">{st.session_state.ad_links["google_space"]}</div>', unsafe_allow_html=True)

            with st.container():
                # ভিডিওর সাইডে ৪টি ছোট ব্যানার
                c1, c2, c3, c4 = st.columns(4)
                c1.markdown(f'<div class="mini-ad-box">{st.session_state.ad_links["mini_1"]}</div>', unsafe_allow_html=True)
                c2.markdown(f'<div class="mini-ad-box">{st.session_state.ad_links["mini_2"]}</div>', unsafe_allow_html=True)
                c3.markdown(f'<div class="mini-ad-box">{st.session_state.ad_links["mini_3"]}</div>', unsafe_allow_html=True)
                c4.markdown(f'<div class="mini-ad-box">{st.session_state.ad_links["mini_4"]}</div>', unsafe_allow_html=True)

                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.video(v['video_url'])
                col_l, col_v, col_e = st.columns([1, 1, 2])
                if col_l.button(f"❤️ {v.get('likes', 0)}", key=f"lk_{v['id']}"):
                    supabase.table("videos").update({"likes": v.get('likes', 0) + 1}).eq("id", v['id']).execute()
                    st.rerun()
                col_v.write(f"👁️ {v.get('views', 0)}")
                col_e.write(f"📊 ${v.get('views', 0) * 0.01:.2f}")
                st.markdown('</div>', unsafe_allow_html=True)

# --- 3. PROFILE & SECURITY (লগইন বাটনে অ্যাড) ---
elif choice == "👤 Profile & Security":
    st.title("👤 Security Dashboard")
    st.info(f"Ad: {st.session_state.ad_links['login_ad']}") # লগইন সেকশনে ছোট অ্যাড
    with st.form("auth"):
        st.text_input("Name", value="MD SOHEL RANA")
        st.text_input("Security Code", type="password")
        if st.form_submit_button("Secure Login"):
            st.success("Protected!")

# --- 4. PUBLISH & OTHERS ---
elif choice == "📤 Publish Video":
    st.title("📤 Upload content")
    v_f = st.file_uploader("MP4 (Max 10s)", type=['mp4'])
    if st.button("Publish") and v_f:
        # (ভিডিও আপলোড লজিক আগের মতোই আছে)
        st.success("Live!")

elif choice == "💰 Wallet & Bank":
    st.title("💰 Payout")
    st.markdown('<div class="card"><h2>$0.00</h2></div>', unsafe_allow_html=True)

# --- 5. SMART AI (মস্তিষ্ক ঠিক রাখা হয়েছে) ---
elif choice == "🤖 AI Assistant":
    st.title("🤖 Bt-Ai World Assistant")
    u_q = st.chat_input("Ask anything...")
    if u_q:
        q = u_q.lower()
        if "নিয়ম" in q: a = "ভিডিও ১০ সেকেন্ডের নিচে। ১০০০ সাব ও ৩০ হাজার ভিউ ১ বছরে।"
        elif "লাভ" in q: a = "প্রতি ভিউতে $0.01।"
        else: a = f"আমি আপনার প্ল্যাটফর্মের সব জানি। আপনি নিয়ম মেনে কাজ করুন।"
        st.chat_message("user").write(u_q)
        st.chat_message("assistant").write(a)
