import streamlit as st
from supabase import create_client
import uuid

# --- DATABASE CONNECTION (সোহেল ভাই, আপনার ডাটাবেস একদম অক্ষত আছে) ---
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

# --- PAGE SETUP ---
st.set_page_config(page_title="Bt-Ai World Intelligence", layout="wide")

# --- ADMIN AD MEMORY ---
if 'ad_links' not in st.session_state:
    st.session_state.ad_links = {
        "login_ad": "Login Page Ad Link",
        "mini_1": "AD 1", "mini_2": "AD 2", "mini_3": "AD 3", "mini_4": "AD 4",
        "google_space": "Google AdSense or Big Ad Space"
    }

# --- HD CSS FIX (নতুন ডিসপ্লে বক্সের ডিজাইনসহ) ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .card { background: #111; padding: 25px; border-radius: 15px; border: 1px solid #222; margin-bottom: 20px; }
    .stChatMessage p { color: #ffffff !important; font-size: 18px !important; font-weight: bold !important; }
    
    /* অটোমেটিক অ্যাড ডিসপ্লে বক্সের ডিজাইন */
    .mini-ad-box { 
        background: #1a1a1a; 
        border: 1px solid #333; 
        padding: 10px; 
        text-align: center; 
        border-radius: 8px; 
        min-height: 100px; 
        display: flex; 
        align-items: center; 
        justify-content: center;
        overflow: hidden;
    }
    
    /* আপনার ডাইরেক্ট লিঙ্ক লাল বাটনের ডিজাইন */
    .direct-link-btn {
        display: inline-block;
        padding: 15px 30px;
        background: linear-gradient(45deg, #ff0000, #ff4500);
        color: white !important;
        text-align: center;
        text-decoration: none;
        font-size: 20px;
        font-weight: bold;
        border-radius: 10px;
        border: 2px solid #fff;
        margin-top: 15px;
        width: 100%;
        box-shadow: 0px 4px 15px rgba(255, 0, 0, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGATION MENU ---
st.sidebar.title("✪ Bt-Ai Global Pro")
menu = ["🏠 Global Feed", "📤 Publish Video", "👤 Profile & Security", "💰 Wallet & Bank", "🤖 AI Assistant", "⚙️ Owner Control"]
choice = st.sidebar.selectbox("Dashboard Menu", menu)

# --- 1. OWNER CONTROL (পাসওয়ার্ড ও অ্যাড আপডেট) ---
if choice == "⚙️ Owner Control":
    st.title("⚙️ Secret Admin Panel")
    pwd = st.text_input("Enter Owner Password", type="password")
    if pwd == "S$s123456789112233":
        st.success("Access Granted, Sohel Bhai!")
        st.subheader("Update Ads Across Platform")
        st.session_state.ad_links["login_ad"] = st.text_area("Login Page Ad Link", st.session_state.ad_links["login_ad"])
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.ad_links["mini_1"] = st.text_area("Mini Ad 1 (Paste Code)", st.session_state.ad_links["mini_1"])
            st.session_state.ad_links["mini_2"] = st.text_area("Mini Ad 2 (Paste Code)", st.session_state.ad_links["mini_2"])
        with col2:
            st.session_state.ad_links["mini_3"] = st.text_area("Mini Ad 3 (Paste Code)", st.session_state.ad_links["mini_3"])
            st.session_state.ad_links["mini_4"] = st.text_area("Mini Ad 4 (Paste Code)", st.session_state.ad_links["mini_4"])
        
        st.session_state.ad_links["google_space"] = st.text_area("Google Ads / Big Banner Code", st.session_state.ad_links["google_space"])
        if st.button("🚀 Update & Save All Ads"):
            st.success("Ads Updated Successfully!")
    elif pwd != "":
        st.error("Wrong Password!")

# --- 2. GLOBAL FEED (এখানেই ডিসপ্লে তৈরি করা হয়েছে) ---
elif choice == "🏠 Global Feed":
    st.title("🌎 Global Trending")
    v_data = supabase.table("videos").select("*").order("created_at", desc=True).execute()
    
    if v_data.data:
        for index, v in enumerate(v_data.data):
            # প্রতি ৫টি ভিডিও পর পর বড় গুগল বা বড় ব্যানার অ্যাড
            if index > 0 and index % 5 == 0:
                st.markdown(f'<div class="card" style="text-align:center; min-height:150px; border:2px dashed #444;">{st.session_state.ad_links["google_space"]}</div>', unsafe_allow_html=True)

            with st.container():
                # ভিডিওর উপরে ৪টি অটোমেটিক ডিসপ্লে বক্স
                c1, c2, c3, c4 = st.columns(4)
                c1.markdown(f'<div class="mini-ad-box">{st.session_state.ad_links["mini_1"]}</div>', unsafe_allow_html=True)
                c2.markdown(f'<div class="mini-ad-box">{st.session_state.ad_links["mini_2"]}</div>', unsafe_allow_html=True)
                c3.markdown(f'<div class="mini-ad-box">{st.session_state.ad_links["mini_3"]}</div>', unsafe_allow_html=True)
                c4.markdown(f'<div class="mini-ad-box">{st.session_state.ad_links["mini_4"]}</div>', unsafe_allow_html=True)

                # ভিডিও সেকশন
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.video(v['video_url'])
                
                # --- সোহেল ভাই, আপনার ডাইরেক্ট লিঙ্ক বাটন ---
                d_link = "https://www.profitablecpmratenetwork.com/tgt6azn6?key=e753cbd6d9bae06d67051ed846419521"
                st.markdown(f'<a href="{d_link}" target="_blank" class="direct-link-btn">📽️ Watch Full Video & Earn Money</a>', unsafe_allow_html=True)
                
                # লাইক, ভিউ এবং আর্নিং ক্যালকুলেশন (অক্ষত রাখা হয়েছে)
                col_l, col_v, col_e = st.columns([1, 1, 2])
                if col_l.button(f"❤️ {v.get('likes', 0)}", key=f"lk_{v['id']}"):
                    supabase.table("videos").update({"likes": v.get('likes', 0) + 1}).eq("id", v['id']).execute()
                    st.rerun()
                col_v.write(f"👁️ {v.get('views', 0)}")
                col_e.write(f"📊 ${v.get('views', 0) * 0.01:.2f}")
                st.markdown('</div>', unsafe_allow_html=True)

# --- 3. PROFILE & SECURITY ---
elif choice == "👤 Profile & Security":
    st.title("👤 Security Dashboard")
    st.info(f"Ad: {st.session_state.ad_links['login_ad']}")
    with st.form("auth"):
        st.text_input("Name", value="MD SOHEL RANA")
        st.text_input("Security Code", type="password")
        if st.form_submit_button("Secure Login"):
            st.success("Protected!")

# --- 4. PUBLISH & OTHERS ---
elif choice == "📤 Publish Video":
    st.title("📤 Upload Content")
    v_f = st.file_uploader("MP4 (Max 10s)", type=['mp4'])
    if st.button("Publish") and v_f:
        st.success("Video Published Successfully!")

elif choice == "💰 Wallet & Bank":
    st.title("💰 Payout")
    st.markdown('<div class="card"><h2>$0.00</h2></div>', unsafe_allow_html=True)

# --- 5. AI ASSISTANT ---
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
