import streamlit as st
import uuid
import random
import os
import sqlite3
from datetime import datetime
import streamlit.components.v1 as components

# 1. Page Configuration
st.set_page_config(page_title="BT AI Book — Verified Network", layout="wide", initial_sidebar_state="expanded")

# Meta Tags & Monetization Scripts
components.html(
    """
    <meta name="msvalidate.01" content="e776b8ce73ea3dcc07551e8a021a0907">
    <meta name="monetag" content="5cc1b7ba5cb29eff802ce49009f87e2b">
    """,
    height=0,
)

SMART_LINK = "https://omg10.com/4/10954816"

# 2. Database & Directory Setup
DB_FILE = "local_storage.db"
VIDEO_DIR = "stored_videos"
PROFILE_DIR = "stored_profiles"

for folder in [VIDEO_DIR, PROFILE_DIR]:
    if not os.path.exists(folder):
        os.makedirs(folder)

def get_db_connection():
    conn = sqlite3.connect(DB_FILE, check_check_same_thread=False) if hasattr(sqlite3, 'check_check_same_thread') else sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            full_name TEXT,
            profile_pic TEXT,
            is_verified INTEGER DEFAULT 1,
            payment_method TEXT,
            account_details TEXT,
            nid_number TEXT,
            address TEXT,
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

# 3. Helper Functions
def format_value(value):
    if value >= 1000000: return f"{value/1000000:.1f}M"
    if value >= 1000: return f"{value/1000:.1f}K"
    return str(value)

# SVG Blue Tick (YouTube/TikTok/Facebook Style)
BLUE_TICK_SVG = """
<svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle; margin-left: 5px;">
    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" fill="#1D9BF0"/>
</svg>
"""

def render_profile_header(display_name, pic_url=None, is_verified=1, subtitle="Official Global Verified Creator"):
    img_html = f'<img src="data:image/png;base64,{pic_url}" style="width:70px; height:70px; border-radius:50%; object-fit:cover; border:2px solid #1D9BF0;">' if pic_url else '<div style="width:70px; height:70px; border-radius:50%; background:#e0e0e0; display:flex; align-items:center; justify-content:center; font-size:30px;">👤</div>'
    badge_html = BLUE_TICK_SVG if is_verified else ""
    
    return f'''
    <div style="display: flex; align-items: center; gap: 15px; background: #ffffff; padding: 15px; border-radius: 12px; border: 1px solid #e1e8ed; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
        <div>{img_html}</div>
        <div>
            <div style="display: flex; align-items: center; font-weight: 800; font-size: 22px; color: #0F1419; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
                <span>{display_name}</span>
                {badge_html}
            </div>
            <p style="color: #536471; font-size: 14px; margin: 2px 0 0 0; font-weight: 500;">🛡️ {subtitle}</p>
        </div>
    </div>
    '''

def show_auto_moving_banner():
    ad_html = f"""
    <div style="text-align:center; margin: 15px 0;">
        <a href="{SMART_LINK}" target="_blank" style="text-decoration:none;">
            <div style="background: linear-gradient(90deg, #1877F2, #00c853); 
                        color: #fff; padding: 14px; border-radius: 12px; 
                        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
                        border: 2px solid #ffffff; font-family: sans-serif;">
                <span style="font-size: 16px; font-weight: bold;">⚡ GLOBAL AUTOMATIC MONETIZATION ACTIVE ⚡</span><br>
                <span style="font-size: 12px;">Click to Boost Earnings & Claim Reward Bonus!</span>
            </div>
        </a>
    </div>
    """
    components.html(ad_html, height=100)

# 4. Custom Global Styling (Fixing Invisibility and UI Bugs)
st.markdown("""
    <style>
    .stApp { background-color: #f7f9fa; color: #0f1419; }
    
    /* Input Field Fix for Visibility */
    div[data-baseweb="input"] > div, div[data-baseweb="textarea"] > div, div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #cccccc !important;
        border-radius: 8px !important;
    }
    textarea, input {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    
    .long-video-card {
        background: #ffffff;
        border: 1px solid #e1e8ed;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    }
    .monetization-box {
        background: linear-gradient(135deg, #00b09b, #96c93d);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin-top: 15px;
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .btn-direct { display: block; width: 100%; padding: 12px; margin: 8px 0; color: white !important; text-align: center; border-radius: 10px; font-weight: bold; text-decoration: none; font-size: 14px; }
    .bg-1 { background: linear-gradient(135deg, #FF416C, #FF4B2B); }
    .bg-2 { background: linear-gradient(135deg, #1DE9B6, #26A69A); }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ BT AI Book — Verified Network")

# 5. Session State Initialization
if 'user' not in st.session_state:
    st.session_state.user = None
    st.session_state.pic = None
    st.session_state.is_verified = 1

# 6. Sidebar: Authentication
st.sidebar.header("📸 Authentication")

if not st.session_state.user:
    u_name = st.sidebar.text_input("Username")
    camera_photo = st.sidebar.camera_input("Take Face Scan", key="face_cam")
    
    if u_name and camera_photo:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (u_name,))
        user_data = cursor.fetchone()
        
        if user_data:
            if st.sidebar.button("🔓 Login with Face ID"):
                st.session_state.user = u_name
                st.session_state.pic = user_data['profile_pic']
                st.session_state.is_verified = user_data['is_verified']
                conn.close()
                st.rerun()
        else:
            if st.sidebar.button("✨ Create Account"):
                fname = os.path.join(PROFILE_DIR, f"p_{uuid.uuid4()}.jpg")
                with open(fname, "wb") as f:
                    f.write(camera_photo.getvalue())
                
                today_str = datetime.now().strftime("%Y-%m-%d")
                cursor.execute("INSERT INTO users (username, full_name, profile_pic, is_verified, created_at) VALUES (?, ?, ?, ?, ?)", 
                               (u_name, u_name, fname, 1, today_str))
                conn.commit()
                conn.close()
                
                st.session_state.user = u_name
                st.session_state.pic = fname
                st.session_state.is_verified = 1
                st.sidebar.success("🎉 Account Created Successfully!")
                st.rerun()
else:
    if st.session_state.pic and os.path.exists(st.session_state.pic):
        st.sidebar.image(st.session_state.pic, width=90)
    
    st.sidebar.markdown(f"Welcome, **{st.session_state.user}**", unsafe_allow_html=True)
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.session_state.pic = None
        st.session_state.is_verified = 1
        st.rerun()

tab = st.sidebar.radio("Navigation", ["🌍 World Feed", "👤 My Profile & Earnings", "📤 Upload Video"])

# 7. World Feed Section
if tab == "🌍 World Feed":
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM videos")
        rows = cursor.fetchall()
        data = [dict(row) for row in rows]
        random.shuffle(data)
        
        if not data:
            st.info("No videos uploaded yet.")

        for index, v in enumerate(data):
            v_id = str(v['id'])
            v_type = v.get("video_type", "long")
            uploader_name = v.get("uploader_name", "Unknown User")
            
            st.markdown('<div class="long-video-card">', unsafe_allow_html=True)
            
            # Render Verified Creator Header
            user_header = render_profile_header(uploader_name, pic_url=None, is_verified=1, subtitle=f"Format: {v_type.upper()}")
            st.markdown(user_header, unsafe_allow_html=True)
            st.write("")
            
            if v.get("title"):
                st.markdown(f"#### {v.get('title')}")
            
            if os.path.exists(v['video_url']):
                st.video(v['video_url'])
            else:
                st.error("Video file lost.")
            
            # Stats Update
            new_views = v.get("views", 0) + 1
            cursor.execute("UPDATE videos SET views = ? WHERE id = ?", (new_views, v_id))
            conn.commit()

            show_auto_moving_banner()

            st.write(f"👁️ **{format_value(new_views)}** Views | ❤️ **{format_value(v.get('likes', 0))}** Likes")
            st.markdown(f'''
                <a href="{SMART_LINK}" target="_blank" class="btn-direct bg-1">💰 Claim Monetization Reward</a>
                <a href="{SMART_LINK}" target="_blank" class="btn-direct bg-2">💎 Premium Bonus Link</a>
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

# 8. Profile, Earnings & Account Settings Tab
elif tab == "👤 My Profile & Earnings":
    if not st.session_state.user:
        st.warning("Please login to access your profile.")
    else:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE username = ?", (st.session_state.user,))
        user_info = cursor.fetchone()
        
        cursor.execute("SELECT * FROM videos WHERE uploader_name = ?", (st.session_state.user,))
        my_videos = [dict(r) for r in cursor.fetchall()]
        
        total_likes = sum([v.get("likes", 0) for v in my_videos])
        total_views = sum([v.get("views", 0) for v in my_videos])
        
        # Original Verification Badge Header
        display_name = user_info['full_name'] if user_info and user_info['full_name'] else st.session_state.user
        st.markdown(render_profile_header(display_name, pic_url=None, is_verified=1), unsafe_allow_html=True)
        st.write("")
        
        st.write(f"📹 Uploaded Videos: **{len(my_videos)}** | ❤️ Likes: **{format_value(total_likes)}** | 👁️ Total Views: **{format_value(total_views)}**")

        # Monetization Dashboard
        st.markdown(f'''
            <div class="monetization-box">
                <h3 style="margin:0;">🌐 Global Monetization Dashboard</h3>
                <p style="margin: 5px 0;">✅ <b>Status: Active & Global Revenue Unlocked</b></p>
                <h2 style="margin: 10px 0; color: #ffffff;">💰 Est. Earnings: ${(total_views * 0.002) + (total_likes * 0.005):.2f} USD</h2>
            </div>
        ''', unsafe_allow_html=True)

        # Tabs inside Profile
        p_tab1, p_tab2, p_tab3 = st.tabs(["💳 Payout Methods", "⚙️ Account & NID Settings", "🎥 Manage Videos"])
        
        with p_tab1:
            st.subheader("💳 Global Bank & Payment Setup")
            with st.form("payout_form"):
                pay_method = st.selectbox("Select Payment Method", [
                    "Visa / Mastercard Debit Card",
                    "International Bank Transfer (SWIFT/IBAN)",
                    "Mobile Financial Service (bKash / Nagad)",
                    "PayPal / Crypto (USDT)"
                ], index=0)
                
                curr_details = user_info['account_details'] if user_info and user_info['account_details'] else ""
                acc_info = st.text_area("Account Details (Card Number, Bank Name, Account No, IBAN or Mobile Number)", value=curr_details)
                
                submit_pay = st.form_submit_button("💾 Save Payment Settings")
                if submit_pay:
                    cursor.execute("UPDATE users SET payment_method = ?, account_details = ? WHERE username = ?", 
                                   (pay_method, acc_info, st.session_state.user))
                    conn.commit()
                    st.success("✅ Payment Details Updated Successfully!")
                    st.rerun()

        with p_tab2:
            st.subheader("⚙️ Identity & Profile Settings (NID Verification)")
            with st.form("profile_settings_form"):
                full_name_input = st.text_input("Full Name (English / As per NID)", value=user_info['full_name'] if user_info and user_info['full_name'] else "")
                nid_input = st.text_input("NID Card Number", value=user_info['nid_number'] if user_info and user_info['nid_number'] else "")
                address_input = st.text_area("Address (Bangladesh / Local Address)", value=user_info['address'] if user_info and user_info['address'] else "")
                
                save_profile = st.form_submit_button("💾 Update Profile Data")
                if save_profile:
                    cursor.execute("UPDATE users SET full_name = ?, nid_number = ?, address = ? WHERE username = ?",
                                   (full_name_input, nid_input, address_input, st.session_state.user))
                    conn.commit()
                    st.success("✅ Profile & Identity details saved!")
                    st.rerun()

        with p_tab3:
            st.subheader("🎥 Manage & Delete Videos")
            if not my_videos:
                st.info("No uploaded videos found.")
            else:
                for idx, mv in enumerate(my_videos):
                    col_vid, col_del = st.columns([3, 1])
                    with col_vid:
                        st.write(f"**{mv.get('title', 'Untitled')}** ({mv.get('views', 0)} Views)")
                        if os.path.exists(mv['video_url']):
                            st.video(mv['video_url'])
                    with col_del:
                        st.write("")
                        st.write("")
                        if st.button("🗑️ Delete Video", key=f"del_{mv['id']}"):
                            if os.path.exists(mv['video_url']):
                                os.remove(mv['video_url'])
                            cursor.execute("DELETE FROM videos WHERE id = ?", (mv['id'],))
                            conn.commit()
                            st.success("Video Deleted!")
                            st.rerun()
                    st.divider()

        conn.close()

# 9. Upload Video Section
elif tab == "📤 Upload Video":
    if not st.session_state.user:
        st.warning("Please login to upload videos.")
    else:
        st.subheader("📤 Upload New Video")
        v_title = st.text_input("Video Title")
        v_type = st.selectbox("Video Type", ["Long Video", "Short Video"])
        file = st.file_uploader("Select MP4 Video File", type=['mp4'])
        
        if st.button("🚀 Publish Video") and file:
            today = datetime.now().strftime("%Y-%m-%d")
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM videos WHERE uploader_name = ? AND created_at >= ?", (st.session_state.user, today))
            check_data = cursor.fetchall()
            
            if check_data and len(check_data) >= 5:
                st.error("Upload limit reached! Max 5 videos per day.")
                conn.close()
            else:
                with st.spinner("Publishing video..."):
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
                    st.success("🎉 Video Uploaded Successfully!")
                    st.rerun()
