import streamlit as st
import uuid
import random
import os
import sqlite3
import subprocess
from datetime import datetime
import streamlit.components.v1 as components

# ১. মেটা ট্যাগ ও ভেরিফিকেশন
st.markdown(
    """
    <head>
        <meta name="msvalidate.01" content="e776b8ce73ea3dcc07551e8a021a0907">
        <meta name="monetag" content="5cc1b7ba5cb29eff802ce49009f87e2b">
    </head>
    """,
    unsafe_allow_html=True
)

SMART_LINK = "https://omg10.com/4/10954816"

# ২. লোকাল SQLite ডাটাবেস ও স্টোরেজ ফোল্ডার সেটআপ (সুপাবেস সম্পূর্ণ মুক্ত)
DB_FILE = "local_storage.db"
VIDEO_DIR = "stored_videos"
PROFILE_DIR = "stored_profiles"

for folder in [VIDEO_DIR, PROFILE_DIR]:
    if not os.path.exists(folder):
        os.makedirs(folder)

def get_db_connection():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

# ডাটাবেস টেবিল তৈরি করা
conn = get_db_connection()
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        profile_pic TEXT
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS videos (
        id TEXT PRIMARY KEY,
        video_url TEXT,
        uploader_name TEXT,
        uploader_pic TEXT,
        likes INTEGER,
        views INTEGER,
        followers INTEGER,
        created_at TEXT
    )
''')
conn.commit()
conn.close()

st.set_page_config(page_title="BT AI book", layout="wide")

# ৩. ফরম্যাট
def format_value(value):
    if value >= 1000: return f"{value/1000:.1f}K"
    return str(value)

def show_auto_moving_banner():
    ad_html = f"""
    <div style="text-align:center; margin: 10px 0;">
        <a href="{SMART_LINK}" target="_blank" style="text-decoration:none;">
            <div style="background: linear-gradient(90deg, #00c853, #000); 
                        color: #fff; padding: 15px; border-radius: 10px; 
                        border: 2px solid #00c853; font-family: sans-serif;">
                <span style="font-size: 18px; font-weight: bold;">⚡ PREMIUM REWARD ACTIVE ⚡</span><br>
                <span style="font-size: 12px;">Click to Claim Your Diamond Bonus!</span>
            </div>
        </a>
    </div>
    """
    components.html(ad_html, height=120)

# ৪. একদম সাদা ব্যাকগ্রাউন্ড ডিজাইন
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #000000; }
    .video-card { background: #ffffff; border: 1px solid #ddd; border-radius: 15px; padding: 15px; margin-bottom: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .user-avatar { width: 50px; height: 50px; border-radius: 50%; border: 2px solid #00c853; object-fit: cover; margin-right: 12px; }
    .stat-box { font-size: 14px; color: #333; font-weight: bold; margin-right: 15px; }
    .btn-direct { display: block; width: 100%; padding: 12px; margin: 8px 0; color: white !important; text-align: center; border-radius: 10px; font-weight: bold; text-decoration: none; font-size: 15px; }
    .bg-1 { background: linear-gradient(135deg, #FF416C, #FF4B2B); }
    .bg-2 { background: linear-gradient(135deg, #1DE9B6, #26A69A); }
    .bg-3 { background: linear-gradient(135deg, #667eea, #764ba2); }
    .bg-4 { background: linear-gradient(135deg, #f6d365, #fda085); }
    .banner-box { background: #fff; border: 1px dashed #ed1c24; padding: 15px; text-align: center; border-radius: 10px; margin: 15px 0; color: #000; }
    section[data-testid="stSidebar"] { background-color: #f8f9fa !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ BT AI book")

# ৫. লগইন সিস্টেম
if 'user' not in st.session_state:
    st.session_state.user = None
    st.session_state.pic = None

conn = get_db_connection()
cursor = conn.cursor()

if not st.session_state.user:
    u_name = st.sidebar.text_input("Name")
    if u_name:
        cursor.execute("SELECT * FROM users WHERE username = ?", (u_name,))
        user_data = cursor.fetchone()
        
        if user_data:
            if st.sidebar.button("Login"):
                st.session_state.user = u_name
                st.session_state.pic = user_data['profile_pic']
                st.rerun()
        else:
            u_pic = st.sidebar.file_uploader("Upload Photo", type=['jpg', 'png', 'jpeg'])
            if st.sidebar.button("Join Now"):
                if u_name and u_pic:
                    fname = os.path.join(PROFILE_DIR, f"p_{uuid.uuid4()}.jpg")
                    with open(fname, "wb") as f:
                        f.write(u_pic.getvalue())
                    
                    cursor.execute("INSERT INTO users (username, profile_pic) VALUES (?, ?)", (u_name, fname))
                    conn.commit()
                    
                    st.session_state.user = u_name
                    st.session_state.pic = fname
                    st.rerun()
else:
    if st.session_state.pic and os.path.exists(st.session_state.pic):
        st.sidebar.image(st.session_state.pic, width=80)
    st.sidebar.write(f"Hello, **{st.session_state.user}**")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.session_state.pic = None
        st.rerun()

tab = st.sidebar.radio("Menu", ["🌍 World Feed", "📤 Upload Video"])

# ৬. মেইন ফিড (ভিডিও দেখার অংশ)
if tab == "🌍 World Feed":
    try:
        cursor.execute("SELECT * FROM videos")
        rows = cursor.fetchall()
        data = [dict(row) for row in rows]
        random.shuffle(data)
        
        for index, v in enumerate(data):
            v_id = str(v['id']) 
            st.markdown('<div class="video-card">', unsafe_allow_html=True)
            
            uploader_pic_path = v.get("uploader_pic", "")
            if not uploader_pic_path or not os.path.exists(uploader_pic_path):
                uploader_pic_path = ""
                
            st.markdown(f'<div style="display:flex; align-items:center; margin-bottom:12px; color:#000;"><img src="{uploader_pic_path}" class="user-avatar"><b>{v.get("uploader_name")}</b></div>', unsafe_allow_html=True)
            
            # লোকাল ভিডিও রেন্ডারিং
            if os.path.exists(v['video_url']):
                st.video(v['video_url'])
            else:
                st.error("Video file not found locally.")
            
            # ভিউ আপডেট
            new_views = v.get("views", 0) + 1
            cursor.execute("UPDATE videos SET views = ? WHERE id = ?", (new_views, v_id))
            conn.commit()

            show_auto_moving_banner()

            st.markdown(f'''
                <div class="banner-box">
                    <a href="{SMART_LINK}" target="_blank" 
                       style="background:#ed1c24; color:white; padding:10px 25px; border-radius:5px; text-decoration:none; font-weight:bold; display:inline-block;">Click to Win Reward 🎁</a>
                </div>
                <div style="margin: 10px 0; display: flex; justify-content: start;">
                    <span class="stat-box">👁️ {format_value(new_views)} Views</span>
                    <span class="stat-box">❤️ {format_value(v.get("likes", 0))} Likes</span>
                    <span class="stat-box">👤 {format_value(v.get("followers", 0))} Followers</span>
                </div>
                <a href="{SMART_LINK}" target="_blank" class="btn-direct bg-1">💰 High CPC Reward 1</a>
                <a href="{SMART_LINK}" target="_blank" class="btn-direct bg-2">💎 Premium Bonus 2</a>
                <a href="{SMART_LINK}" target="_blank" class="btn-direct bg-3">🚀 Mega Earning 3</a>
                <a href="{SMART_LINK}" target="_blank" class="btn-direct bg-4">🎁 Special Gift 4</a>
            ''', unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button(f"❤️ Like", key=f"lk_{v_id}_{index}"):
                    cursor.execute("UPDATE videos SET likes = likes + 1 WHERE id = ?", (v_id,))
                    conn.commit()
                    st.rerun()
            with c2:
                if st.button(f"➕ Follow", key=f"fl_{v_id}_{index}"):
                    cursor.execute("UPDATE videos SET followers = followers + 1 WHERE id = ?", (v_id,))
                    conn.commit()
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Feed Error: {e}")

# ৭. ভিডিও আপলোড
elif tab == "📤 Upload Video":
    if not st.session_state.user: 
        st.warning("Login first!")
    else:
        st.markdown("<h3 style='color:#000;'>Upload Your Video</h3>", unsafe_allow_html=True)
        file = st.file_uploader("Select Video", type=['mp4'])
        if st.button("🚀 Publish Video") and file:
            today = datetime.now().strftime("%Y-%m-%d")
            
            cursor.execute("SELECT * FROM videos WHERE uploader_name = ? AND created_at >= ?", (st.session_state.user, today))
            check_data = cursor.fetchall()
            
            if check_data and len(check_data) >= 3:
                st.error("Daily limit reached!")
            else:
                with st.spinner("Publishing..."):
                    t_in, t_out = "raw.mp4", "final.mp4"
                    with open(t_in, "wb") as f: 
                        f.write(file.getvalue())
                    
                    # ২০ সেকেন্ড এবং ৩ এমবি লিমিট কম্প্রেশন
                    cmd = f'ffmpeg -i {t_in} -t 20 -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -vcodec libx264 -fs 2.9M -y {t_out}'
                    subprocess.run(cmd, shell=True)
                    
                    try:
                        v_id = str(uuid.uuid4())
                        v_name = os.path.join(VIDEO_DIR, f"v_{v_id}.mp4")
                        
                        # লোকাল ফোল্ডারে কমপ্রেসড ভিডিও মুভ করা
                        if os.path.exists(t_out):
                            with open(t_out, "rb") as f_src, open(v_name, "wb") as f_dst:
                                f_dst.write(f_src.read())
                        
                            cursor.execute("""
                                INSERT INTO videos (id, video_url, uploader_name, uploader_pic, likes, views, followers, created_at)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                            """, (
                                v_id, 
                                v_name, 
                                st.session_state.user,
                                st.session_state.pic, 
                                random.randint(20, 50), 
                                random.randint(850, 1200), 
                                random.randint(100, 150),
                                today
                            ))
                            conn.commit()
                            st.success("Published Locally!")
                        else:
                            st.error("Compression failed. Make sure FFmpeg is installed.")
                    except Exception as upload_err:
                        st.error(f"Save failed: {upload_err}")
                    
                    if os.path.exists(t_in): os.remove(t_in)
                    if os.path.exists(t_out): os.remove(t_out)
                    st.rerun()

conn.close()
