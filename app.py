import streamlit as st
from supabase import create_client
import uuid
import random
import os
import subprocess
from datetime import datetime
import streamlit.components.v1 as components

# ১. আগের হেড সেকশন ও ভেরিফিকেশন (ঠিক আছে)
st.markdown(
    f"""
    <head>
        <meta name="msvalidate.01" content="e776b8ce73ea3dcc07551e8a021a0907">
        <meta name="monetag" content="5cc1b7ba5cb29eff802ce49009f87e2b">
    </head>
    """,
    unsafe_allow_html=True
)

SMART_LINK = "https://omg10.com/4/10954816"

def show_auto_moving_banner():
    ad_html = f"""
    <div style="text-align:center; margin: 10px 0;">
        <a href="{SMART_LINK}" target="_blank" style="text-decoration:none;">
            <div style="background: linear-gradient(90deg, #00ff00, #000); 
                        color: #fff; padding: 15px; border-radius: 10px; 
                        border: 2px solid #00ff00; font-family: sans-serif;
                        box-shadow: 0 0 20px #00ff00; transition: 0.3s;">
                <span style="font-size: 18px; font-weight: bold;">⚡ PREMIUM REWARD ACTIVE ⚡</span><br>
                <span style="font-size: 12px; color: #00ff00;">Click to Claim Your Diamond Bonus!</span>
            </div>
        </a>
    </div>
    """
    components.html(ad_html, height=120)

# ২. সুপাবেস কানেকশন ও স্টোরেজ লজিক (সব আপনার অরিজিনাল ডাটা)
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

# ৩. ফরমেট ও ক্লিনআপ (আগের লজিক ঠিক আছে)
def format_value(value):
    if value >= 1000: return f"{value/1000:.1f}K"
    return str(value)

def auto_cleanup(target_storage_url):
    res = supabase.table("videos").select("id", "video_url").like("video_url", f"%{target_storage_url}%").order("created_at", desc=False).execute()
    if len(res.data) >= 500:
        old = res.data[0]
        v_url = old['video_url']
        v_name = v_url.split('/')[-1]
        for s in STORAGE_KEYS:
            if s['url'] in v_url:
                try: create_client(s['url'], s['key']).storage.from_("videos").remove([v_name])
                except: pass
        supabase.table("videos").delete().eq("id", old['id']).execute()

# ৪. স্টাইল (সাদা-কালো মডার্ন ডিজাইন)
st.markdown("""
    <style>
    .stApp { background-color: #f0f2f5; color: #000; }
    .post-card { background: #fff; border-radius: 12px; padding: 20px; margin-bottom: 20px; border: 1px solid #ddd; box-shadow: 0 1px 2px rgba(0,0,0,0.1); }
    .user-avatar { width: 45px; height: 45px; border-radius: 50%; border: 1px solid #ddd; object-fit: cover; margin-right: 12px; }
    .stat-box { font-size: 13px; color: #65676b; font-weight: bold; margin-right: 15px; }
    .btn-direct { display: block; width: 100%; padding: 8px; margin: 5px 0; color: white !important; text-align: center; border-radius: 5px; font-weight: bold; text-decoration: none; font-size: 13px; }
    .bg-1 { background: #FF416C; } .bg-2 { background: #1DE9B6; } .bg-3 { background: #667eea; } .bg-4 { background: #f6d365; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ BT AI book")

# ৫. লগইন (আগের লজিক)
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
            u_pic = st.sidebar.file_uploader("Upload Profile Photo", type=['jpg', 'png'])
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

# মেনু ট্যাব
tab = st.sidebar.radio("Menu", ["🌍 World Feed", "📤 Upload Post"])

# ৬. ফিড (ভিডিও এবং ফেসবুক স্টাইল পোস্ট দুটাই দেখাবে)
if tab == "🌍 World Feed":
    try:
        res = supabase.table("videos").select("*").order("created_at", desc=True).execute()
        data = res.data if res.data else []
        for v in data:
            v_id = v['id']
            st.markdown('<div class="post-card">', unsafe_allow_html=True)
            st.markdown(f'<div style="display:flex; align-items:center; margin-bottom:12px;"><img src="{v.get("uploader_pic", "")}" class="user-avatar"><b>{v.get("uploader_name")}</b></div>', unsafe_allow_html=True)
            
            # লজিক: ভিডিও থাকলে ভিডিও দেখাবে, টেক্সট থাকলে টেক্সট
            if v.get('video_url'):
                if v['video_url'].endswith('.mp4'):
                    st.video(v['video_url'])
                else: # যদি এটা শুধু ছবি বা পোস্ট হয়
                    st.write(v.get('post_text', ''))
                    if v['video_url'].startswith('http'): st.image(v['video_url'])

            show_auto_moving_banner()
            st.markdown(f'''
                <div style="margin: 10px 0;">
                    <span class="stat-box">👁️ {format_value(v.get("views", 0))} Views</span>
                    <span class="stat-box">❤️ {format_value(v.get("likes", 0))} Likes</span>
                </div>
            ''', unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button(f"❤️ Like", key=f"lk_{v_id}"):
                    supabase.table("videos").update({"likes": v.get("likes", 0) + 1}).eq("id", v_id).execute()
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    except: st.error("Feed Error")

# ৭. নতুন পোস্টিং লজিক (আগের ভিডিও আপলোড ঠিক রেখে)
elif tab == "📤 Upload Post":
    if not st.session_state.user: st.warning("Login first!")
    else:
        post_type = st.selectbox("কি আপলোড করবেন?", ["ভিডিও (Shorts)", "ছবি/টেক্সট (Facebook Style)"])
        
        if post_type == "ভিডিও (Shorts)":
            file = st.file_uploader("Select Video", type=['mp4'])
            if st.button("🚀 Publish Video") and file:
                # আপনার আগের সেই ffmpeg এবং স্টোরেজ লজিক
                with st.spinner("Processing Video..."):
                    target = random.choice(STORAGE_KEYS)
                    auto_cleanup(target['url'])
                    t_in, t_out = "raw.mp4", "final.mp4"
                    with open(t_in, "wb") as f: f.write(file.getvalue())
                    cmd = f'ffmpeg -i {t_in} -t 15 -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -vcodec libx264 -fs 1.9M -y {t_out}'
                    subprocess.run(cmd, shell=True)
                    s_bot = create_client(target['url'], target['key'])
                    v_name = f"v_{uuid.uuid4()}.mp4"
                    with open(t_out, "rb") as f: s_bot.storage.from_("videos").upload(v_name, f.read())
                    v_url = s_bot.storage.from_("videos").get_public_url(v_name)
                    supabase.table("videos").insert({
                        "video_url": v_url, "uploader_name": st.session_state.user,
                        "uploader_pic": st.session_state.pic, "likes": 0, "views": 0
                    }).execute()
                    st.success("Video Published!")
                    os.remove(t_in); os.remove(t_out); st.rerun()

        else: # ফেসবুক স্টাইল পোস্টিং
            post_txt = st.text_area("আপনার মনের কথা লিখুন...")
            post_img = st.file_uploader("ছবি যোগ করুন (ঐচ্ছিক)", type=['jpg', 'png'])
            if st.button("📢 Post Now"):
                with st.spinner("Posting..."):
                    img_url = ""
                    if post_img:
                        img_name = f"img_{uuid.uuid4()}.jpg"
                        supabase.storage.from_("videos").upload(img_name, post_img.getvalue())
                        img_url = supabase.storage.from_("videos").get_public_url(img_name)
                    
                    # ডাটাবেসে ভিডিও ইউআরএল এর জায়গায় ছবির ইউআরএল যাবে
                    supabase.table("videos").insert({
                        "video_url": img_url, "post_text": post_txt,
                        "uploader_name": st.session_state.user,
                        "uploader_pic": st.session_state.pic, "likes": 0, "views": 0
                    }).execute()
                    st.success("Post Shared!")
                    st.rerun()
