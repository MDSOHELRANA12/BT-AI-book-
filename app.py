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
        padding: 15px; margin-bottom: 5px; box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    .user-avatar { 
        width: 50px; height: 50px; border-radius: 50%; 
        border: 2px solid #00ff00; object-fit: cover; margin-right: 12px; 
    }
    .username-text { font-weight: bold; font-size: 18px; color: #fff; }
    .stat-box { font-size: 14px; color: #00ff00; font-weight: bold; margin-right: 20px; }
    
    /* বাটন ডিজাইন */
    .btn-revenue { 
        display: block; width: 100%; padding: 14px; margin: 8px 0; 
        background: linear-gradient(135deg, #ed1c24, #aa0000); 
        color: white !important; text-align: center; border-radius: 8px; 
        font-weight: bold; text-decoration: none; border: 1px solid rgba(255,255,255,0.2);
    }
    .btn-revenue-2 { 
        display: block; width: 100%; padding: 14px; margin: 8px 0; 
        background: linear-gradient(135deg, #0056b3, #003d80); 
        color: white !important; text-align: center; border-radius: 8px; 
        font-weight: bold; text-decoration: none; border: 1px solid rgba(255,255,255,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

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
            fname = f"profile_{uuid.uuid4()}.jpg"
            supabase.storage.from_("videos").upload(path=fname, file=file_in.getvalue())
            st.session_state.pic = supabase.storage.from_("videos").get_public_url(fname)
            st.session_state.user = name_in
            st.rerun()
else:
    st.sidebar.image(st.session_state.pic, width=120)
    st.sidebar.markdown(f"### Welcome, **{st.session_state.user}**")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

tab = st.sidebar.radio("Go To", ["🌍 World Feed", "📤 Upload Video"])

# 4. Global World Feed
if tab == "🌍 World Feed":
    try:
        response = supabase.table("videos").select("*").order("created_at", desc=True).execute()
        videos = response.data
        
        if videos:
            for v in videos:
                # অটোমেটিক ভিউ কাউন্ট
                new_view_count = v.get('views', 0) + 1
                supabase.table("videos").update({"views": new_view_count}).eq("id", v['id']).execute()
                
                st.markdown('<div class="video-card">', unsafe_allow_html=True)
                
                # Profile Header & Follow
                col_u, col_f = st.columns([4, 1])
                with col_u:
                    u_pic = v.get('uploader_pic', "https://via.placeholder.com/150")
                    u_name = v.get('uploader_name', 'BT User')
                    st.markdown(f'''
                        <div style="display:flex; align-items:center; margin-bottom:12px;">
                            <img src="{u_pic}" class="user-avatar">
                            <span class="username-text">{u_name}</span>
                        </div>
                    ''', unsafe_allow_html=True)
                
                with col_f:
                    if st.button(f"✚ Follow", key=f"fol_{v['id']}"):
                        supabase.table("videos").update({"followers": v.get('followers', 0) + 1}).eq("id", v['id']).execute()
                        st.toast(f"Following {u_name}")
                        st.rerun()

                # --- ব্যানার অ্যাড (ভিডিওর ঠিক ওপরে) ---
                st.components.v1.html(f"""
                    <div style="text-align:center; width:100%;">
                        <script async="async" data-cfasync="false" src="https://pl29264300.profitablecpmratenetwork.com/3d5c1921120aef030a2a6dd72337ba1d/invoke.js"></script>
                        <div id="container-3d5c1921120aef030a2a6dd72337ba1d"></div>
                    </div>
                """, height=260)

                # Video Player
                st.video(v['video_url'])
                
                # Stats
                st.markdown(f'<div><span class="stat-box">👁️ {new_view_count} Views</span> <span class="stat-box">❤️ {v.get("likes", 0)} Likes</span> <span class="stat-box">👤 {v.get("followers", 0)} Followers</span></div>', unsafe_allow_html=True)
                
                if st.button("❤️ Like", key=f"lk_{v['id']}"):
                    supabase.table("videos").update({"likes": v.get("likes", 0) + 1}).eq("id", v['id']).execute()
                    st.rerun()
                
                # ডাইরেক্ট লিঙ্কের দুইটা বাটন
                st.markdown(f'<a href="https://www.profitablecpmratenetwork.com/tgt6azn6?key=e753cbd6d9bae06d67051ed846419521" class="btn-revenue">💎 Click to Earn Diamond 1</a>', unsafe_allow_html=True)
                st.markdown(f'<a href="https://www.profitablecpmratenetwork.com/tgt6azn6?key=e753cbd6d9bae06d67051ed846419521" class="btn-revenue-2">💰 Click to Earn Diamond 2</a>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)

    except:
        st.info("Syncing with Global Server...")

# 5. Secure Video Uploading
elif tab == "📤 Upload Video":
    if st.session_state.user:
        up_file = st.file_uploader("Choose MP4 Video", type=['mp4'])
        if st.button("🚀 Publish Now") and up_file:
            with st.spinner("Uploading..."):
                vid_id = f"bt_vid_{uuid.uuid4()}.mp4"
                supabase.storage.from_("videos").upload(path=vid_id, file=up_file.getvalue())
                vid_url = supabase.storage.from_("videos").get_public_url(vid_id)
                
                supabase.table("videos").insert({
                    "video_url": vid_url,
                    "uploader_name": st.session_state.user,
                    "uploader_pic": st.session_state.pic,
                    "views": 1, 
                    "likes": 0,
                    "followers": 0
                }).execute()
                st.success("Successfully Published!")
