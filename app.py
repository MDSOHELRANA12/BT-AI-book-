import streamlit as st
from supabase import create_client
import uuid

# 1. Database Connection
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

st.set_page_config(page_title="BT AI book", layout="wide")

# 2. Optimized CSS
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .video-card { 
        background: #0d0d0d; border: 1px solid #333; border-radius: 15px; 
        padding: 15px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    .user-avatar { 
        width: 50px; height: 50px; border-radius: 50%; 
        border: 2px solid #00ff00; object-fit: cover; margin-right: 12px; 
    }
    .username-text { font-weight: bold; font-size: 18px; color: #fff; }
    .stat-box { font-size: 14px; color: #00ff00; font-weight: bold; margin-right: 20px; }
    
    .btn-revenue { 
        display: block; width: 100%; padding: 14px; margin: 8px 0; 
        background: linear-gradient(135deg, #ed1c24, #aa0000); 
        color: white !important; text-align: center; border-radius: 8px; 
        font-weight: bold; text-decoration: none; border: 1px solid rgba(255,255,255,0.2);
    }
    iframe { border-radius: 10px; border: none; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ BT AI book")

# 3. Profile Management
if 'user' not in st.session_state:
    st.session_state.user = None
    st.session_state.pic = None

if not st.session_state.user:
    st.sidebar.header("Profile Setup")
    name_in = st.sidebar.text_input("Username")
    file_in = st.sidebar.file_uploader("Profile Image", type=['jpg', 'png'])
    if st.sidebar.button("Create Account"):
        if name_in and file_in:
            fname = f"profile_{uuid.uuid4()}.jpg"
            supabase.storage.from_("videos").upload(path=fname, file=file_in.getvalue())
            st.session_state.pic = supabase.storage.from_("videos").get_public_url(fname)
            st.session_state.user = name_in
            st.rerun()
else:
    st.sidebar.image(st.session_state.pic, width=100)
    st.sidebar.write(f"Logged in as: **{st.session_state.user}**")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

tab = st.sidebar.radio("Go To", ["🌍 World Feed", "📤 Upload Video"])

# 4. Global World Feed
if tab == "🌍 World Feed":
    try:
        videos = supabase.table("videos").select("*").order("created_at", desc=True).execute().data
        
        for v in videos:
            st.markdown('<div class="video-card">', unsafe_allow_html=True)
            
            # User Info & Follow Status
            st.markdown(f'''
                <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:10px;">
                    <div style="display:flex; align-items:center;">
                        <img src="{v.get('uploader_pic', '')}" class="user-avatar">
                        <span class="username-text">{v.get('uploader_name', 'User')}</span>
                    </div>
                </div>
            ''', unsafe_allow_html=True)

            # --- TOP ADS (ব্যানার ১ - ৩০০x২৫০) ---
            st.components.v1.html(f"""
                <div style="text-align:center;">
                    <script>
                    atOptions = {{ 'key' : '5327bebb34c787d2ccfb1c36bcfa9d6e', 'format' : 'iframe', 'height' : 250, 'width' : 300, 'params' : {{}} }};
                    </script>
                    <script src="https://www.highperformanceformat.com/5327bebb34c787d2ccfb1c36bcfa9d6e/invoke.js"></script>
                </div>
            """, height=260)

            # Video
            st.video(v['video_url'])
            
            # Real Follow & Like Counter
            st.markdown(f'<div><span class="stat-box">❤️ {v.get("likes", 0)} Likes</span> <span class="stat-box">👤 {v.get("followers", 0)} Followers</span></div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"❤️ Like", key=f"lk_{v['id']}"):
                    supabase.table("videos").update({"likes": v.get("likes", 0) + 1}).eq("id", v['id']).execute()
                    st.rerun()
            with col2:
                if st.button(f"➕ Follow", key=f"fol_{v['id']}"):
                    supabase.table("videos").update({"followers": v.get('followers', 0) + 1}).eq("id", v['id']).execute()
                    st.toast(f"Followed {v.get('uploader_name')}")
                    st.rerun()

            # --- BOTTOM ADS (ব্যানার ২ - ৩২০x৫০) ---
            st.components.v1.html(f"""
                <div style="text-align:center;">
                    <script>
                    atOptions = {{ 'key' : '342950879f2064f7255ad047622381c8', 'format' : 'iframe', 'height' : 50, 'width' : 320, 'params' : {{}} }};
                    </script>
                    <script src="https://www.highperformanceformat.com/342950879f2064f7255ad047622381c8/invoke.js"></script>
                </div>
            """, height=70)
            
            # Direct Earnings Buttons
            st.markdown(f'<a href="https://www.profitablecpmratenetwork.com/tgt6azn6?key=e753cbd6d9bae06d67051ed846419521" target="_blank" class="btn-revenue">💎 Get Diamond Reward</a>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    except:
        st.error("Server Error!")

# 5. Video Uploading
elif tab == "📤 Upload Video":
    if st.session_state.user:
        up_file = st.file_uploader("Select Video", type=['mp4'])
        if st.button("🚀 Upload Now") and up_file:
            with st.spinner("Publishing..."):
                vid_id = f"vid_{uuid.uuid4()}.mp4"
                supabase.storage.from_("videos").upload(path=vid_id, file=up_file.getvalue())
                v_url = supabase.storage.from_("videos").get_public_url(vid_id)
                supabase.table("videos").insert({
                    "video_url": v_url, "uploader_name": st.session_state.user,
                    "uploader_pic": st.session_state.pic, "likes": 0, "followers": 0
                }).execute()
                st.success("Video Live!")
    else:
        st.warning("Please Create Profile first!")
