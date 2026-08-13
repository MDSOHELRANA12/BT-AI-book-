import streamlit as st
import uuid
import random
import os
import sqlite3
from datetime import datetime
import streamlit.components.v1 as components

# ১. পেজ কনফিগারেশন
st.set_page_config(page_title="BT AI Book — Verified Network", layout="wide", initial_sidebar_state="expanded")

# মেটা ট্যাগ বসানোর সঠিক উপায়
components.html(
    """
    <meta name="msvalidate.01" content="e776b8ce73ea3dcc07551e8a021a0907">
    <meta name="monetag" content="5cc1b7ba5cb29eff802ce49009f87e2b">
    """,
    height=0,
)

SMART_LINK = "https://omg10.com/4/10954816"

# ২. লোকাল ডাটাবেস ও স্টোরেজ
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

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            profile_pic TEXT,
            is_verified INTEGER DEFAULT 1,
            created_at TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            id TEXT PRIMARY KEY,
            video_url TEXT,
            uploader_name TEXT,
            uploader_pic TEXT,
            video_type TEXT DEFAULT 'long',
            title TEXT,
            likes INTEGER DEFAULT 0,
            views INTEGER DEFAULT 0,
            followers INTEGER DEFAULT 0,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ৩. হেল্পার ফাংশন
def format_value(value):
    if value >= 1000000: return f"{value/1000000:.1f}M"
    if value >= 1000: return f"{value/1000:.1f}K"
    return str(value)

def render_blue_tick(name, is_verified=1):
    if is_verified:
        return f'''{name} <span style="background-color:#1877F2; color:white; border-radius:50%; padding: 2px 6px; font-size:11px;" title="Verified Creator">✓</span>'''
    return name

def show_auto_moving_banner():
    ad_html = f"""
    <div style="text-align:center; margin: 10px 0;">
        <a href="{SMART_LINK}" target="_blank" style="text-decoration:none;">
            <div style="background: linear-gradient(90deg, #00c853, #000); 
                        color: #fff; padding: 12px; border-radius: 10px; 
                        border: 2px solid #00c853; font-family: sans-serif;">
                <span style="font-size: 16px; font-weight: bold;">⚡ PREMIUM REWARD ACTIVE ⚡</span><br>
                <span style="font-size: 11px;">Click to Claim Your Diamond Bonus!</span>
            </div>
        </a>
    </div>
    """
    components.html(ad_html, height=100)

# ৪. সিএসএস ডিজাইন
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #000000; }
    .long-video-card {
        background: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    }
    .profile-card {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid #dee2e6;
    }
    .btn-direct { display: block; width: 100%; padding: 10px; margin: 6px 0; color: white !important; text-align: center; border-radius: 8px; font-weight: bold; text-decoration: none; font-size: 14px; }
    .bg-1 { background: linear-gradient(135deg, #FF416C, #FF4B2B); }
    .bg-2 { background: linear-gradient(135deg, #1DE9B6, #26A69A); }
    section[data-testid="stSidebar"] { background-color: #f8f9fa !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ BT AI Book — Verified Network")

# ৫. সেশন স্টেট
if 'user' not in st.session_state:
    st.session_state.user = None
    st.session_state.pic = None
    st.session_state.is_verified = 1

# ৬. সাইডবার: ফেস লগইন
st.sidebar.header("📸 Face ID Verification")

if not st.session_state.user:
    u_name = st.sidebar.text_input("আপনার নাম (Username)")
    camera_photo = st.sidebar.camera_input("Take Face Scan", key="face_cam")
    
    if u_name and camera_photo:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (u_name,))
        user_data = cursor.fetchone()
        
        if user_data:
            if st.sidebar.button("🔓 ফেস স্ক্যান দিয়ে লগইন করুন"):
                st.session_state.user = u_name
                st.session_state.pic = user_data['profile_pic']
                st.session_state.is_verified = user_data['is_verified']
                conn.close()
                st.rerun()
        else:
            if st.sidebar.button("✨ নতুন একাউন্ট খুলুন (ব্লু টিকসহ)"):
                fname = os.path.join(PROFILE_DIR, f"p_{uuid.uuid4()}.jpg")
                with open(fname, "wb") as f:
                    f.write(camera_photo.getvalue())
                
                today_str = datetime.now().strftime("%Y-%m-%d")
                cursor.execute("INSERT INTO users (username, profile_pic, is_verified, created_at) VALUES (?, ?, ?, ?)", 
                               (u_name, fname, 1, today_str))
                conn.commit()
                conn.close()
                
                st.session_state.user = u_name
                st.session_state.pic = fname
                st.session_state.is_verified = 1
                st.sidebar.success("🎉 একাউন্ট তৈরি সফল!")
                st.rerun()
else:
    if st.session_state.pic and os.path.exists(st.session_state.pic):
        st.sidebar.image(st.session_state.pic, width=90)
    
    st.sidebar.write(f"স্বাগতম, **{st.session_state.user}** ✓")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.session_state.pic = None
        st.session_state.is_verified = 1
        st.rerun()

tab = st.sidebar.radio("Navigation", ["🌍 World Feed", "👤 My Profile", "📤 Upload Video"])

# ৭. মেইন ফিড
if tab == "🌍 World Feed":
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM videos")
        rows = cursor.fetchall()
        data = [dict(row) for row in rows]
        random.shuffle(data)
        
        if not data:
            st.info("এখনো কোনো ভিডিও নেই। প্রথম ভিডিওটি আপলোড করুন!")

        for index, v in enumerate(data):
            v_id = str(v['id'])
            v_type = v.get("video_type", "long")
            
            st.markdown('<div class="long-video-card">', unsafe_allow_html=True)
            
            uploader_name = v.get("uploader_name", "Unknown User")
            
            st.write(f"👤 **{uploader_name}** ✓  •  *🎬 {v_type.upper()}*")
            if v.get("title"):
                st.markdown(f"### {v.get('title')}")
            
            # ভিডিও প্লেয়ার
            if os.path.exists(v['video_url']):
                st.video(v['video_url'])
            else:
                st.error("ভিডিও ফাইলটি পাওয়া যায়নি।")
            
            # ভিউ সংখ্যা আপডেট
            new_views = v.get("views", 0) + 1
            cursor.execute("UPDATE videos SET views = ? WHERE id = ?", (new_views, v_id))
            conn.commit()

            show_auto_moving_banner()

            st.write(f"👁️ **{format_value(new_views)}** Views | ❤️ **{format_value(v.get('likes', 0))}** Likes")
            st.markdown(f'''
                <a href="{SMART_LINK}" target="_blank" class="btn-direct bg-1">💰 Claim Reward 1</a>
                <a href="{SMART_LINK}" target="_blank" class="btn-direct bg-2">💎 Premium Bonus 2</a>
            ''', unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button(f"❤️ Like ({format_value(v.get('likes', 0))})", key=f"lk_{v_id}_{index}"):
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
    finally:
        conn.close()

# ৮. মাই প্রোফাইল
elif tab == "👤 My Profile":
    if not st.session_state.user:
        st.warning("আপনার প্রোফাইল দেখতে প্রথমে লগইন করুন!")
    else:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM videos WHERE uploader_name = ?", (st.session_state.user,))
        my_videos = [dict(r) for r in cursor.fetchall()]
        
        total_likes = sum([v.get("likes", 0) for v in my_videos])
        total_views = sum([v.get("views", 0) for v in my_videos])
        
        st.markdown(f'''
            <div class="profile-card">
                <h2>{st.session_state.user} ✓</h2>
                <p style="color:#1877F2; font-weight:bold;">🛡️ Official Verified Creator</p>
                <p>📹 আপলোড: <b>{len(my_videos)}</b>টি | ❤️ লাইক: <b>{format_value(total_likes)}</b> | 👁️ ভিউ: <b>{format_value(total_views)}</b></p>
            </div>
        ''', unsafe_allow_html=True)
        
        st.subheader("🎬 আমার ভিডিওসমূহ")
        if not my_videos:
            st.info("আপনি এখনো কোনো ভিডিও আপলোড করেননি।")
        else:
            cols = st.columns(2)
            for idx, mv in enumerate(my_videos):
                with cols[idx % 2]:
                    st.write(f"**{mv.get('title', 'Untitled Video')}**")
                    if os.path.exists(mv['video_url']):
                        st.video(mv['video_url'])
                    st.caption(f"👁️ {format_value(mv.get('views', 0))} views • ❤️ {format_value(mv.get('likes', 0))} likes")
        conn.close()

# ৯. ভিডিও আপলোড
elif tab == "📤 Upload Video":
    if not st.session_state.user:
        st.warning("ভিডিও আপলোড করতে প্রথমে ফেস স্ক্যান করে লগইন করুন!")
    else:
        st.markdown("<h3>আপনার ভিডিও পাবলিশ করুন</h3>", unsafe_allow_html=True)
        
        v_title = st.text_input("ভিডিও টাইটেল")
        v_type = st.selectbox("ভিডিওর ধরন", ["Long Video", "Short Video"])
        file = st.file_uploader("Select Video File (MP4)", type=['mp4'])
        
        if st.button("🚀 Publish Video") and file:
            today = datetime.now().strftime("%Y-%m-%d")
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM videos WHERE uploader_name = ? AND created_at >= ?", (st.session_state.user, today))
            check_data = cursor.fetchall()
            
            if check_data and len(check_data) >= 5:
                st.error("দৈনিক ৫টির বেশি ভিডিও আপলোড করা যাবে না!")
                conn.close()
            else:
                with st.spinner("পাবলিশ হচ্ছে..."):
                    v_id = str(uuid.uuid4())
                    v_name = os.path.join(VIDEO_DIR, f"v_{v_id}.mp4")
                    
                    with open(v_name, "wb") as f_dst:
                        f_dst.write(file.getvalue())
                    
                    video_kind = "long" if "Long" in v_type else "short"
                    
                    cursor.execute("""
                        INSERT INTO videos (id, video_url, uploader_name, uploader_pic, video_type, title, likes, views, followers, created_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        v_id, 
                        v_name, 
                        st.session_state.user,
                        st.session_state.pic, 
                        video_kind,
                        v_title if v_title else "Untitled Video",
                        random.randint(10, 50), 
                        1, 
                        random.randint(5, 30),
                        today
                    ))
                    conn.commit()
                    conn.close()
                    st.success("🎉 সফলভাবে পাবলিশ করা হয়েছে!")
                    st.rerun()
