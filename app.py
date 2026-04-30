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

# ১. সুপাবেস কানেকশন (অক্ষত রাখা হয়েছে)
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

# ইউটিউব চাবি (আপনার দেওয়া তথ্য অনুযায়ী)
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

st.set_page_config(page_title="BT AI book", layout="wide")

# ২. ফরম্যাট ফাংশন (অক্ষত)
def format_value(value):
    if value >= 1000000: return f"{value/1000000:.1f}M"
    elif value >= 1000: return f"{value/1000:.1f}K"
    return str(value)

# ৩. ডিজাইন ও স্টাইল (আপনার প্রিয় সেই কালো ও লাল থিম)
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
    .username-text { font-weight: bold; font-size: 18px; color: #fff; }
    .stat-box { font-size: 14px; color: #00ff00; font-weight: bold; margin-right: 15px; }
    .btn-reward { 
        display: block; width: 100%; padding: 12px; margin: 10px 0; 
        background: linear-gradient(135deg, #ed1c24, #aa0000); 
        color: white !important; text-align: center; border-radius: 8px; 
        font-weight: bold; text-decoration: none;
    }
    .big-ad-box {
        background: #1a1a1a; border: 2px dashed #ed1c24; border-radius: 15px;
        padding: 25px; text-align: center; margin-bottom: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

# ইউটিউব অথেনটিকেশন ফাংশন
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
            flow = InstalledAppFlow.from_client_config(config, ['https://www.googleapis.com/auth/youtube.upload'])
            creds = flow.run_local_server(port=8501, prompt='consent')
        with open(ch['token_file'], 'wb') as token:
            pickle.dump(creds, token)
    return build('youtube', 'v3', credentials=creds)

st.title("🛡️ BT AI book")

# ৪. লগইন সিস্টেম (অক্ষত)
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

# ৫. মেইন ফিড (অরিজিনাল অ্যাড ও প্লেয়ার)
if tab == "🌍 World Feed":
    try:
        res = supabase.table("videos").select("*").execute()
        data = res.data if res.data else []
        random.shuffle(data)

        for index, v in enumerate(data):
            st.markdown('<div class="video-card">', unsafe_allow_html=True)
            st.markdown(f'<div style="display:flex; align-items:center; margin-bottom:15px;"><img src="{v.get("uploader_pic", "")}" class="user-avatar"><span class="username-text">{v.get("uploader_name", "BT User")}</span></div>', unsafe_allow_html=True)
            
            # ইউটিউব ভিডিও হলে লোগো ছাড়া প্লেয়ার, না হলে নরমাল প্লেয়ার
            v_url = v['video_url']
            if "youtube.com/4" in v_url:
                v_id = v_url.split("4")[-1]
                st.components.v1.html(f'<iframe width="100%" height="315" src="https://www.youtube.com/embed/{v_id}?modestbranding=1&rel=0" frameborder="0" allowfullscreen></iframe>', height=315)
            else:
                st.video(v_url)
            
            # লাইক, ভিউ ও অ্যাড সিস্টেম (সব আপনার অরিজিনাল কোড থেকে আনা)
            st.markdown(f'''
                <div style="margin: 12px 0;">
                    <span class="stat-box">👁️ {format_value(v.get("views", 0))} Views</span>
                    <span class="stat-box">❤️ {format_value(v.get("likes", 0))} Likes</span>
                    <span class="stat-box">👤 {format_value(v.get("followers", 0))} Followers</span>
                </div>
            ''', unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button(f"❤️ Like", key=f"l_{v['id']}"):
                    supabase.table("videos").update({"likes": v.get("likes", 0) + 1}).eq("id", v['id']).execute(); st.rerun()
            with c2:
                if st.button(f"➕ Follow", key=f"f_{v['id']}"):
                    supabase.table("followers").update({"followers": v.get("followers", 0) + 1}).eq("id", v['id']).execute(); st.rerun()

            st.markdown(f'<a href="https://www.profitablecpmratenetwork.com/tgt6azn6?key=e753cbd6d9bae06d67051ed846419521" target="_blank" class="btn-reward">💎 Claim Diamond Reward</a>', unsafe_allow_html=True)
            
            st.components.v1.html("""<script type="text/javascript">atOptions = { 'key' : '342950879f2064f7255ad047622381c8', 'format' : 'iframe', 'height' : 50, 'width' : 320, 'params' : {} };</script><script src="https://www.highperformanceformat.com/342950879f2064f7255ad047622381c8/invoke.js"></script>""", height=65)
            st.markdown('</div>', unsafe_allow_html=True)

            if (index + 1) % 2 == 0:
                st.markdown('<div class="big-ad-box"><p style="color:#00ff00; font-size:18px; font-weight:bold;">🔥 BIG REWARD WAITING 🔥</p><a href="https://www.profitablecpmratenetwork.com/a68pzvy9g?key=ff79dfacf59be49e36f413f0f2e76766" target="_blank" style="background:#ed1c24; color:white; padding:12px 35px; border-radius:30px; text-decoration:none; font-weight:bold; display:inline-block; margin-top:10px;">CLICK FOR BIG AD REWARD</a></div>', unsafe_allow_html=True)
    except: st.error("Syncing Feed...")

# ৬. ভিডিও আপলোড (মাস্টার অটোমেশন ইঞ্জিন)
elif tab == "📤 Upload Video":
    if st.session_state.user:
        v_title = st.text_input("ভিডিওর টাইটেল দিন")
        target_ch = st.selectbox("কোন চ্যানেলে আপলোড হবে?", ["চ্যানেল ১", "চ্যানেল ২"])
        v_file = st.file_uploader("Select MP4", type=['mp4'])
        
        if st.button("🚀 Publish to YouTube") and v_file:
            with st.spinner("🤖 ওজন শূন্য করে ইউটিউবে পাঠানো হচ্ছে..."):
                try:
                    # ইউটিউব আপলোড লজিক
                    yt = get_yt_service(target_ch)
                    request = yt.videos().insert(
                        part="snippet,status",
                        body={"snippet": {"title": v_title}, "status": {"privacyStatus": "public"}},
                        media_body=MediaIoBaseUpload(v_file, mimetype='video/mp4', resumable=True)
                    )
                    response = request.execute()
                    final_url = f"https://www.youtube.com/watch?v={response['id']}"
                    
                    # সুপাবেসে ডাটা সেভ
                    supabase.table("videos").insert({
                        "video_url": final_url, 
                        "uploader_name": st.session_state.user, 
                        "uploader_pic": st.session_state.pic, 
                        "likes": 0, "followers": 0, "views": 0
                    }).execute()
                    st.success(f"✅ সোহেল ভাই, {target_ch}-এ সফলভাবে পাবলিশ হয়েছে!")
                except Exception as e:
                    st.error(f"Error: {e}")
