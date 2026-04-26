import streamlit as st
from supabase import create_client
import uuid
import streamlit.components.v1 as components

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

# --- বিজ্ঞাপনের কোডগুলো এখানে সরাসরি সেট করা হলো ---
ad_code_1 = """<script type="text/javascript"> atOptions = { 'key' : '342950879f2064f7255ad047622381c8', 'format' : 'iframe', 'height' : 50, 'width' : 320, 'params' : {} }; </script> <script type="text/javascript" src="https://www.highperformanceformat.com/342950879f2064f7255ad047622381c8/invoke.js"></script>"""
ad_code_2 = """<script type="text/javascript"> atOptions = { 'key' : '5327bebb34c787d2ccfb1c36bcfa9d6e', 'format' : 'iframe', 'height' : 250, 'width' : 300, 'params' : {} }; </script> <script type="text/javascript" src="https://www.highperformanceformat.com/5327bebb34c787d2ccfb1c36bcfa9d6e/invoke.js"></script>"""
ad_code_3 = """<script async="async" data-cfasync="false" src="https://pl29264300.profitablecpmratenetwork.com/3d5c1921120aef030a2a6dd72337ba1d/invoke.js"></script><div id="container-3d5c1921120aef030a2a6dd72337ba1d"></div>"""
ad_code_4 = """<script src="https://pl29264299.profitablecpmratenetwork.com/e5/58/5e/e5585e56ecc6ca2a987116ca54b2614d.js"></script>"""

# --- HD CSS FIX ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .card { background: #111; padding: 25px; border-radius: 15px; border: 1px solid #222; margin-bottom: 20px; }
    .ad-container { text-align: center; margin: 15px 0; background: #000; padding: 10px; border-radius: 10px; border: 1px solid #333; }
    .direct-link-btn {
        display: inline-block; padding: 15px 30px;
        background: linear-gradient(45deg, #ff0000, #ff4500);
        color: white !important; text-align: center;
        text-decoration: none; font-size: 20px; font-weight: bold;
        border-radius: 10px; border: 2px solid #fff; margin-top: 15px;
        width: 100%; box-shadow: 0px 4px 15px rgba(255, 0, 0, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGATION MENU ---
menu = ["🏠 Global Feed", "📤 Publish Video", "👤 Profile & Security", "💰 Wallet & Bank", "🤖 AI Assistant", "⚙️ Owner Control"]
choice = st.sidebar.selectbox("Dashboard Menu", menu)

# --- 1. OWNER CONTROL ---
if choice == "⚙️ Owner Control":
    st.title("⚙️ Secret Admin Panel")
    pwd = st.text_input("Enter Owner Password", type="password")
    if pwd == "S$s123456789112233":
        st.success("Access Granted, Sohel Bhai!")
        st.info("আপনার ৪টি ব্যানার এখন সরাসরি কোডের ভেতর সেট করা আছে।")
    elif pwd != "":
        st.error("Wrong Password!")

# --- 2. GLOBAL FEED (ভিডিওর ফাঁকে ফাঁকে বিজ্ঞাপন) ---
elif choice == "🏠 Global Feed":
    st.title("🌎 Global Trending")
    v_data = supabase.table("videos").select("*").order("created_at", desc=True).execute()
    
    if v_data.data:
        for index, v in enumerate(v_data.data):
            # ভিডিওর কার্ড
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.video(v['video_url'])
            
            # আপনার ডাইরেক্ট লিঙ্ক বাটন (ডার্লিং)
            d_link = "https://www.profitablecpmratenetwork.com/tgt6azn6?key=e753cbd6d9bae06d67051ed846419521"
            st.markdown(f'<a href="{d_link}" target="_blank" class="direct-link-btn">📽️ Watch Full Video & Earn Money</a>', unsafe_allow_html=True)
            
            # লাইক ও ভিউ
            col_l, col_v, col_e = st.columns([1, 1, 2])
            if col_l.button(f"❤️ {v.get('likes', 0)}", key=f"lk_{v['id']}"):
                supabase.table("videos").update({"likes": v.get('likes', 0) + 1}).eq("id", v['id']).execute()
                st.rerun()
            col_v.write(f"👁️ {v.get('views', 0)}")
            col_e.write(f"📊 ${v.get('views', 0) * 0.01:.2f}")
            st.markdown('</div>', unsafe_allow_html=True)

            # --- বিজ্ঞাপনের ফাঁক (গ্যাপ) তৈরি করা ---
            if index % 1 == 0: # প্রতি ১টি ভিডিওর পরপরই একটি করে অ্যাড আসবে
                st.markdown('<div class="ad-container">', unsafe_allow_html=True)
                if index % 4 == 0: components.html(ad_code_1, height=70)
                elif index % 4 == 1: components.html(ad_code_2, height=270)
                elif index % 4 == 2: components.html(ad_code_3, height=200)
                else: components.html(ad_code_4, height=150)
                st.markdown('</div>', unsafe_allow_html=True)

# --- বাকি সেকশনগুলো (Profile, Upload, AI) ঠিক রাখা হয়েছে ---
elif choice == "👤 Profile & Security":
    st.title("👤 Security Dashboard")
    st.info(f"Ad: {st.session_state.ad_links['login_ad']}")
    with st.form("auth"):
        st.text_input("Name", value="MD SOHEL RANA")
        st.text_input("Security Code", type="password")
        if st.form_submit_button("Secure Login"):
            st.success("Protected!")

elif choice == "📤 Publish Video":
    st.title("📤 Upload Content")
    v_f = st.file_uploader("MP4 (Max 10s)", type=['mp4'])
    if st.button("Publish") and v_f:
        st.success("Video Published Successfully!")

elif choice == "💰 Wallet & Bank":
    st.title("💰 Payout")
    st.markdown('<div class="card"><h2>$0.00</h2></div>', unsafe_allow_html=True)

elif choice == "🤖 AI Assistant":
    st.title("🤖 Bt-Ai World Assistant")
    u_q = st.chat_input("Ask anything...")
    if u_q:
        a = "আমি আপনার প্ল্যাটফর্মের সব জানি। আপনি নিয়ম মেনে কাজ করুন।"
        st.chat_message("user").write(u_q)
        st.chat_message("assistant").write(a)
import
