import streamlit as st
from supabase import create_client
import uuid
import random
import os
import subprocess
from datetime import datetime
import streamlit.components.v1 as components

# ১. মাইক্রোসফট বিং ভেরিফিকেশন (এটি ভেতরেই থাকল)
st.markdown(
    f"""
    <script>
        var meta = document.createElement('meta');
        meta.name = "msvalidate.01";
        meta.content = "8D0CF51CA6DBABB744B29B8B6DE6925C";
        document.getElementsByTagName('head')[0].appendChild(meta);
    </script>
    """,
    unsafe_allow_html=True
)

# ২. সুপাবেস কানেকশন (আপনার অরিজিনাল ডাটা)
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

STORAGE_KEYS = [
    {"url": "https://wzwhcuifcdkhjkvhndcp.supabase.co", "key": "sb_secret_bt9SDKvRqm9J91cZD-MAkw_caf0Gnkh"},
    {"url": "https://fypvwatkffekksbceofu.supabase.co", "key": "sb_secret_JeRIhaN33UZe9nTKgfMzwQ_Kc5rHL8o"},
    {"url": "https://osdjwtywivieuetnhxyo.supabase.co", "key": "sb_secret_ffiZGQ8XSUdAWXa26Ut2ww_-dVCfJy4"},
    {"url": "https://fiqjddgdpirdpbaccynt.supabase.co", "key": "sb_secret_kKfsUaR3Eyxp-W-ZLQYftg_9THDBB3C"},
    {"url": "https://ebkpbdjfeabqfwbkgvrg.supabase.co", "key": "sb_secret_HuxmaOONEyvFBqDB2yH_IQ_OcC6Pm4b"},
    {"url": "https://xjquucfkndfzawjscmdb.supabase.co", "key": "sb_secret_dRBwgkxRhwLwwYLSU92VBw_NUKkyX32"},
    {"url": "https://ziliihcgqsxnttrtupgm.supabase.co", "key": "sb_secret_GyhZd_60lAW6np0uBNjuBA_amZpgwUl"},
    {"url": "https://optlxxgrdmrvvkzwkmui.supabase.co", "key": "sb_secret_aKImpLhPtUkF3ggXgDKGRw_BJC7Qd_M"},
    {"url": "https://owlhzlgegmezedskzwgl.supabase.co", "key": "sb_secret_wOMZKz1TtugQNXFYgV4d4g_K82EnAl1"},
    {"url": "https://bczxwfclimiaaljjfegq.supabase.co", "key": "sb_secret_7rFR003t7a_N_VIEbf7aAw_WfPL7xRs"},
]

st.set_page_config(page_title="BT AI book", layout="wide")

# ৩. ফরম্যাট ও অটো ক্লিনআপ
def format_value(value):
    if value >= 1000: return f"{value/1000:.1f}K"
    return str(value)

# ৪. আপনার সেই হাই-কোয়ালিটি স্টাইল ও লাইট ডিজাইন
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    
    /* ভিডিও কার্ড ডিজাইন ও লাইট শ্যাডো */
    .video-card { 
        background: #0d0d0d; 
        border: 1px solid #333; 
        border-radius: 15px; 
        padding: 15px; 
        margin-bottom: 25px; 
        box-shadow: 0 0 15px rgba(0, 255, 0, 0.2);
    }
    
    .user-avatar { width: 50px; height: 50px; border-radius: 50%; border: 2px solid #00ff00; object-fit: cover; margin-right: 12px; }
    .stat-box { font-size: 14px; color: #00ff00; font-weight: bold; margin-right: 15px; }
    
    /* আপনার সেই লাকঝারি বাটনগুলো */
    .btn-direct { 
        display: block; 
        width: 100%; 
        padding: 12px; 
        margin: 8px 0; 
        color: white !important; 
        text-align: center; 
        border-radius: 10px; 
        font-weight: bold; 
        text-decoration: none; 
        font-size: 16px; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.5); 
        transition: 0.3s;
    }
    .bg-1 { background: linear-gradient(45deg, #FF416C, #FF4B2B); border: 1px solid #ff416c; }
    .bg-2 { background: linear-gradient(45deg, #1DE9B6, #26A69A); border: 1px solid #1de9b6; }
    .bg-3 { background: linear-gradient(45deg, #667eea, #764ba2); border: 1px solid #667eea; }
    .bg-4 { background: linear-gradient(45deg, #f6d365, #fda085); border: 1px solid #f6d365; }
    
    /* রিওয়ার্ড বক্সের গ্লোয়িং এনিমেশন */
    .banner-box { 
        background: #1a1a1a; 
        border: 2px dashed #ed1c24; 
        padding: 15px; 
        text-align: center; 
        border-radius: 12px; 
        margin: 20px 0; 
        animation: glow 1.5s infinite alternate; 
    }
    @keyframes glow { 
        from { box-shadow: 0 0 5px #ed1c24; } 
        to { box-shadow: 0 0 20px #ed1c24; } 
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ BT AI book")

# ৫. লগইন সিস্টেম (আগের মতোই)
if 'user' not in st.session_state:
    st.session_state.user = None
    st.session_state.pic = None

if not st.session_state.user:
    u_name = st.sidebar.text_input("Name")
    if u_name:
        user_data = supabase.table("users").select("*").eq("username", u_name).execute()
        if user_data.data:
            if st.sidebar.button("Login"):
                st.session_state.user = u_name
                st.session_state.pic = user_data.data[0]['profile_pic']
                st.rerun()
        else:
            u_pic = st.sidebar.file_uploader("Upload Photo", type=['jpg', 'png', 'jpeg'])
            if st.sidebar.button("Join Now"):
                if u_name and u_pic:
                    fname = f"p_{uuid.uuid4()}.jpg"
                    supabase.storage.from_("videos").upload(path=fname, file=u_pic.getvalue())
                    p_url = supabase.storage.from_("videos").get_public_url(fname)
                    supabase.table("users").insert({"username": u_name, "profile_pic": p_url}).execute()
                    st.session_state.user = u_name
                    st.session_state.pic = p_url
                    st.rerun()
else:
    st.sidebar.image(st.session_state.pic, width=80)
    st.sidebar.write(f"Hello, {st.session_state.user}")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

tab = st.sidebar.radio("Menu", ["🌍 World Feed", "📤 Upload Video"])

# ৬. মেইন ফিড (রঙিন বাটন ও ডিজাইন সহ)
if tab == "🌍 World Feed":
    try:
        res = supabase.table("videos").select("*").execute()
        data = res.data if res.data else []
        random.shuffle(data)
        for index, v in enumerate(data):
            v_id = v['id']
            st.markdown('<div class="video-card">', unsafe_allow_html=True)
            st.markdown(f'<div style="display:flex; align-items:center; margin-bottom:12px;"><img src="{v.get("uploader_pic", "")}" class="user-avatar"><b>{v.get("uploader_name")}</b></div>', unsafe_allow_html=True)
            st.video(v['video_url'])
            
            # আপনার সেই আকর্ষণীয় বাটনসমূহ
            st.markdown(f'''
                <div class="banner-box">
                    <a href="https://www.profitablecpmratenetwork.com/a68pzvy9g?key=ff79dfacf59be49e36f413f0f2e76766" target="_blank" 
                       style="background:#ed1c24; color:white; padding:10px 25px; border-radius:8px; text-decoration:none; font-weight:bold; font-size:18px;">Click to Win Reward 🎁</a>
                </div>
                <div style="margin: 10px 0;">
                    <span class="stat-box">👁️ {format_value(v.get("views", 0))} Views</span>
                    <span class="stat-box">❤️ {format_value(v.get("likes", 0))} Likes</span>
                    <span class="stat-box">👤 {format_value(v.get("followers", 0))} Followers</span>
                </div>
                <a href="https://www.profitablecpmratenetwork.com/krgreepsz8?key=08a0fdc6d7ed4f33a60d1f4910ec27c5" target="_blank" class="btn-direct bg-1">💰 High CPC Reward 1</a>
                <a href="https://www.profitablecpmratenetwork.com/tgt6azn6?key=e753cbd6d9bae06d67051ed846419521" target="_blank" class="btn-direct bg-2">💎 Premium Bonus 2</a>
                <a href="https://www.profitablecpmratenetwork.com/cq47z3azy?key=89e1a9a3fcee8e90a78f858e32718ec4" target="_blank" class="btn-direct bg-3">🚀 Mega Earning 3</a>
            ''', unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button(f"❤️ Like", key=f"lk_{v_id}"):
                    supabase.table("videos").update({"likes": v.get("likes", 0) + 1}).eq("id", v_id).execute()
                    st.rerun()
            with c2:
                if st.button(f"➕ Follow", key=f"fl_{v_id}"):
                    supabase.table("videos").update({"followers": v.get("followers", 0) + 1}).eq("id", v_id).execute()
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    except: st.error("Feed Error")

# ৭. ভিডিও আপলোড
elif tab == "📤 Upload Video":
    # আপনার আপলোড কোড এখানে আগের মতোই আছে...
    if not st.session_state.user: st.warning("Login first!")
    else:
        file = st.file_uploader("Select Video", type=['mp4'])
        if st.button("🚀 Publish Video") and file:
            with st.spinner("Publishing..."):
                target = random.choice(STORAGE_KEYS)
                t_in = "raw.mp4"
                with open(t_in, "wb") as f: f.write(file.getvalue())
                s_bot = create_client(target['url'], target['key'])
                v_name = f"v_{uuid.uuid4()}.mp4"
                with open(t_in, "rb") as f: s_bot.storage.from_("videos").upload(v_name, f.read())
                v_url = s_bot.storage.from_("videos").get_public_url(v_name)
                supabase.table("videos").insert({
                    "video_url": v_url, "uploader_name": st.session_state.user,
                    "uploader_pic": st.session_state.pic, "likes": random.randint(20, 50), 
                    "views": random.randint(850, 1200), "followers": random.randint(100, 150)
                }).execute()
                st.success("Published!")
                os.remove(t_in)
                st.rerun()
