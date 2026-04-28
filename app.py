import streamlit as st
from supabase import create_client
import uuid

# ১. নতুন চাবি দিয়ে ডাটাবেজ কানেকশন (সুপার ফাস্ট করার জন্য আপডেট করা)
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
# এখানে আপনার দেওয়া পাবলিশেবল এবং সিক্রেট কি ব্যবহার করা হয়েছে
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

st.set_page_config(page_title="BT AI book", layout="wide")

# ২. ডিজাইন এবং গ্যাপ কমানোর সিএসএস
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .video-card { 
        background: #0d0d0d; border: 1px solid #333; border-radius: 15px; 
        padding: 10px; margin-bottom: 5px;
    }
    .user-avatar { 
        width: 45px; height: 45px; border-radius: 50%; 
        border: 2px solid #00ff00; object-fit: cover; margin-right: 10px; 
    }
    .username-text { font-weight: bold; font-size: 16px; color: #fff; }
    .btn-revenue { 
        display: block; width: 100%; padding: 12px; margin-top: 5px;
        background: linear-gradient(135deg, #ed1c24, #aa0000); 
        color: white !important; text-align: center; border-radius: 8px; 
        font-weight: bold; text-decoration: none;
    }
    .banner-ad-box { margin: 10px 0; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ BT AI book")

# ৩. প্রোফাইল ম্যানেজমেন্ট
if 'user' not in st.session_state:
    st.session_state.user = None
    st.session_state.pic = None

st.sidebar.header("Account")
if not st.session_state.user:
    name_in = st.sidebar.text_input("Name")
    file_in = st.sidebar.file_uploader("Photo", type=['jpg', 'png'])
    if st.sidebar.button("Create Account"):
        if name_in and file_in:
            fname = f"profile_{uuid.uuid4()}.jpg"
            supabase.storage.from_("videos").upload(path=fname, file=file_in.getvalue())
            st.session_state.pic = supabase.storage.from_("videos").get_public_url(fname)
            st.session_state.user = name_in
            st.rerun()
else:
    st.sidebar.image(st.session_state.pic, width=100)
    st.sidebar.write(f"Logged as: {st.session_state.user}")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

tab = st.sidebar.radio("Go To", ["🌍 World Feed", "📤 Upload Video"])

# ৪. ওয়ার্ল্ড ফিড (ভিডিও যাতে লোডিং ছাড়া চলে)
if tab == "🌍 World Feed":
    try:
        # ডাটাবেজ থেকে ভিডিও আনা
        response = supabase.table("videos").select("*").order("created_at", desc=True).execute()
        videos = response.data
        
        if videos:
            for v in videos:
                # অটোমেটিক ভিউ সিস্টেম
                new_count = v.get('views', 0) + 1
                supabase.table("videos").update({"views": new_count}).eq("id", v['id']).execute()
                
                st.markdown('<div class="video-card">', unsafe_allow_html=True)
                
                # প্রোফাইল হেডার
                u_pic = v.get('uploader_pic', "https://via.placeholder.com/150")
                u_name = v.get('uploader_name', 'User')
                st.markdown(f'''
                    <div style="display:flex; align-items:center; margin-bottom:10px;">
                        <img src="{u_pic}" class="user-avatar">
                        <span class="username-text">{u_name}</span>
                    </div>
                ''', unsafe_allow_html=True)

                # ফাস্ট ভিডিও প্লেয়ার (format="video/mp4" দিয়ে দ্রুত করা হয়েছে)
                st.video(v['video_url'], format="video/mp4")
                
                st.write(f"👁️ {new_count} Views | ❤️ {v.get('likes', 0)} Likes")
                
                # ইনকাম লিঙ্ক
                st.markdown(f'<a href="https://www.profitablecpmratenetwork.com/tgt6azn6?key=e753cbd6d9bae06d67051ed846419521" class="btn-revenue">💎 Click to Earn Diamond</a>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

                # ৫. ব্যানার অ্যাড (একটি লোডিং এবং ক্লিন ডিসপ্লে)
                st.markdown('<div class="banner-ad-box">', unsafe_allow_html=True)
                st.components.v1.html(f"""
                    <div style="text-align:center;">
                        <script async="async" data-cfasync="false" src="https://pl29264300.profitablecpmratenetwork.com/3d5c1921120aef030a2a6dd72337ba1d/invoke.js"></script>
                        <div id="container-3d5c1921120aef030a2a6dd72337ba1d"></div>
                    </div>
                """, height=260)
                st.markdown('</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error("Server connection is busy...")

# ৬. ভিডিও আপলোডিং
elif tab == "📤 Upload Video":
    if st.session_state.user:
        up_file = st.file_uploader("Upload MP4 Video", type=['mp4'])
        if st.button("🚀 Publish Video") and up_file:
            with st.spinner("Publishing..."):
                vid_id = f"vid_{uuid.uuid4()}.mp4"
                supabase.storage.from_("videos").upload(path=vid_id, file=up_file.getvalue())
                vid_url = supabase.storage.from_("videos").get_public_url(vid_id)
                
                supabase.table("videos").insert({
                    "video_url": vid_url,
                    "uploader_name": st.session_state.user,
                    "uploader_pic": st.session_state.pic,
                    "views": 1, 
                    "likes": 0
                }).execute()
                st.success("Successfully Published!")
    else:
        st.info("Please setup profile first.")
