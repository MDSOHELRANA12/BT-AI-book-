import streamlit as st
from supabase import create_client
import uuid
import random
import os
import pickle
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# ১. আপনার শক্তিশালী সুপাবেস কানেকশন
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

# ২. আপনার সেই অরিজিনাল দুইটি ইউটিউব চ্যানেল
CHANNELS = {
    "চ্যানেল ১": {
        "client_id": "1052502665296-cv7c3jjq4g6to426uriib7ei9le1tl7j.apps.googleusercontent.com",
        "client_secret": "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",
        "token_file": "token1.pickle"
    },
    "চ্যানেল ২": {
        "client_id": "681450003814-j2fc889ei0gj0cfog625ibpg15bflcur.apps.googleusercontent.com",
        "client_secret": "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",
        "token_file": "token2.pickle"
    }
}

# ৩. ইউটিউব সার্ভিস (গ্লোবাল ইউজারদের জন্য ফিক্সড)
def get_yt_service(ch_name):
    ch = CHANNELS[ch_name]
    creds = None
    if os.path.exists(ch['token_file']):
        with open(ch['token_file'], 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            config = {"web": {"client_id": ch['client_id'], "client_secret": ch['client_secret'], "auth_uri": "https://accounts.google.com/o/oauth2/auth", "token_uri": "https://oauth2.googleapis.com/token"}}
            flow = InstalledAppFlow.from_client_config(config, ['https://www.googleapis.com/auth/youtube.upload'], redirect_uri='urn:ietf:wg:oauth:2.0:oob')
            auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
            st.warning("Authorize this app to upload globally:")
            st.markdown(f"🔗 [Get Google Code]({auth_url})")
            auth_code = st.text_input("Enter Verification Code:", key=f"auth_{ch_name}")
            if auth_code:
                flow.fetch_token(code=auth_code)
                creds = flow.credentials
                with open(ch['token_file'], 'wb') as token:
                    pickle.dump(creds, token)
            else: st.stop()
    return build('youtube', 'v3', credentials=creds)

st.set_page_config(page_title="BT AI book | Sohel Rana", layout="wide")

# ৪. গ্লোবাল ডিজাইন স্টাইল (ভিডিওর নিচে বড় বড় ভিউ ও বাটন)
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .video-card { background: #0d0d0d; border: 2px solid #ed1c24; border-radius: 20px; padding: 25px; margin-bottom: 45px; box-shadow: 0 0 25px rgba(237, 28, 36, 0.5); }
    .user-header { display: flex; align-items: center; margin-bottom: 20px; }
    .user-avatar { width: 70px; height: 70px; border-radius: 50%; border: 3px solid #00ff00; margin-right: 15px; }
    .global-stat { font-size: 26px; color: #00ff00; font-weight: bold; margin-right: 35px; text-shadow: 2px 2px #000; }
    .btn-global-reward { display: block; width: 100%; padding: 22px; background: linear-gradient(90deg, #ed1c24, #ff0000, #aa0000); color: white !important; text-align: center; border-radius: 15px; font-weight: bold; text-decoration: none; font-size: 24px; margin-top: 30px; animation: pulse 2s infinite; }
    @keyframes pulse { 0% {transform: scale(1);} 50% {transform: scale(1.02);} 100% {transform: scale(1);} }
    .big-ad-box { background: #111; border: 5px dashed #00ff00; border-radius: 30px; padding: 60px; text-align: center; margin: 60px 0; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ BT AI book - The World's Power")

# ৫. সেশন ও অরিজিনাল লগইন
if 'user' not in st.session_state:
    st.session_state.user = None
    st.session_state.pic = None

# ৬. ভিডিও ফিড (যেখানে আপনার অরিজিনাল ভিউ আর লাইক ধামাকা দেখাবে)
tab = st.sidebar.radio("Navigation", ["🌏 World Feed", "📤 Upload Video"])

if tab == "🌏 World Feed":
    try:
        res = supabase.table("videos").select("*").execute()
        v_list = res.data if res.data else []
        random.shuffle(v_list)

        for i, v in enumerate(v_list):
            st.markdown('<div class="video-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="user-header"><img src="{v.get("uploader_pic", "")}" class="user-avatar"><div style="font-size:24px; font-weight:bold;">{v.get("uploader_name", "Sohel Rana")}</div></div>', unsafe_allow_html=True)
            
            # আপনার ভিডিও রান করার মেইন পার্ট
            st.video(v['video_url'])
            
            # আপনার সেই কাঙ্ক্ষিত বড় বড় স্ট্যাটাস
            st.markdown(f'''
                <div style="margin: 30px 0;">
                    <span class="global-stat">👁️ {v.get("views", 25000)} Views</span>
                    <span class="global-stat">❤️ {v.get("likes", 5000)} Likes</span>
                    <span class="global-stat">👤 {v.get("followers", 5000)} Followers</span>
                </div>
            ''', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"🔥 Like", key=f"lk_{v['id']}"):
                    supabase.table("videos").update({"likes": v.get("likes", 0) + 1}).eq("id", v['id']).execute(); st.rerun()
            with col2:
                if st.button(f"🚀 Follow", key=f"fw_{v['id']}"):
                    supabase.table("videos").update({"followers": v.get("followers", 0) + 1}).eq("id", v['id']).execute(); st.rerun()

            st.markdown(f'<a href="https://www.profitablecpmratenetwork.com/tgt6azn6?key=e753cbd6d9bae06d67051ed846419521" target="_blank" class="btn-global-reward">💎 CLAIM WORLD REWARD: 10,000 DIAMONDS</a>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # প্রতি ২ ভিডিওর পর মেইন গ্লোবাল অ্যাড বক্স
            if (i + 1) % 2 == 0:
                st.markdown(f'''
                    <div class="big-ad-box">
                        <h1 style="color:#ed1c24; font-size:40px;">💰 MEGA GLOBAL BONUS 💰</h1>
                        <p style="font-size:28px; color:#fff;">Click below to boost your earnings across the world!</p>
                        <a href="https://www.profitablecpmratenetwork.com/a68pzvy9g?key=ff79dfacf59be49e36f413f0f2e76766" target="_blank" style="background:#00ff00; color:black; padding:30px 80px; border-radius:60px; text-decoration:none; font-weight:bold; display:inline-block; margin-top:35px; font-size:30px;">GET GLOBAL REWARD</a>
                    </div>
                ''', unsafe_allow_html=True)
    except: st.error("World Server Syncing...")

# ৭. আপলোড (সবকিছু সেট করে দিয়েছি)
elif tab == "📤 Upload Video":
    v_title = st.text_input("ভিডিও টাইটেল (সারা বিশ্বের মানুষ দেখবে)")
    target_ch = st.selectbox("Select Youtube Channel", ["চ্যানেল ১", "চ্যানেল ২"])
    v_file = st.file_uploader("Upload MP4 File", type=['mp4'])
    
    if st.button("🚀 Publish To World") and v_file:
        with st.spinner("Publishing Global Feed..."):
            try:
                yt = get_yt_service(target_ch)
                request = yt.videos().insert(
                    part="snippet,status",
                    body={"snippet": {"title": v_title}, "status": {"privacyStatus": "public"}},
                    media_body=MediaIoBaseUpload(v_file, mimetype='video/mp4', resumable=True)
                )
                response = request.execute()
                v_url = f"https://www.youtube.com/watch?v={response['id']}"
                
                supabase.table("videos").insert({
                    "video_url": v_url, "uploader_name": st.session_state.user if st.session_state.user else "Sohel Rana", 
                    "uploader_pic": st.session_state.pic, "likes": 5000, "followers": 5000, "views": 25000
                }).execute()
                st.success("✅ Your Video is now LIVE Worldwide!")
            except Exception as e: st.error(f"Global Error: {e}")
