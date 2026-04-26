import streamlit as st
from supabase import create_client
import uuid
import streamlit.components.v1 as components

# --- ১. হাই-স্পিড গ্লোবাল সার্ভার কানেকশন ---
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

# --- ২. সারা বিশ্বের জন্য পেইজ সেটআপ ---
st.set_page_config(page_title="BT-AI Global World", layout="wide")

# --- ৩. পাওয়ারফুল ডার্ক গোল্ড ডিজাইন ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .video-card { 
        background: #0d0d0d; border: 2px solid #1a1a1a; 
        border-radius: 20px; padding: 20px; margin-bottom: 30px;
        box-shadow: 0 4px 20px rgba(255, 0, 0, 0.1);
    }
    .direct-btn {
        display: block; width: 100%; padding: 15px; margin: 10px 0;
        background: linear-gradient(90deg, #ff0000, #990000);
        color: white !important; text-align: center; border-radius: 12px;
        font-weight: bold; text-decoration: none; border: 1px solid #fff;
    }
    .stats-row { display: flex; justify-content: space-around; padding: 10px; background: #111; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- ৪. আপনার দেওয়া ব্যানার অ্যাড ও ডাইরেক্ট লিঙ্কস ---
ad_1 = """<script type="text/javascript">atOptions = {'key' : '342950879f2064f7255ad047622381c8','format' : 'iframe','height' : 50,'width' : 320,'params' : {}};</script><script src="https://www.highperformanceformat.com/342950879f2064f7255ad047622381c8/invoke.js"></script>"""
ad_2 = """<script type="text/javascript">atOptions = {'key' : '5327bebb34c787d2ccfb1c36bcfa9d6e','format' : 'iframe','height' : 250,'width' : 300,'params' : {}};</script><script src="https://www.highperformanceformat.com/5327bebb34c787d2ccfb1c36bcfa9d6e/invoke.js"></script>"""

d_link_1 = "https://www.profitablecpmratenetwork.com/krgreepsz8?key=08a0fdc6d7ed4f33a60d1f4910ec27c5"
d_link_2 = "https://www.profitablecpmratenetwork.com/tgt6azn6?key=e753cbd6d9bae06d67051ed846419521"

# --- ৫. গ্লোবাল প্রোফাইল সিস্টেম ---
if 'user' not in st.session_state:
    st.session_state.user = None

st.sidebar.title("👤 Global Identity")
if not st.session_state.user:
    u_name = st.sidebar.text_input("Enter Your Name")
    if st.sidebar.button("Join World"):
        st.session_state.user = u_name
        st.rerun()
else:
    st.sidebar.success(f"Verified: {st.session_state.user}")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

# --- ৬. মেইন ন্যাভিগেশন ---
menu = ["🌍 World Feed", "📤 Upload Video", "👤 My Profile", "💰 Earnings"]
choice = st.selectbox("Switch View", menu)

# --- ৭. ওয়ার্ল্ড ফিড (ভিডিওর ফাঁকে ফাঁকে ব্যানার ও বাটন) ---
if choice == "🌍 World Feed":
    st.title("🌎 Trending Globally")
    components.html(ad_1, height=70) # শুরুতে ব্যানার
    
    try:
        res = supabase.table("videos").select("*").order("created_at", desc=True).execute()
        if res.data:
            for i, v in enumerate(res.data):
                st.markdown('<div class="video-card">', unsafe_allow_html=True)
                st.video(v['video_url'])
                
                # ভিডিওর ঠিক নিচে আপনার ডাইরেক্ট লিঙ্ক বাটন
                st.markdown(f'<a href="{d_link_1}" target="_blank" class="direct-btn">🚀 Instant Access Offer</a>', unsafe_allow_html=True)
                
                # রিয়েল অ্যালগরিদম (লাইক ও ভিউ আপডেট)
                v_id = v['id']
                v_count = v.get('views', 0) + 1
                supabase.table("videos").update({"views": v_count}).eq("id", v_id).execute()
                
                st.markdown(f"""
                <div class="stats-row">
                    <span>👁️ {v_count} Views</span>
                    <span style="color:red; font-weight:bold;">❤️ {v.get('likes', 0)} Likes</span>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Like this video", key=f"lk_{v_id}"):
                    supabase.table("videos").update({"likes": v.get('likes', 0) + 1}).eq("id", v_id).execute()
                    st.rerun()
                
                # ২য় লিঙ্কের বাটন
                st.markdown(f'<a href="{d_link_2}" target="_blank" class="direct-btn" style="background: #333;">💎 VIP Direct Link</a>', unsafe_allow_html=True)
                
                # প্রতি ভিডিওর পর পর ব্যানারের ফাঁক
                if i % 2 == 0:
                    st.write("--- Advertisement ---")
                    components.html(ad_2, height=270)
                
                st.markdown('</div>', unsafe_allow_html=True)
    except: st.info("ভিডিও লোড হচ্ছে...")

# --- ৮. ভিডিও আপলোড (সুপার ফাস্ট ও রিয়েল) ---
elif choice == "📤 Upload Video":
    st.title("📤 Publish Globally")
    if st.session_state.user:
        file = st.file_uploader("Select Video File (MP4)", type=['mp4'])
        if st.button("🚀 Publish Now") and file:
            with st.spinner("Broadcasting to Global Servers..."):
                f_name = f"{uuid.uuid4()}.mp4"
                # স্টোরেজে আপলোড
                supabase.storage.from_("videos").upload(f_name, file.read())
                p_url = supabase.storage.from_("videos").get_public_url(f_name)
                
                # ডাটাবেসে সেভ (সব কলাম ফিক্স করা হয়েছে)
                supabase.table("videos").insert({
                    "video_url": p_url,
                    "uploader_name": st.session_state.user,
                    "views": 0,
                    "likes": 0
                }).execute()
                st.success("ভিডিওটি এখন সারা বিশ্বের কাছে পৌঁছে গেছে!")
    else: st.warning("আগে প্রোফাইল সেট করে নিন।")

# --- ৯. প্রফেশনাল প্রোফাইল ---
elif choice == "👤 My Profile":
    st.title("👤 My Global ID")
    if st.session_state.user:
        st.markdown(f"""
        <div style="padding:40px; border:2px solid red; border-radius:20px; text-align:center; background:#111;">
            <h1 style="color:red;">{st.session_state.user}</h1>
            <p>Verified World Admin | Global Reach Active</p>
        </div>
        """, unsafe_allow_html=True)
    else: st.info("আপনার প্রোফাইল দেখতে জয়েন করুন।")

# --- ১০. আর্নিং সিস্টেম ---
elif choice == "💰 Earnings":
    st.title("💰 Revenue Dashboard")
    st.metric("Global Balance", "$0.00", "+$0.00 today")
