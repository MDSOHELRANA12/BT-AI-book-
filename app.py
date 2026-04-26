import streamlit as st
from supabase import create_client
import uuid
import streamlit.components.v1 as components

# --- ১. ডাটাবেস কানেকশন (সোহেল ভাই, আপনার ডাটাবেস একদম নিরাপদ) ---
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

# --- ২. পেজ সেটআপ ---
st.set_page_config(page_title="Bt-Ai World Intelligence", layout="wide")

# --- ৩. বিজ্ঞাপনের কোড (ব্যানার ১, ২, ৩, ৪) ---
ad_code_1 = """<script type="text/javascript"> atOptions = { 'key' : '342950879f2064f7255ad047622381c8', 'format' : 'iframe', 'height' : 50, 'width' : 320, 'params' : {} }; </script> <script type="text/javascript" src="https://www.highperformanceformat.com/342950879f2064f7255ad047622381c8/invoke.js"></script>"""
ad_code_2 = """<script type="text/javascript"> atOptions = { 'key' : '5327bebb34c787d2ccfb1c36bcfa9d6e', 'format' : 'iframe', 'height' : 250, 'width' : 300, 'params' : {} }; </script> <script type="text/javascript" src="https://www.highperformanceformat.com/5327bebb34c787d2ccfb1c36bcfa9d6e/invoke.js"></script>"""
ad_code_3 = """<script async="async" data-cfasync="false" src="https://pl29264300.profitablecpmratenetwork.com/3d5c1921120aef030a2a6dd72337ba1d/invoke.js"></script><div id="container-3d5c1921120aef030a2a6dd72337ba1d"></div>"""
ad_code_4 = """<script src="https://pl29264299.profitablecpmratenetwork.com/e5/58/5e/e5585e56ecc6ca2a987116ca54b2614d.js"></script>"""

# --- ৪. এইচডি ডিজাইন এবং পরিষ্কার লেখা (সাদা টেক্সট) ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #ffffff !important; }
    h1, h2, h3, p, span, div { color: #ffffff !important; }
    .card { background: #1a1a1a; padding: 25px; border-radius: 20px; border: 1px solid #333; margin-bottom: 25px; box-shadow: 0px 4px 20px rgba(0,0,0,0.5); }
    .direct-link-btn {
        display: block; padding: 15px; background: linear-gradient(45deg, #ff0000, #ff4500);
        color: #ffffff !important; text-align: center; text-decoration: none;
        font-size: 20px; font-weight: bold; border-radius: 12px; margin-top: 15px;
        border: 2px solid #fff; transition: 0.3s;
    }
    .ad-container { text-align: center; padding: 15px; background: #000; border-radius: 10px; margin: 15px 0; border: 1px dashed #555; }
    .stButton>button { width: 100%; border-radius: 10px; background-color: #333; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- ৫. সাইডবার মেনু ---
st.sidebar.title("✪ Bt-Ai Global Pro")
menu = ["🏠 Global Feed", "📤 Publish Video", "💰 Wallet & Bank", "👤 Profile & Security", "⚙️ Owner Control"]
choice = st.sidebar.selectbox("Dashboard Menu", menu)

# --- ৬. গ্লোবাল ফিড (ভিডিওর ফাঁকে ফাঁকে বিজ্ঞাপন) ---
if choice == "🏠 Global Feed":
    st.title("🌎 Global Trending Feed")
    try:
        v_data = supabase.table("videos").select("*").order("created_at", desc=True).execute()
        if v_data.data:
            for index, v in enumerate(v_data.data):
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.video(v['video_url'])
                
                # আপনার সেই ডাইরেক্ট লিঙ্ক বাটন (ডার্লিং)
                d_link = "https://www.profitablecpmratenetwork.com/tgt6azn6?key=e753cbd6d9bae06d67051ed846419521"
                st.markdown(f'<a href="{d_link}" target="_blank" class="direct-link-btn">📽️ Watch Full Video & Earn Money</a>', unsafe_allow_html=True)
                
                # লাইক ও ভিউ কাউন্টার (সাদা লেখা)
                c1, c2, c3 = st.columns([1, 1, 2])
                if c1.button(f"❤️ Like ({v.get('likes', 0)})", key=f"lk_{v['id']}"):
                    supabase.table("videos").update({"likes": v.get('likes', 0) + 1, "views": v.get('views', 0) + 1}).eq("id", v['id']).execute()
                    st.rerun()
                c2.markdown(f"**👁️ Views: {v.get('views', 0)}**", unsafe_allow_html=True)
                c3.markdown(f"**📊 Earnings: ${v.get('views', 0) * 0.01:.2f}**", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

                # বিজ্ঞাপনগুলো অটোমেটিক ঘুরবে
                st.markdown('<div class="ad-container">', unsafe_allow_html=True)
                if index % 4 == 0: components.html(ad_code_1, height=70)
                elif index % 4 == 1: components.html(ad_code_2, height=270)
                elif index % 4 == 2: components.html(ad_code_3, height=200)
                else: components.html(ad_code_4, height=150)
                st.markdown('</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error("ডাটাবেস থেকে ভিডিও লোড করা যাচ্ছে না।")

# --- ৭. ভিডিও আপলোড (একবারে কাজ করবে) ---
elif choice == "📤 Publish Video":
    st.title("📤 Publish Your Content")
    v_file = st.file_uploader("Select MP4 Video File", type=['mp4'])
    
    if st.button("Publish Now") and v_file:
        with st.spinner("Processing... Please wait, Sohel Bhai!"):
            unique_filename = f"{uuid.uuid4()}.mp4"
            try:
                # সুপাবেস স্টোরেজে আপলোড
                supabase.storage.from_("videos").upload(unique_filename, v_file.read())
                v_url = supabase.storage.from_("videos").get_public_url(unique_filename)
                # ডাটাবেসে তথ্য রাখা
                supabase.table("videos").insert({"video_url": v_url, "likes": 0, "views": 0}).execute()
                st.success("Congratulations! Video Published Successfully.")
                st.balloons()
            except Exception as e:
                st.error(f"Error: {e}")

# --- ৮. ওয়ালেট (টাকার হিসাব) ---
elif choice == "💰 Wallet & Bank":
    st.title("💰 Payout & Earnings")
    v_total = supabase.table("videos").select("views").execute()
    total_views = sum([x['views'] for x in v_total.data]) if v_total.data else 0
    st.markdown(f"""
    <div class="card">
        <h2 style='text-align:center;'>Current Balance</h2>
        <h1 style='text-align:center; font-size: 50px;'>${total_views * 0.01:.2f}</h1>
        <p style='text-align:center;'>Keep uploading videos to earn more!</p>
    </div>
    """, unsafe_allow_html=True)

# --- ৯. প্রোফাইল ---
elif choice == "👤 Profile & Security":
    st.title("👤 User Profile")
    st.markdown(f'<div class="card"><h3>Name: MD SOHEL RANA</h3><p>Status: Verified Member</p></div>', unsafe_allow_html=True)

# --- ১০. অনার কন্ট্রোল ---
elif choice == "⚙️ Owner Control":
    st.title("⚙️ Security Panel")
    pwd = st.text_input("Enter Owner Password", type="password")
    if pwd == "S$s123456789112233":
        st.success("Hello Sohel Bhai! Your platform is 100% Secure.")
import
