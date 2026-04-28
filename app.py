import streamlit as st
from supabase import create_client
import uuid

# 1. Database Connection
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

st.set_page_config(page_title="BT AI book", layout="wide")

# 2. Advanced CSS for Profile and Visible Ads
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .video-card { 
        background: #0d0d0d; border: 1px solid #333; border-radius: 15px; 
        padding: 15px; margin-bottom: 30px;
    }
    .user-avatar { 
        width: 50px; height: 50px; border-radius: 50%; 
        border: 2px solid #00ff00; object-fit: cover; margin-right: 12px; 
    }
    .username-text { font-weight: bold; font-size: 18px; color: #fff; }
    .ad-container { 
        background: #111; padding: 10px; border-radius: 10px; 
        margin: 20px 0; min-height: 250px; display: block; border: 1px dashed #444;
    }
    .btn-revenue { 
        display: block; width: 100%; padding: 14px; margin: 10px 0; 
        background: linear-gradient(135deg, #ed1c24, #aa0000); 
        color: white !important; text-align: center; border-radius: 8px; 
        font-weight: bold; text-decoration: none; border: 1px solid rgba(255,255,255,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ BT AI book")

# 3. Permanent Logic (Refresh Proof)
if 'user' not in st.session_state:
    # রিফ্রেশ দিলে যেন লিঙ্ক থেকে তথ্য উদ্ধার করতে পারে
    params = st.query_params
    st.session_state.user = params.get("u", None)
    st.session_state.pic = params.get("p", None)

st.sidebar.header("My Profile")

if not st.session_state.user:
    name_in = st.sidebar.text_input("Username")
    # যদি আগে ছবি না থাকে তবেই আপলোডার দেখাবে
    file_in = st.sidebar.file_uploader("Upload Profile Image (Once)", type=['jpg', 'png', 'jpeg'])
    
    if st.sidebar.button("Login / Create Account"):
        if name_in and file_in:
            fname = f"profile_{uuid.uuid4()}.jpg"
            supabase.storage.from_("videos").upload(path=fname, file=file_in.getvalue())
            img_url = supabase.storage.from_("videos").get_public_url(fname)
            
            # সেশনে এবং ইউআরএল-এ সেভ করা হচ্ছে যাতে রিফ্রেশে না যায়
            st.session_state.user = name_in
            st.session_state.pic = img_url
            st.query_params["u"] = name_in
            st.query_params["p"] = img_url
            st.rerun()
        elif name_in and st.session_state.pic: # শুধু নাম দিলে যদি ছবি আগে থাকে
             st.session_state.user = name_in
             st.query_params["u"] = name_in
             st.rerun()
else:
    st.sidebar.image(st.session_state.pic, width=120)
    st.sidebar.markdown(f"### Active: **{st.session_state.user}**")
    if st.sidebar.button("Logout & Reset"):
        st.session_state.user = None
        st.session_state.pic = None
        st.query_params.clear()
        st.rerun()

tab = st.sidebar.radio("Go To", ["🌍 World Feed", "📤 Upload Video"])

# 4. Global World Feed
if tab == "🌍 World Feed":
    try:
        response = supabase.table("videos").select("*").order("created_at", desc=True).execute()
        if response.data:
            for v in response.data:
                st.markdown('<div class="video-card">', unsafe_allow_html=True)
                
                # User Header
                u_pic = v.get('uploader_pic', "https://via.placeholder.com/150")
                u_name = v.get('uploader_name', 'BT User')
                st.markdown(f'''
                    <div style="display:flex; align-items:center; margin-bottom:10px;">
                        <img src="{u_pic}" class="user-avatar">
                        <span class="username-text">{u_name}</span>
                        <div style="margin-left:auto;"><button style="background:#28a745; border:none; border-radius:50%; color:white; width:30px; height:30px;">+</button></div>
                    </div>
                ''', unsafe_allow_html=True)

                st.video(v['video_url'])
                
                st.write(f"👁️ {v.get('views', 0)} Views | ❤️ {v.get('likes', 0)} Likes")
                
                if st.button("❤️ Like", key=f"lk_{v['id']}"):
                    supabase.table("videos").update({"likes": v.get("likes", 0) + 1}).eq("id", v['id']).execute()
                    st.rerun()
                
                st.markdown(f'<a href="https://www.profitablecpmratenetwork.com/tgt6azn6?key=e753cbd6d9bae06d67051ed846419521" class="btn-revenue">💎 Diamond Link 1</a>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)

                # Visible Ads Section
                st.markdown('<div class="ad-container">', unsafe_allow_html=True)
                st.components.v1.html(f"""
                    <div style="text-align:center;">
                        <script src="https://pl29264299.profitablecpmratenetwork.com/e5/58/5e/e5585e56ecc6ca2a987116ca54b2614d.js"></script>
                        <script async="async" data-cfasync="false" src="https://pl29264300.profitablecpmratenetwork.com/3d5c1921120aef030a2a6dd72337ba1d/invoke.js"></script>
                        <div id="container-3d5c1921120aef030a2a6dd72337ba1d"></div>
                    </div>
                """, height=250)
                st.markdown('</div>', unsafe_allow_html=True)
    except:
        st.info("Loading BT AI book feed...")

# 5. Upload Video
elif tab == "📤 Upload Video":
    if st.session_state.user:
        up_file = st.file_uploader("Choose MP4 Video", type=['mp4'])
        if st.button("🚀 Publish Now") and up_file:
            with st.spinner("Uploading..."):
                vid_id = f"bt_{uuid.uuid4()}.mp4"
                supabase.storage.from_("videos").upload(path=vid_id, file=up_file.getvalue())
                vid_url = supabase.storage.from_("videos").get_public_url(vid_id)
                
                supabase.table("videos").insert({
                    "video_url": vid_url,
                    "uploader_name": st.session_state.user,
                    "uploader_pic": st.session_state.pic,
                    "views": 1, "likes": 0
                }).execute()
                st.success("Published Successfully!")
    else:
        st.error("Please Login in the Sidebar first.")
