import streamlit as st
from supabase import create_client
import uuid
import streamlit.components.v1 as components

# ১. সুপাবেস কানেকশন (সোহেল ভাই, আপনার অরিজিনাল ডাটাবেস)
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

st.set_page_config(page_title="BT AI book", layout="wide")

# ২. ডার্ক ইন্টারফেস ও অরিজিনাল ডিজাইন
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .video-card { 
        background: #0d0d0d; border: 1px solid #333; border-radius: 15px; 
        padding: 15px; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    .user-avatar { 
        width: 50px; height: 50px; border-radius: 50%; 
        border: 2px solid #00ff00; object-fit: cover; margin-right: 12px; 
    }
    .username-text { font-weight: bold; font-size: 18px; color: #fff; }
    .stat-box { font-size: 14px; color: #00ff00; font-weight: bold; margin-right: 15px; }
    .claim-btn {
        display: block; width: 100%; padding: 12px; margin: 10px 0;
        background: red; color: white !important; text-align: center;
        border-radius: 10px; font-weight: bold; text-decoration: none; border: 1px solid #fff;
    }
    </style>
    """, unsafe_allow_html=True)

# ৩. সোশ্যাল বার (Social Bar) - এটি স্ক্রিনে অটোমেটিক নড়াচড়া করবে
components.html("""
    <script src="https://pl29289908.profitablecpmratenetwork.com/75/f2/b3/75f2b3ea1ac23fb6fb2830593292cea8.js"></script>
""", height=0)

# ৪. সেশন ম্যানেজমেন্ট (লগইন ও প্রোফাইল ডাটা ঠিক আছে)
if 'user' not in st.session_state:
    st.session_state.user = None
    st.session_state.pic = None

if not st.session_state.user:
    st.sidebar.header("🔐 Login")
    u_name = st.sidebar.text_input("Full Name")
    u_pic = st.sidebar.file_uploader("Upload Photo", type=['jpg', 'png', 'jpeg'])
    if st.sidebar.button("Login"):
        if u_name and u_pic:
            try:
                fname = f"profile_{uuid.uuid4()}.jpg"
                supabase.storage.from_("videos").upload(path=fname, file=u_pic.getvalue())
                st.session_state.pic = supabase.storage.from_("videos").get_public_url(fname)
                st.session_state.user = u_name
                st.rerun()
            except: st.sidebar.error("Error! Try again.")
else:
    st.sidebar.image(st.session_state.pic, width=100)
    st.sidebar.success(f"Welcome, {st.session_state.user}")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

tab = st.sidebar.radio("Navigation", ["🌍 World Feed", "📤 Upload Video"])

# ৫. ফিড সেকশন (ভিডিও ও সব ধরনের অ্যাড)
if tab == "🌍 World Feed":
    try:
        res = supabase.table("videos").select("*").order("created_at", desc=True).execute()
        data = res.data if res.data else []

        for index, v in enumerate(data):
            st.markdown('<div class="video-card">', unsafe_allow_html=True)
            
            # ইউজার প্রোফাইল ও নাম
            st.markdown(f'''
                <div style="display:flex; align-items:center; margin-bottom:12px;">
                    <img src="{v.get('uploader_pic', '')}" class="user-avatar">
                    <span class="username-text">{v.get('uploader_name', 'User')}</span>
                </div>
            ''', unsafe_allow_html=True)

            # ভিডিও প্লেয়ার
            st.video(v['video_url'])
            
            # প্রতিটি ভিডিওর নিচে আপনার লাল রিওয়ার্ড বাটন
            st.markdown(f'<a href="https://www.profitablecpmratenetwork.com/a68pzvy9g?key=ff79dfacf59be49e36f413f0f2e76766" target="_blank" class="claim-btn">💎 Claim Diamond Reward</a>', unsafe_allow_html=True)

            # --- আপনার অরিজিনাল ব্যানার অ্যাডস (সবগুলো ঠিক আছে) ---
            
            # Banner 320x50
            components.html("""
                <script>
                  atOptions = { 'key' : '342950879f2064f7255ad047622381c8', 'format' : 'iframe', 'height' : 50, 'width' : 320, 'params' : {} };
                </script>
                <script src="https://www.highperformanceformat.com/342950879f2064f7255ad047622381c8/invoke.js"></script>
            """, height=60)

            # Banner 300x250
            components.html("""
                <script>
                  atOptions = { 'key' : '5327bebb34c787d2ccfb1c36bcfa9d6e', 'format' : 'iframe', 'height' : 250, 'width' : 300, 'params' : {} };
                </script>
                <script src="https://www.highperformanceformat.com/5327bebb34c787d2ccfb1c36bcfa9d6e/invoke.js"></script>
            """, height=260)

            # স্ট্যাটাস (ভিউ ও লাইক)
            st.markdown(f'<div><span class="stat-box">👁️ {v.get("views", 0)} Views</span> <span class="stat-box">❤️ {v.get("likes", 0)} Likes</span></div>', unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button(f"❤️ Like", key=f"l_{v['id']}"):
                    supabase.table("videos").update({"likes": v.get("likes", 0) + 1}).eq("id", v['id']).execute()
                    st.rerun()
            with c2:
                if st.button(f"➕ Follow", key=f"f_{v['id']}"):
                    supabase.table("videos").update({"followers": v.get("followers", 0) + 1}).eq("id", v['id']).execute()
                    st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)

            # ৩টি ভিডিও পর পর বড় রিওয়ার্ড ব্যানার
            if (index + 1) % 3 == 0:
                components.html("""
                    <div style="text-align:center;">
                        <script async="async" data-cfasync="false" src="https://pl29264300.profitablecpmratenetwork.com/3d5c1921120aef030a2a6dd72337ba1d/invoke.js"></script>
                        <div id="container-3d5c1921120aef030a2a6dd72337ba1d"></div>
                    </div>
                """, height=260)

    except Exception as e: st.error("Feed loading...")

# ৬. ভিডিও আপলোড সেকশন (সম্পূর্ণ অরিজিনাল ও নিরাপদ)
elif tab == "📤 Upload Video":
    if st.session_state.user:
        st.subheader("Upload Your Content")
        v_file = st.file_uploader("Select MP4 Video", type=['mp4'])
        if st.button("🚀 Publish Now") and v_file:
            with st.spinner("Processing..."):
                try:
                    v_uuid = f"v_{uuid.uuid4()}.mp4"
                    supabase.storage.from_("videos").upload(path=v_uuid, file=v_file.getvalue())
                    v_url = supabase.storage.from_("videos").get_public_url(v_uuid)
                    supabase.table("videos").insert({
                        "video_url": v_url, "uploader_name": st.session_state.user,
                        "uploader_pic": st.session_state.pic, "likes": 0, "views": 0
                    }).execute()
                    st.success("Video Published!")
                    st.balloons()
                except Exception as e: st.error(f"Error: {e}")
    else: st.warning("Login first.")
