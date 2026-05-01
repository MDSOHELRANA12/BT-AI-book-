import streamlit as st
from supabase import create_client
import uuid
import random

# ১. গুগল অ্যাডসেন্স ভেরিফিকেশন এবং পাবলিশার আইডি (এটি অদৃশ্য থাকবে)
st.markdown("""
    <div style="display: none;">
        <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1831608481745604" crossorigin="anonymous"></script>
        <meta name="google-adsense-account" content="ca-pub-1831608481745604">
    </div>
    """, unsafe_allow_html=True)

# ২. সুপাবেস কানেকশন
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

# ৩. পেজ সেটআপ
st.set_page_config(page_title="BT AI book", layout="wide")

# ৪. হেল্পার ফাংশন
def format_value(value):
    if value >= 1000000: return f"{value/1000000:.1f}M"
    elif value >= 1000: return f"{value/1000:.1f}K"
    return str(value)

# ৫. ডিজাইন ও স্টাইল (আপনার অরিজিনাল কাঠামো)
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .video-card { 
        background: #0d0d0d; border: 1px solid #333; border-radius: 15px; 
        padding: 15px; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    .user-avatar { width: 50px; height: 50px; border-radius: 50%; border: 2px solid #00ff00; object-fit: cover; margin-right: 12px; }
    .username-text { font-weight: bold; font-size: 18px; color: #fff; }
    .stat-box { font-size: 14px; color: #00ff00; font-weight: bold; margin-right: 15px; }
    .btn-reward { display: block; width: 100%; padding: 12px; margin: 10px 0; background: linear-gradient(135deg, #ed1c24, #aa0000); color: white !important; text-align: center; border-radius: 8px; font-weight: bold; text-decoration: none; }
    .big-ad-box { background: #1a1a1a; border: 2px dashed #ed1c24; border-radius: 15px; padding: 25px; text-align: center; margin-bottom: 30px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ BT AI book")

# ৬. লগইন সিস্টেম
if 'user' not in st.session_state:
    st.session_state.user = None
    st.session_state.pic = None

if not st.session_state.user:
    st.sidebar.header("🔐 User Login")
    u_name = st.sidebar.text_input("Enter Your Registered Name")
    if u_name:
        user_data = supabase.table("users").select("*").eq("username", u_name).execute()
        if user_data.data:
            if st.sidebar.button("Login"):
                st.session_state.user = u_name
                st.session_state.pic = user_data.data[0]['profile_pic']
                st.rerun()
        else:
            u_pic = st.sidebar.file_uploader("Upload Photo once", type=['jpg', 'png', 'jpeg'])
            if st.sidebar.button("Create Account"):
                if u_name and u_pic:
                    fname = f"p_{uuid.uuid4()}.jpg"
                    supabase.storage.from_("videos").upload(path=fname, file=u_pic.getvalue())
                    p_url = supabase.storage.from_("videos").get_public_url(fname)
                    supabase.table("users").insert({"username": u_name, "profile_pic": p_url}).execute()
                    st.session_state.user = u_name
                    st.session_state.pic = p_url
                    st.rerun()
else:
    st.sidebar.image(st.session_state.pic, width=100)
    st.sidebar.success(f"Profile: {st.session_state.user}")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

tab = st.sidebar.radio("Navigation", ["🌍 World Feed", "📤 Upload Video"])

# ৭. মেইন ফিড
if tab == "🌍 World Feed":
    try:
        res = supabase.table("videos").select("*").execute()
        data = res.data if res.data else []
        random.shuffle(data)
        for index, v in enumerate(data):
            v_id = v['id']
            st.markdown('<div class="video-card">', unsafe_allow_html=True)
            st.markdown(f'<div style="display:flex; align-items:center; margin-bottom:15px;"><img src="{v.get("uploader_pic", "")}" class="user-avatar"><span class="username-text">{v.get("uploader_name", "BT User")}</span></div>', unsafe_allow_html=True)
            st.video(v['video_url'])
            
            try: supabase.table("videos").update({"views": v.get("views", 0) + 1}).eq("id", v_id).execute()
            except: pass

            st.markdown(f'<div style="margin: 12px 0;"><span class="stat-box">👁️ {format_value(v.get("views", 0)+1)} Views</span><span class="stat-box">❤️ {format_value(v.get("likes", 0))} Likes</span><span class="stat-box">👤 {format_value(v.get("followers", 0))} Followers</span></div>', unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button(f"❤️ Like", key=f"l_{v_id}"):
                    supabase.table("videos").update({"likes": v.get("likes", 0) + 1}).eq("id", v_id).execute(); st.rerun()
            with c2:
                if st.button(f"➕ Follow", key=f"f_{v_id}"):
                    supabase.table("videos").update({"followers": v.get("followers", 0) + 1}).eq("id", v_id).execute(); st.rerun()

            st.markdown(f'<a href="https://www.profitablecpmratenetwork.com/tgt6azn6?key=e753cbd6d9bae06d67051ed846419521" target="_blank" class="btn-reward">💎 Claim Diamond Reward</a>', unsafe_allow_html=True)
            st.components.v1.html("""<div style="text-align:center;"><script type="text/javascript">atOptions = { 'key' : '342950879f2064f7255ad047622381c8', 'format' : 'iframe', 'height' : 50, 'width' : 320, 'params' : {} };</script><script src="https://www.highperformanceformat.com/342950879f2064f7255ad047622381c8/invoke.js"></script></div>""", height=65)
            st.markdown('</div>', unsafe_allow_html=True)

            if (index + 1) % 2 == 0:
                st.markdown(f'<div class="big-ad-box"><p style="color:#00ff00; font-size:18px; font-weight:bold;">🔥 BIG REWARD WAITING 🔥</p><a href="https://www.profitablecpmratenetwork.com/a68pzvy9g?key=ff79dfacf59be49e36f413f0f2e76766" target="_blank" style="background:#ed1c24; color:white; padding:12px 35px; border-radius:30px; text-decoration:none; font-weight:bold; display:inline-block; margin-top:10px;">CLICK FOR BIG AD REWARD</a></div>', unsafe_allow_html=True)
    except: st.error("Syncing Feed...")

# ৮. ভিডিও আপলোড
elif tab == "📤 Upload Video":
    if st.session_state.user:
        v_file = st.file_uploader("Select MP4", type=['mp4'])
        if st.button("🚀 Publish") and v_file:
            with st.spinner("🤖 পাবলিশ হচ্ছে..."):
                try:
                    v_uuid = f"v_{uuid.uuid4()}.mp4"
                    supabase.storage.from_("videos").upload(path=v_uuid, file=v_file.getvalue())
                    v_url = supabase.storage.from_("videos").get_public_url(v_uuid)
                    supabase.table("videos").insert({"video_url": v_url, "uploader_name": st.session_state.user, "uploader_pic": st.session_state.pic, "likes": 0, "followers": 0, "views": 0}).execute()
                    st.success("✅ সোহেল ভাই, সব লাইভ হয়েছে!")
                except: st.error("Try again later.")
