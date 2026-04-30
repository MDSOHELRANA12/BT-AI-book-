import streamlit as st
from supabase import create_client
import uuid
import random
import os
import json
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google_auth_oauthlib.flow import InstalledAppFlow
import io

# ১. সুপাবেস কানেকশন
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

# ২. ইউটিউব কনফিগারেশন (আপনার দেওয়া ডাটা)
CLIENT_CONFIG = {
    "web": {
        "client_id": "681450003814-j2fc889ei0gj0cfog625ibpg15bflcur.apps.googleusercontent.com",
        "project_id": "bt-ai-book",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "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",
        "redirect_uris": ["http://localhost:8501"]
    }
}
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

st.set_page_config(page_title="BT AI book", layout="wide")

# --- ইউটিউব আপলোড ফাংশন ---
def upload_to_youtube(video_file, title, description):
    try:
        flow = InstalledAppFlow.from_client_config(CLIENT_CONFIG, SCOPES)
        credentials = flow.run_local_server(port=8501)
        youtube = build('youtube', 'v3', credentials=credentials)

        request_body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': ['BT AI book', 'Sohel Rana'],
                'categoryId': '22'
            },
            'status': {
                'privacyStatus': 'public',
                'selfDeclaredMadeForKids': False,
            }
        }

        media = MediaIoBaseUpload(io.BytesIO(video_file.read()), mimetype='video/mp4', resumable=True)
        response = youtube.videos().insert(
            part='snippet,status',
            body=request_body,
            media_body=media
        ).execute()
        return response.get('id')
    except Exception as e:
        st.error(f"YouTube Upload Error: {e}")
        return None

# ৩. ডিজাইন ও স্টাইল
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .video-card { 
        background: #0d0d0d; border: 1px solid #333; border-radius: 15px; 
        padding: 15px; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    .btn-reward { 
        display: block; width: 100%; padding: 12px; margin: 10px 0; 
        background: linear-gradient(135deg, #ed1c24, #aa0000); 
        color: white !important; text-align: center; border-radius: 8px; 
        font-weight: bold; text-decoration: none;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ BT AI book - YouTube Integrated")

# ৪. লগইন সিস্টেম (আপনার আগের কোড অনুযায়ী)
if 'user' not in st.session_state:
    st.session_state.user = None
    st.session_state.pic = None

# ... (লগইন লজিক এখানে থাকবে) ...

tab = st.sidebar.radio("Navigation", ["🌍 World Feed", "📤 Upload Video"])

# ৫. মেইন ফিড
if tab == "🌍 World Feed":
    st.info("ভিডিও ফিড লোড হচ্ছে...")
    # আপনার আগের ফিড ডিসপ্লে কোড এখানে থাকবে

# ৬. ভিডিও আপলোড (ইউটিউব কানেকশন সহ)
elif tab == "📤 Upload Video":
    if st.session_state.user:
        v_file = st.file_uploader("Select MP4 to upload on YouTube", type=['mp4'])
        v_title = st.text_input("Video Title", value="New Video from BT AI book")
        
        if st.button("🚀 Publish to YouTube & Feed") and v_file:
            with st.spinner("🤖 ইউটিউবে আপলোড হচ্ছে... অনুগ্রহ করে ব্রাউজার উইন্ডো চেক করুন"):
                # ইউটিউবে আপলোড
                yt_id = upload_to_youtube(v_file, v_title, "Uploaded via BT AI book app")
                
                if yt_id:
                    # ইউটিউব সফল হলে সুপাবেসে ডাটা সেভ
                    v_url = f"https://www.youtube.com/watch?v={yt_id}"
                    supabase.table("videos").insert({
                        "video_url": v_url, 
                        "uploader_name": st.session_state.user, 
                        "uploader_pic": st.session_state.pic, 
                        "likes": 0, "followers": 0, "views": 0
                    }).execute()
                    st.success(f"✅ সোহেল ভাই, ভিডিও ইউটিউবে লাইভ হয়েছে! ID: {yt_id}")
                else:
                    st.error("ইউটিউব আপলোডে সমস্যা হয়েছে।")
    else:
        st.warning("আগে লগইন করুন।")
