import streamlit as st
from supabase import create_client
import uuid

# 1. Database Connection
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

st.set_page_config(page_title="BT AI book", layout="wide")

# 2. Optimized CSS (বাটন এবং কার্ড ডিজাইন)
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .video-card { 
        background: #0d0d0d; border: 1px solid #333; border-radius: 15px; 
        padding: 15px; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    .user-avatar { 
        width: 45px; height: 45px; border-radius: 50%; 
        border: 2px solid #00ff00; object-fit: cover; margin-right: 10px; 
    }
    .username-text { font-weight: bold; font-size: 16px; color: #fff; }
    .stat-box { font-size: 14px; color: #00ff00; font-weight: bold; margin-right: 15px; }
    
    /* কাস্টম বাটন স্টাইল */
    .btn-reward { 
        display: block; width: 100%; padding: 12px; margin: 10px 0; 
        background: linear-gradient(135deg, #ed1c24, #aa0000); 
        color: white !important; text-align: center; border-radius: 8px; 
        font-weight: bold; text-decoration: none;
    }
    iframe { border-radius: 10px; margin: 10px 0; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ BT AI book")

# 3. Session State for Profile
if 'user' not in st.session_state:
    st.session_state.user = None
    st.session_state.pic = None

# Sidebar Profile
if not st.session_state.user:
    st.sidebar.header("Login")
    u_name = st.sidebar.text_input("Username")
    u_pic = st.sidebar.file_uploader("Upload Image", type=['jpg', 'png'])
    if st.sidebar.button("Enter"):
        if u_name and u_pic:
            fname = f"profile_{uuid.uuid4()}.jpg"
            supabase.storage.from_("videos").upload(path=fname, file=u_pic.getvalue())
            st.session_state.pic = supabase.storage.from_("videos").get_public_url(fname)
            st.session_state.user = u_name
            st.rerun()
else:
    st.sidebar.image(st.session_state.pic, width=80)
    st.sidebar.write(f"User: **{st.session_state.user}**")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

tab = st.sidebar.radio("Navigation", ["🌍 World Feed", "📤 Upload Video"])

# 4. Feed Section
if tab == "🌍 World Feed":
    try:
        data = supabase.table("videos").select("*").order("created_at", desc=True).execute().data
        for v in data:
            st.markdown('<div class="video-card">', unsafe_allow_html=True)
            
            # Header: Profile & Name
            st.markdown(f'''
                <div style="display:flex; align-items:center; margin-bottom:10px;">
                    <img src="{v.get('uploader_pic', '')}" class="user-avatar">
                    <span class="username-text">{v.get('uploader_name', 'BT User')}</span>
                </div>
            ''', unsafe_allow_html=True)

            # --- AD 1 (Top Banner) ---
            st.components.v1.html("""
                <div style="text-align:center;">
                    <script type="text/javascript">
                    atOptions = { 'key' : '5327bebb34c787d2ccfb1c36bcfa9d6e', 'format' : 'iframe', 'height' : 250, 'width' : 300, 'params' : {} };
                    </script>
                    <script src="https://www.highperformanceformat.com/5327bebb34c787d2ccfb1c36bcfa9d6e/invoke.js"></script>
                </div>
            """, height=260)

            # Video Player
            st.video(v['video_url'])
            
            # Stats (Real-time updates)
            st.markdown(f'''
                <div style="margin: 10px 0;">
                    <span class="stat-box">❤️ {v.get("likes", 0)} Likes</span>
                    <span class="stat-box">👤 {v.get("followers", 0)} Followers</span>
                </div>
            ''', unsafe_allow_html=True)
            
            # Interaction Buttons
            c1, c2 = st.columns(2)
            with c1:
                if st.button(f"❤️ Like", key=f"l_{v['id']}"):
                    supabase.table("videos").update({"likes": v.get("likes", 0) + 1}).eq("id", v['id']).execute()
                    st.rerun()
            with c2:
                if st.button(f"➕ Follow", key=f"f_{v['id']}"):
                    supabase.table("videos").update({"followers": v.get("followers", 0) + 1}).eq("id", v['id']).execute()
                    st.rerun()

            # --- AD 2 (Middle Thin Banner) ---
            st.components.v1.html("""
                <div style="text-align:center;">
                    <script type="text/javascript">
                    atOptions = { 'key' : '342950879f2064f7255ad047622381c8', 'format' : 'iframe', 'height' : 50, 'width' : 320, 'params' : {} };
                    </script>
                    <script src="https://www.highperformanceformat.com/342950879f2064f7255ad047622381c8/invoke.js"></script>
                </div>
            """, height=70)

            # Reward Button
            st.markdown(f'<a href="https://www.profitablecpmratenetwork.com/tgt6azn6?key=e753cbd6d9bae06d67051ed846419521" target="_blank" class="btn-reward">💎 Get Diamond Reward</a>', unsafe_allow_html=True)

            # --- AD 3 (Bottom Large Adzilla Style) ---
            st.components.v1.html("""
                <div style="text-align:center;">
                    <script async="async" data-cfasync="false" src="https://pl29264300.profitablecpmratenetwork.com/3d5c1921120aef030a2a6dd72337ba1d/invoke.js"></script>
                    <div id="container-3d5c1921120aef030a2a6dd72337ba1d"></div>
                </div>
            """, height=250)
            
            st.markdown('</div>', unsafe_allow_html=True)
    except:
        st.error("Connecting to server...")

# 5. Upload Section
elif tab == "📤 Upload Video":
    if st.session_state.user:
        v_file = st.file_uploader("Select Video (MP4)", type=['mp4'])
        if st.button("🚀 Publish") and v_file:
            with st.spinner("Uploading..."):
                v_id = f"v_{uuid.uuid4()}.mp4"
                supabase.storage.from_("videos").upload(path=v_id, file=v_file.getvalue())
                url = supabase.storage.from_("videos").get_public_url(v_id)
                supabase.table("videos").insert({
                    "video_url": url, "uploader_name": st.session_state.user,
                    "uploader_pic": st.session_state.pic, "likes": 0, "followers": 0
                }).execute()
                st.success("Success!")
    else:
        st.warning("Please login first!")
