import streamlit as st
import uuid
import random
import os
import sqlite3
import base64
from datetime import datetime
import streamlit.components.v1 as components

# 1. Page Configuration
st.set_page_config(page_title="BD AI book — Verified Social Network", layout="wide", initial_sidebar_state="expanded")

# Meta Tags & Monetization Scripts
components.html(
    """
    <meta name="msvalidate.01" content="e776b8ce73ea3dcc07551e8a021a0907">
    <meta name="monetag" content="5cc1b7ba5cb29eff802ce49009f87e2b">
    """,
    height=0,
)

SMART_LINK = "https://omg10.com/4/10954816"

# 2. Local Storage and Database Setup
DB_FILE = "local_storage.db"
VIDEO_DIR = "stored_videos"
IMAGE_DIR = "stored_images"
PROFILE_DIR = "stored_profiles"

for folder in [VIDEO_DIR, IMAGE_DIR, PROFILE_DIR]:
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
    
    for col in ["full_name", "nid_number", "address"]:
        try:
            cursor.execute(f"ALTER TABLE users ADD COLUMN {col} TEXT")
        except Exception:
            pass

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
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id TEXT PRIMARY KEY,
            uploader_name TEXT,
            uploader_pic TEXT,
            content TEXT,
            image_url TEXT,
            likes INTEGER DEFAULT 0,
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

def get_image_base64(image_path):
    if image_path and os.path.exists(image_path):
        try:
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode('utf-8')
        except Exception:
            return None
    return None

def show_verified_profile(display_name, profile_pic_path=None, subtitle="Official Global Verified Creator"):
    b64_img = get_image_base64(profile_pic_path)
    if b64_img:
        img_html = f'<img src="data:image/jpeg;base64,{b64_img}" style="width:50px; height:50px; border-radius:50%; object-fit:cover; border:2px solid #00c853;">'
    else:
        img_html = '<div style="width:50px; height:50px; border-radius:50%; background:#2a2a2a; color:#fff; display:flex; align-items:center; justify-content:center; font-size:24px;">👤</div>'

    html_code = f"""<div style="display: flex; align-items: center; gap: 12px; background: #18191a; padding: 12px; border-radius: 12px; border: 1px solid #2d2f31; margin-bottom: 12px;">
<div>{img_html}</div>
<div>
<div style="display: flex; align-items: center; font-weight: 700; font-size: 17px; color: #e4e6eb; font-family: sans-serif;">
<span>{display_name}</span>
<svg width="18" height="18" viewBox="0 0 24 24" fill="none" style="margin-left: 6px;"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" fill="#00c853"/></svg>
</div>
<div style="color: #b0b3b8; font-size: 12px; margin-top: 1px;">{subtitle}</div>
</div>
</div>"""
    st.markdown(html_code, unsafe_allow_html=True)

def show_auto_moving_banner():
    ad_html = f"""
    <div style="text-align:center; margin: 15px 0;">
        <a href="{SMART_LINK}" target="_blank" style="text-decoration:none;">
            <div style="background: linear-gradient(90deg, #1877F2, #00c853); color: #fff; padding: 14px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); border: 1px solid #3a3b3c; font-family: sans-serif;">
                <span style="font-size: 15px; font-weight: bold;">⚡ GLOBAL AUTOMATIC MONETIZATION ACTIVE ⚡</span><br>
                <span style="font-size: 12px;">Click to Boost Earnings & Claim Reward Bonus!</span>
            </div>
        </a>
    </div>
    """
    components.html(ad_html, height=95)

# 4. Custom Styling (Dark UI Theme)
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: #e4e6eb; }
    
    div[data-baseweb="input"] > div, div[data-baseweb="textarea"] > div, div[data-baseweb="select"] > div {
        background-color: #242526 !important;
        color: #ffffff !important;
        border: 1px solid #3a3b3c !important;
    }
    textarea, input {
        color: #ffffff !important;
        background-color: #242526 !important;
    }
    
    .feed-card {
        background: #18191a;
        border: 1px solid #2d2f31;
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 20px;
    }
    
    .scrolle-header {
        font-size: 18px;
        font-weight: bold;
        color: #1877F2;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .monetization-box {
        background: linear-gradient(135deg, #00b09b, #96c93d);
        color: white;
        padding: 18px;
        border-radius: 12px;
        margin-top: 15px;
        margin-bottom: 15px;
    }
    .btn-direct { display: block; width: 100%; padding: 10px; margin: 6px 0; color: white !important; text-align: center; border-radius: 8px; font-weight: bold; text-decoration: none; font-size: 14px; }
    .bg-1 { background: linear-gradient(135deg, #FF416C, #FF4B2B); }
    .bg-2 { background: linear-gradient(135deg, #1DE9B6, #26A69A); }

    /* Shorts Full-screen Scroll Layout */
    .shorts-container {
        height: 80vh;
        overflow-y: scroll;
        scroll-snap-type: y mandatory;
        border-radius: 16px;
        max-width: 450px;
        margin: 0 auto;
        background: #000;
    }
    .short-card {
        scroll-snap-align: start;
        height: 80vh;
        position: relative;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        background: #000;
        border-bottom: 2px solid #222;
    }
    .short-video {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("BD AI book — Verified Social Network")

# 5. Session State
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
    
    st.sidebar.markdown(f"Welcome, **{st.session_state.user}**")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.session_state.pic = None
        st.session_state.is_verified = 1
        st.rerun()

# --- Navigation tab selection updated to include Scrolle Shorts Feed ---
tab = st.sidebar.radio("Navigation", ["🌍 World Feed", "📱 Scrolle Shorts Feed", "👤 My Profile & Earnings", "📤 Create Post / Upload"])

# 7. World Feed
if tab == "🌍 World Feed":
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # --- Top Scrolle (Shorts Video) Preview Section ---
    try:
        cursor.execute("SELECT * FROM videos WHERE video_type = 'short'")
        short_videos = [dict(r) for r in cursor.fetchall()]
        
        if short_videos:
            st.markdown('<div class="scrolle-header">▶️ Scrolle Shorts</div>', unsafe_allow_html=True)
            cols = st.columns(min(len(short_videos), 3))
            for i, sv in enumerate(short_videos[:3]):
                with cols[i]:
                    st.markdown(f"**{sv.get('uploader_name', 'User')}** ✔️")
                    if os.path.exists(sv['video_url']):
                        st.video(sv['video_url'], format="video/mp4")
                    st.caption(f"👁️ {format_value(sv.get('views', 0))} views")
            st.divider()
    except Exception as e:
        pass

    # --- Posts & Video Feed ---
    try:
        cursor.execute("SELECT * FROM videos WHERE video_type != 'short'")
        videos = [dict(row) for row in cursor.fetchall()]
        
        cursor.execute("SELECT * FROM posts")
        posts = [dict(row) for row in cursor.fetchall()]
        
        combined_feed = videos + posts
        random.shuffle(combined_feed)
        
        if not combined_feed:
            st.info("No feeds uploaded yet.")

        for index, item in enumerate(combined_feed):
            item_id = str(item['id'])
            uploader_name = item.get("uploader_name", "Unknown User")
            uploader_pic = item.get("uploader_pic", None)
            created_at = item.get("created_at", "Recently")
            
            st.markdown('<div class="feed-card">', unsafe_allow_html=True)
            show_verified_profile(uploader_name, profile_pic_path=uploader_pic, subtitle=f"Posted {created_at}")
            
            if "content" in item and item["content"]:
                st.markdown(f"### {item['content']}")
                
            if "image_url" in item and item["image_url"] and os.path.exists(item["image_url"]):
                st.image(item["image_url"], use_container_width=True)
                
            if "video_url" in item and os.path.exists(item['video_url']):
                if item.get("title"):
                    st.markdown(f"#### {item.get('title')}")
                st.video(item['video_url'], format="video/mp4")
                
                new_views = item.get("views", 0) + 1
                cursor.execute("UPDATE videos SET views = ? WHERE id = ?", (new_views, item_id))
                conn.commit()

            show_auto_moving_banner()

            st.write(f"❤️ **{format_value(item.get('likes', 0))}** Likes")
            st.markdown(f'''
                <a href="{SMART_LINK}" target="_blank" class="btn-direct bg-1">💰 Claim Monetization Reward</a>
                <a href="{SMART_LINK}" target="_blank" class="btn-direct bg-2">💎 Premium Bonus Link</a>
            ''', unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button(f"❤️ Like ({format_value(item.get('likes', 0))})", key=f"lk_{item_id}_{index}"):
                    table_name = "posts" if "content" in item else "videos"
                    cursor.execute(f"UPDATE {table_name} SET likes = likes + 1 WHERE id = ?", (item_id,))
                    conn.commit()
                    st.rerun()
            with c2:
                if st.button(f"➕ Follow", key=f"fl_{item_id}_{index}"):
                    st.toast("Followed successfully!")
                    
            st.markdown('</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Feed Error: {e}")
    finally:
        conn.close()

# 📱 --- NEW: Scrolle Shorts Full Feed (TikTok/Shorts Style Vertical Scroll) ---
elif tab == "📱 Scrolle Shorts Feed":
    st.subheader("📱 Scrolle Shorts")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM videos WHERE video_type = 'short' ORDER BY created_at DESC")
    short_vids = [dict(r) for r in cursor.fetchall()]
    conn.close()

    if not short_vids:
        st.info("কোনো শর্টস ভিডিও পাওয়া যায়নি। নতুন শর্টস আপলোড করুন!")
    else:
        # Loop through short videos and present vertical player cards
        for idx, sv in enumerate(short_vids):
            st.markdown("---")
            col_vid, col_actions = st.columns([3, 1])
            with col_vid:
                show_verified_profile(sv.get("uploader_name", "User"), profile_pic_path=sv.get("uploader_pic"), subtitle="Scrolle Creator")
                st.markdown(f"**{sv.get('title', 'Short Video')}**")
                if os.path.exists(sv['video_url']):
                    st.video(sv['video_url'], format="video/mp4")
            
            with col_actions:
                st.write(" ")
                st.write(" ")
                if st.button(f"❤️ {format_value(sv.get('likes', 0))}", key=f"s_like_{sv['id']}"):
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute("UPDATE videos SET likes = likes + 1 WHERE id = ?", (sv['id'],))
                    conn.commit()
                    conn.close()
                    st.rerun()
                st.caption(f"👁️ {format_value(sv.get('views', 0))}")
                if st.button("➕ Follow", key=f"s_fol_{sv['id']}"):
                    st.toast("Followed!")
                st.markdown(f'<a href="{SMART_LINK}" target="_blank" style="text-decoration:none;">💰 Earn</a>', unsafe_allow_html=True)

# 8. Profile Section
elif tab == "👤 My Profile & Earnings":
    if not st.session_state.user:
        st.warning("Please login to view your profile.")
    else:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE username = ?", (st.session_state.user,))
        raw_user = cursor.fetchone()
        user_info = dict(raw_user) if raw_user else {}
        
        cursor.execute("SELECT * FROM videos WHERE uploader_name = ?", (st.session_state.user,))
        my_videos = [dict(r) for r in cursor.fetchall()]
        
        total_likes = sum([v.get("likes", 0) for v in my_videos])
        total_views = sum([v.get("views", 0) for v in my_videos])
        
        display_name = user_info.get('full_name') if user_info.get('full_name') else st.session_state.user
        pic_path = user_info.get('profile_pic', st.session_state.pic)
        
        show_verified_profile(display_name, profile_pic_path=pic_path, subtitle="Official Verified Creator")
        
        st.write(f"📹 Uploads: **{len(my_videos)}** | ❤️ Likes: **{format_value(total_likes)}** | 👁️ Views: **{format_value(total_views)}**")

        st.markdown(f'''
            <div class="monetization-box">
                <h3 style="margin:0; color:#fff;">🌐 Global Monetization Dashboard</h3>
                <p style="margin: 5px 0;">✅ <b>Status: Active & Global Revenue Unlocked</b></p>
                <h2 style="margin: 10px 0; color: #ffffff;">💰 Est. Earnings: ${(total_views * 0.002) + (total_likes * 0.005):.2f} USD</h2>
            </div>
        ''', unsafe_allow_html=True)

        p_tab1, p_tab2, p_tab3 = st.tabs(["💳 Payout Methods", "⚙️ Account & NID Settings", "🎥 Manage Content"])
        
        with p_tab1:
            st.subheader("💳 Global Bank & Payment Setup")
            with st.form("payout_form"):
                pay_method = st.selectbox("Select Payment Method", [
                    "Visa / Mastercard Debit Card",
                    "International Bank Transfer (SWIFT/IBAN)",
                    "Mobile Financial Service (bKash / Nagad)",
                    "PayPal / Crypto (USDT)"
                ], index=0)
                
                curr_details = user_info.get('account_details', '') or ''
                acc_info = st.text_area("Account Details (Card Number, Bank Name, Account No, IBAN or Mobile Number)", value=curr_details)
                
                submit_pay = st.form_submit_button("💾 Save Payment Settings")
                if submit_pay:
                    cursor.execute("UPDATE users SET payment_method = ?, account_details = ? WHERE username = ?", 
                                   (pay_method, acc_info, st.session_state.user))
                    conn.commit()
                    st.success("✅ Payment Details Updated Successfully!")
                    st.rerun()

        with p_tab2:
            st.subheader("⚙️ Identity & Profile Settings")
            with st.form("profile_settings_form"):
                full_name_input = st.text_input("Full Name (English / As per NID)", value=user_info.get('full_name', '') or '')
                nid_input = st.text_input("NID Card Number", value=user_info.get('nid_number', '') or '')
                address_input = st.text_area("Address (Bangladesh / Local Address)", value=user_info.get('address', '') or '')
                
                save_profile = st.form_submit_button("💾 Update Profile Data")
                if save_profile:
                    cursor.execute("UPDATE users SET full_name = ?, nid_number = ?, address = ? WHERE username = ?",
                                   (full_name_input, nid_input, address_input, st.session_state.user))
                    conn.commit()
                    st.success("✅ Profile & Identity details saved!")
                    st.rerun()

        with p_tab3:
            st.subheader("🎥 Manage Videos")
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
                        if st.button("🗑️ Delete", key=f"del_{mv['id']}"):
                            if os.path.exists(mv['video_url']):
                                os.remove(mv['video_url'])
                            cursor.execute("DELETE FROM videos WHERE id = ?", (mv['id'],))
                            conn.commit()
                            st.success("Deleted!")
                            st.rerun()
                    st.divider()

        conn.close()

# 9. Upload & Post Creation Section
elif tab == "📤 Create Post / Upload":
    if not st.session_state.user:
        st.warning("Please login to create a post or upload.")
    else:
        post_type = st.radio("Choose What to Share", ["📝 Photo & Text Post", "🎥 Video / Scrolle Shorts"])
        
        if post_type == "📝 Photo & Text Post":
            st.subheader("📝 Create Facebook-Style Post")
            post_text = st.text_area("What's on your mind?")
            img_file = st.file_uploader("Upload Photo (JPG/PNG)", type=['jpg', 'png', 'jpeg'])
            
            if st.button("🚀 Publish Post"):
                img_path = None
                if img_file:
                    img_path = os.path.join(IMAGE_DIR, f"img_{uuid.uuid4()}.jpg")
                    with open(img_path, "wb") as f:
                        f.write(img_file.getvalue())
                        
                today_str = datetime.now().strftime("%Y-%m-%d %H:%M")
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO posts (id, uploader_name, uploader_pic, content, image_url, likes, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (str(uuid.uuid4()), st.session_state.user, st.session_state.pic, post_text, img_path, random.randint(5, 20), today_str))
                conn.commit()
                conn.close()
                st.success("🎉 Post Published Successfully!")
                st.rerun()
                
        else:
            st.subheader("📤 Upload Video or Scrolle Shorts")
            v_title = st.text_input("Video Title")
            v_type = st.selectbox("Video Format", ["Long Video", "Scrolle Short Video"])
            file = st.file_uploader("Select MP4 Video File", type=['mp4'])
            
            if st.button("🚀 Publish Video") and file:
                today = datetime.now().strftime("%Y-%m-%d")
                conn = get_db_connection()
                cursor = conn.cursor()
                
                v_id = str(uuid.uuid4())
                v_name = os.path.join(VIDEO_DIR, f"v_{v_id}.mp4")
                
                with open(v_name, "wb") as f_dst:
                    f_dst.write(file.getvalue())
                
                video_kind = "short" if "Short" in v_type else "long"
                
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
