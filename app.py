import streamlit as st
from supabase import create_client
import uuid
import random
import os
import subprocess
from datetime import datetime

# --- [জংশন বক্স] ---
MAIN_URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
MAIN_KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(MAIN_URL, MAIN_KEY)

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

st.set_page_config(page_title="BT AI book", layout="centered")

# --- ডিজাইন (CSS) ---
st.markdown("""
<style>
    .stApp { background-color: #000; color: #fff; }
    .video-card { background: #111; border-radius: 15px; padding: 10px; margin-bottom: 20px; border: 1px solid #222; }
    .ad-banner { background: #222; height: 60px; border-radius: 5px; text-align: center; line-height: 60px; margin: 10px 0; color: #555; }
    .profile-header { display: flex; align-items: center; gap: 10px; margin-bottom: 10px; }
    .profile-pic { width: 40px; height: 40px; border-radius: 50%; border: 2px solid #00ff00; }
</style>
""", unsafe_allow_html=True)

if 'user' not in st.session_state: st.session_state.user = None

# --- ফাংশন ---
def auto_cleanup():
    res = supabase.table("videos").select("id", "video_url").order("created_at", desc=False).execute()
    if len(res.data) > 100:
        old = res.data[0]
        v_name = old['video_url'].split('/')[-1]
        for s in STORAGE_KEYS:
            if s['url'] in old['video_url']:
                try: create_client(s['url'], s['key']).storage.from_("videos").remove([v_name])
                except: pass
        supabase.table("videos").delete().eq("id", old['id']).execute()

# --- মেনু ---
tab = st.sidebar.radio("BT Menu", ["🌍 World Feed", "📤 Upload Video", "🔐 Profile"])

# --- ১. ওয়ার্ল্ড ফিড (ভিডিও দেখার জায়গা) ---
if tab == "🌍 World Feed":
    st.title("🛡️ BT AI book")
    
    # অ্যাড ব্যানার (উপরে)
    st.markdown('<div class="ad-banner">Your Google Ad Here</div>', unsafe_allow_html=True)
    
    res = supabase.table("videos").select("*").order("created_at", desc=True).execute()
    
    for v in res.data:
        with st.container():
            st.markdown(f'''
            <div class="video-card">
                <div class="profile-header">
                    <img src="{v['uploader_pic']}" class="profile-pic">
                    <b>{v['uploader_name']}</b>
                </div>
            </div>
            ''', unsafe_allow_html=True)
            
            st.video(v['video_url'])
            
            # লাইক ও ফলো সেকশন
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button(f"❤️ {v['likes']}", key=f"like_{v['id']}"):
                    supabase.table("videos").update({"likes": v['likes'] + 1}).eq("id", v['id']).execute()
                    st.rerun()
            with col2:
                st.write(f"👁️ {v['views']}")
            with col3:
                if st.button("➕ Follow", key=f"fol_{v['id']}"):
                    st.toast(f"Followed {v['uploader_name']}!")

# --- ২. ভিডিও আপলোড ---
elif tab == "📤 Upload Video":
    if not st.session_state.user:
        st.warning("Please login first!")
    else:
        file = st.file_uploader("Select Video", type=['mp4'])
        if st.button("🚀 Publish") and file:
            with st.spinner("Processing..."):
                auto_cleanup()
                t_in, t_out = "in.mp4", "out.mp4"
                with open(t_in, "wb") as f: f.write(file.getvalue())
                
                # কম্প্রেস এবং ফিক্সড কোড
                subprocess.run(f"ffmpeg -i {t_in} -t 15 -vf scale=-2:720 -vcodec libx264 -crf 28 -fs 2M -y {t_out}", shell=True)
                
                target = random.choice(STORAGE_KEYS)
                s_bot = create_client(target['url'], target['key'])
                v_name = f"v_{uuid.uuid4()}.mp4"
                
                with open(t_out, "rb") as f:
                    s_bot.storage.from_("videos").upload(v_name, f.read())
                
                v_url = s_bot.storage.from_("videos").get_public_url(v_name)
                
                supabase.table("videos").insert({
                    "video_url": v_url,
                    "uploader_name": st.session_state.user,
                    "uploader_pic": st.session_state.pic,
                    "likes": random.randint(1, 10),
                    "views": random.randint(10, 100)
                }).execute()
                st.success("Published!")
                os.remove(t_in); os.remove(t_out)
                st.rerun()

# --- ৩. প্রোফাইল ---
elif tab == "🔐 Profile":
    if not st.session_state.user:
        u_name = st.text_input("Username")
        u_pass = st.text_input("Password", type="password")
        if st.button("Login"):
            res = supabase.table("users").select("*").eq("username", u_name).eq("password", u_pass).execute()
            if res.data:
                st.session_state.user = u_name
                st.session_state.pic = res.data[0]['profile_pic']
                st.rerun()
    else:
        st.image(st.session_state.pic, width=100)
        st.write(f"Logged in as: {st.session_state.user}")
        if st.button("Logout"):
            st.session_state.user = None
            st.rerun()
