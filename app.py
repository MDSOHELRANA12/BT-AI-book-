import streamlit as st
from supabase import create_client
import uuid

# ১. গুগল এডসেন্স ও ব্যানার (আপনার আগের সিস্টেম একদম ঠিক রাখা হয়েছে)
st.markdown("""<div style="display:none;">google.com, pub-1831608481745604, DIRECT, f08c47fec0942fa0</div>
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1831608481745604" crossorigin="anonymous"></script>""", unsafe_allow_html=True)

# ২. সার্ভার কানেকশন (Supabase)
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

st.set_page_config(page_title="BT-AI World Engine", layout="wide")

# ৩. প্রফেশনাল ডিজাইন (গোল আইকন ও হাই-স্পিড প্লেয়ার)
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .video-card { background: #0d0d0d; border: 1px solid #333; border-radius: 20px; padding: 15px; margin-bottom: 25px; }
    .profile-pic { width: 45px; height: 45px; border-radius: 50%; object-fit: cover; border: 2px solid #ff0000; margin-right: 12px; }
    .user-info { display: flex; align-items: center; margin-bottom: 12px; }
    .user-name { font-weight: bold; color: #fff; font-size: 16px; }
    video { width: 100%; border-radius: 12px; }
    .stats { font-size: 14px; color: #888; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# ৪. ইউজার সেশন ম্যানেজমেন্ট
if 'user' not in st.session_state: st.session_state.user = None

st.sidebar.title("👤 My Account")
if not st.session_state.user:
    u_name = st.sidebar.text_input("Enter Name")
    u_pic = st.sidebar.text_input("Profile Image Link", "https://cdn-icons-png.flaticon.com/512/3135/3135715.png")
    if st.sidebar.button("Login"):
        st.session_state.user, st.session_state.pic = u_name, u_pic
        st.rerun()
else:
    st.sidebar.image(st.session_state.pic, width=80)
    st.sidebar.write(f"Logged in: {st.session_state.user}")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

choice = st.sidebar.radio("Navigation", ["🌍 World Feed", "📤 Upload Video"])

# ৫. ওয়ার্ল্ড ফিড (সব ভিডিও এখানে দেখা যাবে)
if choice == "🌍 World Feed":
    st.title("🌍 Global Trending")
    try:
        res = supabase.table("videos").select("*").order("created_at", desc=True).execute()
        if res.data:
            for v in res.data:
                st.markdown('<div class="video-card">', unsafe_allow_html=True)
                
                # গোল আইকন ও নাম
                u_n = v.get('uploader_name', 'Anonymous')
                u_p = v.get('uploader_pic', "https://cdn-icons-png.flaticon.com/512/3135/3135715.png")
                
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f'<div class="user-info"><img src="{u_p}" class="profile-pic"><span class="user-name">{u_n}</span></div>', unsafe_allow_html=True)
                with col2:
                    if st.button("Follow", key=f"f_{v['id']}"):
                        st.toast(f"Following {u_n}")

                # ভিডিও এবং ভিউ আপডেট
                st.video(v['video_url'])
                v_id, v_count = v['id'], v.get('views', 0) + 1
                supabase.table("videos").update({"views": v_count}).eq("id", v_id).execute()
                
                st.markdown(f'<div class="stats">👁️ {v_count} Views | ❤️ {v.get("likes", 0)} Likes</div>', unsafe_allow_html=True)
                if st.button("Like", key=f"l_{v_id}"):
                    supabase.table("videos").update({"likes": v.get('likes', 0) + 1}).eq("id", v_id).execute()
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
    except: st.info("Loading trending videos...")

# ৬. ভিডিও আপলোড (নাম ও ছবি সহ সেভ হবে)
elif choice == "📤 Upload Video":
    if st.session_state.user:
        v_file = st.file_uploader("Select Video File", type=['mp4'])
        if st.button("🚀 Publish Now") and v_file:
            with st.spinner("Publishing..."):
                f_name = f"{uuid.uuid4()}.mp4"
                supabase.storage.from_("videos").upload(path=f_name, file=v_file.getvalue())
                p_url = supabase.storage.from_("videos").get_public_url(f_name)
                
                supabase.table("videos").insert({
                    "video_url": p_url,
                    "uploader_name": st.session_state.user,
                    "uploader_pic": st.session_state.pic,
                    "views": 0, "likes": 0
                }).execute()
                st.success("Video is now Live!")
                st.balloons()
    else: st.warning("Please Login first to upload videos.")
