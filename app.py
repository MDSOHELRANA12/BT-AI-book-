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

# ১. সুপাবেস কানেকশন
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

# ২. আপনার সেই দুইটি ইউটিউব চ্যানেলের ডাটা
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

# ৩. ইউটিউব সার্ভিস (মোবাইল ফ্রেন্ডলি লিঙ্ক সিস্টেমসহ)
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
            st.warning("নিচের লিঙ্কে ক্লিক করে কোডটি নিয়ে আসুন:")
            st.markdown(f"🔗 [ভেরিফাই লিঙ্ক]({auth_url})")
            auth_code = st.text_input("ভেরিফিকেশন কোড এখানে দিন:", key=f"v_{ch_name}")
            if auth_code:
                flow.fetch_token(code=auth_code)
                creds = flow.credentials
                with open(ch['token_file'], 'wb') as token:
                    pickle.dump(creds, token)
            else:
                st.stop()
    return build('youtube', 'v3', credentials=creds)

st.set_page_config(page_title="BT AI book", layout="wide")

# ৪. আপনার অরিজিনাল ব্ল্যাক-রেড থিম ও ডিজাইন
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .video-card { background: #0d0d0d; border: 1px solid #333; border-radius: 20px; padding: 20px; margin-bottom: 30px; box-shadow: 0 10px 30px rgba(237, 28, 36, 0.2); }
    .user-info { display: flex; align-items: center; margin-bottom: 15px; }
    .user-avatar { width: 55px; height: 55px; border-radius: 50%; border: 2px solid #00ff00; object-fit: cover; margin-right: 15px; }
    .stat-text { font-size: 16px; color: #00ff00; font-weight: bold; margin-right: 20px; }
    .btn-reward { display: block; width: 100%; padding: 15px; margin-top: 15px; background: linear-gradient(135deg, #ed1c24, #aa0000); color: white !important; text-align: center; border-radius: 10px; font-weight: bold; text-decoration: none; font-size: 18px; }
    .big-ad-box { background: #1a1a1a; border: 3px dashed #ed1c24; border-radius: 20px; padding: 40px; text-align: center; margin: 40px 0; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ BT AI book - Official")

# ৫. আপনার অরিজিনাল সেশন ও লগইন সিস্টেম
if 'user' not in st.session_state:
    st.session_state.user = None
    st.session_state.pic = None

if not st.session_state.user:
    st.sidebar.header("🔐 User Login")
    u_name = st.sidebar.text_input("আপনার রেজিস্টার্ড নাম")
    if u_name:
        user_data = supabase.table("users").select("*").eq("username", u_name).execute()
        if user_data.data:
            if st.sidebar.button("লগইন করুন"):
                st.session_state.user = u_name
                st.session_state.pic = user_data.data[0]['profile_pic']
                st.rerun()
        else:
            u_pic = st.sidebar.file_uploader("আপনার প্রোফাইল ছবি", type=['jpg', 'png'])
            if st.sidebar.button("অ্যাকাউন্ট তৈরি করুন"):
                if u_name and u_pic:
                    fname = f"user_{uuid.uuid4()}.jpg"
                    supabase.storage.from_("videos").upload(path=fname, file=u_pic.getvalue())
                    p_url = supabase.storage.from_("videos").get_public_url(fname)
                    supabase.table("users").insert({"username": u_name, "profile_pic": p_url}).execute()
                    st.session_state.user = u_name; st.session_state.pic = p_url; st.rerun()

tab = st.sidebar.radio("Navigation", ["🌍 World Feed", "📤 Upload Video"])

# ৬. আপনার ফিড (লাইক, ফলো, ভিউ এবং অটো-অ্যাড সিস্টেম)
if tab == "🌍 World Feed":
    try:
        res = supabase.table("videos").select("*").execute()
        video_data = res.data if res.data else []
        random.shuffle(video_data)

        for index, v in enumerate(video_data):
            st.markdown('<div class="video-card">', unsafe_allow_html=True)
            st.markdown(f'''
                <div class="user-info">
                    <img src="{v.get("uploader_pic", "")}" class="user-avatar">
                    <div>
                        <span style="font-size:18px; font-weight:bold;">{v.get("uploader_name", "Unknown")}</span><br>
                        <span style="color:#888; font-size:12px;">Verified User</span>
                    </div>
                </div>
            ''', unsafe_allow_html=True)
            
            st.video(v['video_url'])
            
            # ভিউ কাউন্ট আপডেট
            if f"v_{v['id']}" not in st.session_state:
                supabase.table("videos").update({"views": v.get("views", 0) + 1}).eq("id", v['id']).execute()
                st.session_state[f"v_{v['id']}"] = True

            st.markdown(f'''
                <div style="margin: 15px 0;">
                    <span class="stat-text">👁️ {v.get("views", 0)} Views</span>
                    <span class="stat-text">❤️ {v.get("likes", 0)} Likes</span>
                    <span class="stat-text">👤 {v.get("followers", 0)} Followers</span>
                </div>
            ''', unsafe_allow_html=True)
            
            # বাটন লজিক
            c1, c2 = st.columns(2)
            with c1:
                if st.button(f"❤️ Like", key=f"l_{v['id']}"):
                    supabase.table("videos").update({"likes": v.get("likes", 0) + 1}).eq("id", v['id']).execute(); st.rerun()
            with c2:
                if st.button(f"➕ Follow", key=f"f_{v['id']}"):
                    supabase.table("videos").update({"followers": v.get("followers", 0) + 1}).eq("id", v['id']).execute(); st.rerun()

            st.markdown(f'<a href="https://www.profitablecpmratenetwork.com/tgt6azn6?key=e753cbd6d9bae06d67051ed846419521" target="_blank" class="btn-reward">💎 Claim Diamond Reward</a>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # দুইটি ভিডিওর পর একটি বড় ফরওয়ার্ড/অ্যাড বক্স
            if (index + 1) % 2 == 0:
                st.markdown(f'''
                    <div class="big-ad-box">
                        <h2 style="color:#ed1c24;">🔥 BIG REWARD WAITING 🔥</h2>
                        <p style="font-size:20px;">Complete this task to earn 10,000 Diamonds!</p>
                        <a href="https://www.profitablecpmratenetwork.com/a68pzvy9g?key=ff79dfacf59be49e36f413f0f2e76766" target="_blank" style="background:#00ff00; color:black; padding:15px 40px; border-radius:30px; text-decoration:none; font-weight:bold; display:inline-block; margin-top:20px;">CLICK FOR BIG REWARD</a>
                    </div>
                ''', unsafe_allow_html=True)
    except: st.error("সার্ভার সিঙ্ক হচ্ছে...")

# ৭. আপনার ভিডিও আপলোড সেকশন
elif tab == "📤 Upload Video":
    if st.session_state.user:
        v_title = st.text_input("ভিডিও টাইটেল দিন")
        target_ch = st.selectbox("কোন চ্যানেলে যাবে?", ["চ্যানেল ১", "চ্যানেল ২"])
        v_file = st.file_uploader("আপনার ভিডিও ফাইলটি দিন (MP4)", type=['mp4'])
        
        if st.button("🚀 Publish to YouTube") and v_file:
            with st.spinner("ইউটিউব ও ডাটাবেসে সিঙ্ক হচ্ছে..."):
                try:
                    yt = get_yt_service(target_ch)
                    request = yt.videos().insert(
                        part="snippet,status",
                        body={"snippet": {"title": v_title}, "status": {"privacyStatus": "public"}},
                        media_body=MediaIoBaseUpload(v_file, mimetype='video/mp4', resumable=True)
                    )
                    response = request.execute()
                    final_url = f"https://www.youtube.com/watch?v={response['id']}"
                    
                    supabase.table("videos").insert({
                        "video_url": final_url, 
                        "uploader_name": st.session_state.user, 
                        "uploader_pic": st.session_state.pic, 
                        "likes": 0, "followers": 0, "views": 0
                    }).execute()
                    st.success(f"✅ আপনার ভিডিও সফলভাবে পাবলিশ হয়েছে!")
                except Exception as e: st.error(f"Error: {e}")
