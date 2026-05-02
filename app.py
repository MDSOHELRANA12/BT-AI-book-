import streamlit as st
from supabase import create_client
import uuid
import random
import os
import subprocess
from datetime import datetime
import streamlit.components.v1 as components

# ১. সুপাবেস কানেকশন (মাস্টার কন্ট্রোল)
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

# ২. অটো ক্লিনআপ (১০০ ভিডিও লিমিট)
def auto_cleanup():
    res = supabase.table("videos").select("id", "video_url").order("created_at", desc=False).execute()
    if len(res.data) >= 100:
        old = res.data[0]
        v_url = old['video_url']
        v_name = v_url.split('/')[-1]
        for s in STORAGE_KEYS:
            if s['url'] in v_url:
                try: create_client(s['url'], s['key']).storage.from_("videos").remove([v_name])
                except: pass
        supabase.table("videos").delete().eq("id", old['id']).execute()

# ৩. অরিজিনাল ডিজাইন ও কাঠামো (জিরো ফিগার সেটিং)
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .video-card { 
        background: #0d0d0d; border: 1px solid #333; border-radius: 15px; 
        padding: 15px; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    .user-avatar { 
        width: 50px; height: 50px; border-radius: 50%; 
        border: 2px solid #00ff00; object-fit: cover; margin-right: 12px; 
    }
    .stat-box { font-size: 14px; color: #00ff00; font-weight: bold; margin-right: 15px; }
    
    /* অ্যাড বাটন স্টাইল */
    .btn-direct { 
        display: block; width: 100%; padding: 10px; margin: 5px 0; 
        color: white !important; text-align: center; border-radius: 8px; 
        font-weight: bold; text-decoration: none; font-size: 14px;
    }
    .bg-1 { background: linear-gradient(135deg, #FF416C, #FF4B2B); }
    .bg-2 { background: linear-gradient(135deg, #1DE9B6, #26A69A); }
    .bg-3 { background: linear-gradient(135deg, #667eea, #764ba2); }
    .bg-4 { background: linear-gradient(135deg, #f6d365, #fda085); }
    
    /* ব্যানার অ্যাড বিকল্প (কালো দাগ দূর করতে) */
    .banner-box {
        background: #1a1a1a; border: 1px dashed #ed1c24;
        padding: 15px; text-align: center; border-radius: 10px; margin: 15px 0;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ BT AI book")

# ৪. লগইন সিস্টেম (আপনার অরিজিনাল কাঠামো)
if 'user' not in st.session_state:
    st.session_state.user = None
    st.session_state.pic = None

if not st.session_state.user:
    u_name = st.sidebar.text_input("Username")
    if u_name:
        user_data = supabase.table("users").select("*").eq("username", u_name).execute()
        if user_data.data:
            if st.sidebar.button("Login"):
                st.session_state.user = u_name
                st.session_state.pic = user_data.data[0]['profile_pic']
                st.rerun()
        else:
            u_pic = st.sidebar.file_uploader("Upload Profile Pic", type=['jpg', 'png', 'jpeg'])
            if st.sidebar.button("Register"):
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
    st.sidebar.write(f"Logged in: {st.session_state.user}")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

tab = st.sidebar.radio("BT Menu", ["🌍 World Feed", "📤 Upload Video"])

# ৫. মেইন ফিড (কালো গ্যাপ ফিক্সড)
if tab == "🌍 World Feed":
    try:
        res = supabase.table("videos").select("*").execute()
        data = res.data if res.data else []
        random.shuffle(data)

        for index, v in enumerate(data):
            st.markdown('<div class="video-card">', unsafe_allow_html=True)
            # ইউজার প্রোফাইল ছবি ও নাম
            st.markdown(f'<div style="display:flex; align-items:center; margin-bottom:12px;"><img src="{v.get("uploader_pic", "")}" class="user-avatar"><b>{v.get("uploader_name", "BT User")}</b></div>', unsafe_allow_html=True)
            
            # ভিডিও প্লেয়ার
            st.video(v['video_url'])
            
            # কালো গ্যাপের জায়গায় "ব্যানার অ্যাড বাটন" (আপনার দেওয়া নতুন লিঙ্ক)
            st.markdown(f'''
                <div class="banner-box">
                    <p style="color:#aaa; font-size:12px; margin-bottom:5px;">Sponsored Ad</p>
                    <a href="https://www.profitablecpmratenetwork.com/a68pzvy9g?key=ff79dfacf59be49e36f413f0f2e76766" target="_blank" 
                       style="background:#ed1c24; color:white; padding:8px 20px; border-radius:5px; text-decoration:none; font-weight:bold;">
                       Click to Win Reward 🎁
                    </a>
                </div>
            ''', unsafe_allow_html=True)

            # স্ট্যাটাস ও বাকি ৪টি বাটন
            st.markdown(f'''
                <div style="margin: 10px 0;">
                    <span class="stat-box">👁️ {v.get("views", 0)} Views</span>
                    <span class="stat-box">❤️ {v.get("likes", 0)} Likes</span>
                </div>
                <a href="https://www.profitablecpmratenetwork.com/krgreepsz8?key=08a0fdc6d7ed4f33a60d1f4910ec27c5" target="_blank" class="btn-direct bg-1">💰 High CPC Reward 1</a>
                <a href="https://www.profitablecpmratenetwork.com/tgt6azn6?key=e753cbd6d9bae06d67051ed846419521" target="_blank" class="btn-direct bg-2">💎 Premium Bonus 2</a>
                <a href="https://www.profitablecpmratenetwork.com/cq47z3azy?key=89e1a9a3fcee8e90a78f858e32718ec4" target="_blank" class="btn-direct bg-3">🚀 Mega Earning 3</a>
                <a href="https://www.profitablecpmratenetwork.com/et1vapu9bt?key=fa5bc3d78e5b5dbd9f470c2249c4180b" target="_blank" class="btn-direct bg-4">🎁 Special Gift 4</a>
            ''', unsafe_allow_html=True)
            
            # লাইক ও ফলো বাটন
            c1, c2 = st.columns(2)
            with c1:
                if st.button(f"❤️ Like", key=f"lk_{index}"):
                    supabase.table("videos").update({"likes": v.get("likes", 0) + 1}).eq("id", v['id']).execute()
                    st.rerun()
            with c2:
                if st.button(f"➕ Follow", key=f"fl_{index}"):
                    supabase.table("videos").update({"followers": v.get("followers", 0) + 1}).eq("id", v['id']).execute()
                    st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)
    except:
        st.error("Feed Error")

# ৬. ভিডিও আপলোড (১৫ সেকেন্ড, ৩ লিমিট এবং ২ এমবি)
elif tab == "📤 Upload Video":
    if not st.session_state.user:
        st.warning("Login first!")
    else:
        file = st.file_uploader("Select Video", type=['mp4'])
        if st.button("Publish") and file:
            with st.spinner("Processing..."):
                auto_cleanup()
                t_in, t_out = "raw.mp4", "final.mp4"
                with open(t_in, "wb") as f: f.write(file.getvalue())
                cmd = f'ffmpeg -i {t_in} -t 15 -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -vcodec libx264 -fs 1.9M -y {t_out}'
                subprocess.run(cmd, shell=True)
                
                target = random.choice(STORAGE_KEYS)
                s_bot = create_client(target['url'], target['key'])
                v_name = f"v_{uuid.uuid4()}.mp4"
                with open(t_out, "rb") as f: s_bot.storage.from_("videos").upload(v_name, f.read())
                
                v_url = s_bot.storage.from_("videos").get_public_url(v_name)
                supabase.table("videos").insert({
                    "video_url": v_url, "uploader_name": st.session_state.user,
                    "uploader_pic": st.session_state.pic, "likes": 0, "views": 0, "followers": 0
                }).execute()
                st.success("Done!")
                st.rerun()
