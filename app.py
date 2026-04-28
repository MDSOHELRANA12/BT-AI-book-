import streamlit as st
from supabase import create_client
import uuid

# 1. Database Connection (BT AI book Backend)
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

# Platform Branding
st.set_page_config(page_title="BT AI book", layout="wide")

# 2. Premium Professional CSS (Global Standard)
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .video-card { 
        background: #0d0d0d; 
        border: 1px solid #333; 
        border-radius: 15px; 
        padding: 15px; 
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    
    /* Profile Header Styling */
    .profile-container { display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; }
    .user-box { display: flex; align-items: center; }
    .user-avatar { 
        width: 50px; height: 50px; 
        border-radius: 50%; 
        border: 2px solid #00ff00; 
        object-fit: cover; 
        margin-right: 12px; 
    }
    .username-text { font-weight: bold; font-size: 18px; color: #ffffff; text-transform: capitalize; }
    
    /* Plus Button */
    .follow-btn { 
        background-color: #28a745; color: white; 
        border: none; border-radius: 50%; 
        width: 32px; height: 32px; font-size: 20px; cursor: pointer;
    }
    
    /* Income/Revenue Buttons */
    .btn-revenue { 
        display: block; width: 100%; padding: 14px; margin: 10px 0; 
        background: linear-gradient(135deg, #ed1c24, #aa0000); 
        color: white !important; text-align: center; border-radius: 8px; 
        font-weight: bold; text-decoration: none; border: 1px solid rgba(255,255,255,0.2);
    }
    .stat-box { font-size: 14px; color: #00ff00; font-weight: bold; margin-right: 20px; }
    </style>
    """, unsafe_allow_html=True)

# Main Title
st.title("🛡️ BT AI book")

# 3. Permanent Profile Management
if 'user' not in st.session_state:
    st.session_state.user = None
    st.session_state.pic = None

st.sidebar.header("My Profile")
if not st.session_state.user:
    name_in = st.sidebar.text_input("Username")
    file_in = st.sidebar.file_uploader("Upload Profile Image", type=['jpg', 'png', 'jpeg'])
    if st.sidebar.button("Create Account"):
        if name_in and file_in:
            file_ext = file_in.name.split('.')[-1]
            unique_name = f"profile_{uuid.uuid4()}.{file_ext}"
            supabase.storage.from_("videos").upload(path=unique_name, file=file_in.getvalue())
            st.session_state.pic = supabase.storage.from_("videos").get_public_url(unique_name)
            st.session_state.user = name_in
            st.rerun()
else:
    st.sidebar.image(st.session_state.pic, width=120)
    st.sidebar.markdown(f"### Welcome, **{st.session_state.user}**")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

tab = st.sidebar.radio("Go To", ["🌍 World Feed", "📤 Upload Video"])

# 4. Global World Feed (Real-Time Views & Likes)
if tab == "🌍 World Feed":
    st.subheader("Global Trending Videos")
    try:
        # Fetching videos with uploader details
        response = supabase.table("videos").select("*").order("created_at", desc=True).execute()
        videos = response.data
        
        if videos:
            for v in videos:
                st.markdown('<div class="video-card">', unsafe_allow_html=True)
                
                # Profile Section (Original Photo & Name)
                col1, col2 = st.columns([6, 1])
                with col1:
                    u_pic = v.get('uploader_pic') if v.get('uploader_pic') else "https://via.placeholder.com/150"
                    u_name = v.get('uploader_name', 'BT User')
                    st.markdown(f'''
                        <div class="profile-container">
                            <div class="user-box">
                                <img src="{u_pic}" class="user-avatar">
                                <span class="username-text">{u_name}</span>
                            </div>
                        </div>
                    ''', unsafe_allow_html=True)
                with col2:
                    if st.button("✚", key=f"f_{v['id']}"):
                        st.toast(f"Following {u_name}")

                # Optimized Video Player
                st.video(v['video_url'])
                
                # Dynamic Stats (Views & Likes)
                st.markdown(f'<div><span class="stat-box">👁️ {v.get("views", 0)} Views</span> <span class="stat-box">❤️ {v.get("likes", 0)} Likes</span></div>', unsafe_allow_html=True)
                
                # Action Buttons
                c_like, c_share = st.columns(2)
                with c_like:
                    if st.button("❤️ Like This", key=f"lk_{v['id']}"):
                        current_likes = v.get("likes", 0) + 1
                        supabase.table("videos").update({"likes": current_likes}).eq("id", v['id']).execute()
                        st.rerun()
                
                # Revenue Links
                st.markdown(f'<a href="https://www.profitablecpmratenetwork.com/tgt6azn6?key=e753cbd6d9bae06d67051ed846419521" class="btn-revenue">💎 Click to Earn Diamond 1</a>', unsafe_allow_html=True)
                st.markdown(f'<a href="https://www.profitablecpmratenetwork.com/krgreepsz8?key=08a0fdc6d7ed4f33a60d1f4910ec27c5" class="btn-revenue">🔥 Direct Reward Link 2</a>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)

                # Ads integration (4 scripts as requested)
                st.components.v1.html("""
                    <div style="text-align:center; padding: 10px;">
                        <script src="https://pl29264299.profitablecpmratenetwork.com/e5/58/5e/e5585e56ecc6ca2a987116ca54b2614d.js"></script>
                        <script async="async" data-cfasync="false" src="https://pl29264300.profitablecpmratenetwork.com/3d5c1921120aef030a2a6dd72337ba1d/invoke.js"></script>
                    </div>
                """, height=220)
    except:
        st.info("Syncing with Global Server... Please Wait.")

# 5. Secure Video Uploading
elif tab == "📤 Upload Video":
    if st.session_state.user:
        st.subheader("Publish to World")
        up_file = st.file_uploader("Choose MP4 Video", type=['mp4'])
        if st.button("🚀 Publish Now") and up_file:
            with st.spinner("Processing High-Speed Upload..."):
                vid_id = f"bt_vid_{uuid.uuid4()}.mp4"
                supabase.storage.from_("videos").upload(path=vid_id, file=up_file.getvalue())
                vid_url = supabase.storage.from_("videos").get_public_url(vid_id)
                
                # Secure Insert into Database
                supabase.table("videos").insert({
                    "video_url": vid_url,
                    "uploader_name": st.session_state.user,
                    "uploader_pic": st.session_state.pic,
                    "views": 1, # Auto-start with 1 view
                    "likes": 0
                }).execute()
                st.success("Successfully Published on BT AI book!")
                st.balloons()
    else:
        st.error("Access Denied: Please Setup Your Profile in the Sidebar First.")
