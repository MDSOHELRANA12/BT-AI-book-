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

# ২. ইউটিউব কনফিগারেশন (Refresh Token লজিকসহ)
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

# ৩. ইউটিউব সার্ভিস জেনারেটর (একবার ভেরিফাই করলে আজীবন চলবে)
def get_yt_service(ch_name):
    ch = CHANNELS[ch_name]
    creds = None
    
    # আগে থেকে ভেরিফাই করা থাকলে ফাইল থেকে পড়বে
    if os.path.exists(ch['token_file']):
        with open(ch['token_file'], 'rb') as token:
            creds = pickle.load(token)
            
    # যদি টোকেন না থাকে বা মেয়াদ শেষ হয়
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            config = {
                "web": {
                    "client_id": ch['client_id'],
                    "client_secret": ch['client_secret'],
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token"
                }
            }
            # এখানে 'access_type=offline' দেওয়া হয়েছে যাতে আজীবন কাজ করে
            flow = InstalledAppFlow.from_client_config(config, ['https://www.googleapis.com/auth/youtube.upload'])
            creds = flow.run_local_server(port=0, prompt='consent', access_type='offline')
        
        # টোকেন সেভ করে রাখা হচ্ছে
        with open(ch['token_file'], 'wb') as token:
            pickle.dump(creds, token)
            
    return build('youtube', 'v3', credentials=creds)

st.set_page_config(page_title="BT AI book", layout="wide")

# ৪. ডিজাইন ও স্টাইল (সোহেল ভাইয়ের অরিজিনাল থিম)
def format_value(value):
    if value >= 1000000: return f"{value/1000000:.1f}M"
    elif value >= 1000: return f"{value/1000:.1f}K"
    return str(value)

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
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ BT AI book")

# ৫. লগইন সিস্টেম (অক্ষত)
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

# ৬. মেইন ফিড (ভিডিও প্লেয়ার ও রিওয়ার্ড)
if tab == "🌍 World Feed":
    try:
        res = supabase.table("videos").select("*").execute()
        data = res.data if res.data else []
        random.shuffle(data)

        for index, v in enumerate(data):
            st.markdown('<div class="video-card">', unsafe_allow_html=True)
            st.markdown(f'<div style="display:flex; align-items:center; margin-bottom:15px;"><img src="{v.get("uploader_pic", "")}" class="user-avatar"><span class="username-text">{v.get("uploader_name", "BT User")}</span></div>', unsafe_allow_html=True)
            
            v_url = v['video_url']
            # ইউটিউব ভিডিও হলে অটো প্লেয়ার
            if "youtube.com" in v_url or "youtu.be" in v_url:
                st.video(v_url)
            else:
                st.video(v_url)
            
            st.markdown(f'''
                <div style="margin: 12px 0;">
                    <span class="stat-box">👁️ {format_value(v.get("views", 0))} Views</span>
                    <span class="stat-box">❤️ {format_value(v.get("likes", 0))} Likes</span>
                </div>
            ''', unsafe_allow_html=True)
            
            st.markdown(f'<a href="https://www.profitablecpmratenetwork.com/tgt6azn6?key=e753cbd6d9bae06d67051ed846419521" target="_blank" class="btn-reward">💎 Claim Diamond Reward</a>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    except: st.error("Syncing Feed...")

# ৭. ভিডিও আপলোড অটোমেশন (আজীবন ভেরিফাইড সিস্টেম)
elif tab == "📤 Upload Video":
    if st.session_state.user:
        v_title = st.text_input("ভিডিওর টাইটেল দিন")
        target_ch = st.selectbox("কোন চ্যানেলে আপলোড হবে?", ["চ্যানেল ১", "চ্যানেল ২"])
        v_file = st.file_uploader("Select MP4", type=['mp4'])
        
        if st.button("🚀 Publish to YouTube") and v_file:
            with st.spinner("🤖 অটোমেটিক ভেরিফাই করে ইউটিউবে পাঠানো হচ্ছে..."):
                try:
                    # ১. একবার ভেরিফাই করবে, পরে অটো টোকেন নিবে
                    yt = get_yt_service(target_ch)
                    
                    # ২. ভিডিও ইউটিউবে যাবে
                    request = yt.videos().insert(
                        part="snippet,status",
                        body={
                            "snippet": {"title": v_title, "description": "Uploaded via BT AI Book"},
                            "status": {"privacyStatus": "public"}
                        },
                        media_body=MediaIoBaseUpload(v_file, mimetype='video/mp4', resumable=True)
                    )
                    response = request.execute()
                    final_url = f"https://www.youtube.com/watch?v={response['id']}"
                    
                    # ৩. সুপাবেসে ডাটা সেভ
                    supabase.table("videos").insert({
                        "video_url": final_url, 
                        "uploader_name": st.session_state.user, 
                        "uploader_pic": st.session_state.pic, 
                        "likes": 0, "views": 0
                    }).execute()
                    
                    st.success(f"✅ সফলভাবে পাবলিশ হয়েছে! ইউটিউব আইডি: {response['id']}")
                except Exception as e:
                    st.error(f"Error: {e}")
