import streamlit as st
from supabase import create_client
import uuid

# ১. সুপাবেস কানেকশন
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

st.set_page_config(page_title="BT AI book", layout="wide")

# ২. ডার্ক ইন্টারফেস ও ডিজাইন
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
    .btn-reward { 
        display: block; width: 100%; padding: 12px; margin: 10px 0; 
        background: linear-gradient(135deg, #ed1c24, #aa0000); 
        color: white !important; text-align: center; border-radius: 8px; 
        font-weight: bold; text-decoration: none;
    }
    .big-ad-box {
        background: #1a1a1a; border: 2px dashed #00ff00; border-radius: 15px;
        padding: 20px; text-align: center; margin-bottom: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ BT AI book")

# ৩. সেশন ম্যানেজমেন্ট
if 'user' not in st.session_state:
    st.session_state.user = None
    st.session_state.pic = None

# সাইডবার লগইন
if not st.session_state.user:
    st.sidebar.header("🔐 Login")
    u_name = st.sidebar.text_input("Full Name / Username")
    u_pic = st.sidebar.file_uploader("Choose Profile Photo", type=['jpg', 'png', 'jpeg'])
    if st.sidebar.button("Enter Platform"):
        if u_name and u_pic:
            try:
                fname = f"profile_{uuid.uuid4()}.jpg"
                supabase.storage.from_("videos").upload(path=fname, file=u_pic.getvalue())
                st.session_state.pic = supabase.storage.from_("videos").get_public_url(fname)
                st.session_state.user = u_name
                st.rerun()
            except:
                st.sidebar.error("Connection Error! Please try again.")
else:
    st.sidebar.image(st.session_state.pic, width=100)
    st.sidebar.success(f"Welcome, {st.session_state.user}")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

tab = st.sidebar.radio("Navigation", ["🌍 World Feed", "📤 Upload Video"])

# ৪. মেইন ফিড (ভিডিও ও অ্যাডস)
if tab == "🌍 World Feed":
    try:
        res = supabase.table("videos").select("*").order("created_at", desc=True).execute()
        data = res.data if res.data else []

        # লুপের ইনডেক্স ট্র্যাক করার জন্য enumerate ব্যবহার করা হয়েছে
        for index, v in enumerate(data):
            st.markdown('<div class="video-card">', unsafe_allow_html=True)
            
            # ইউজার প্রোফাইল গোল ছবি ও নাম
            st.markdown(f'''
                <div style="display:flex; align-items:center; margin-bottom:15px;">
                    <img src="{v.get('uploader_pic', '')}" class="user-avatar">
                    <span class="username-text">{v.get('uploader_name', 'BT User')}</span>
                </div>
            ''', unsafe_allow_html=True)

            # ভিডিও প্লেয়ার
            st.video(v['video_url'])
            
            # --- অটোমেটিক ভিউ কাউন্ট ---
            v_id = v['id']
            v_count = v.get("views", 0)
            try:
                supabase.table("videos").update({"views": v_count + 1}).eq("id", v_id).execute()
            except: pass

            # স্ট্যাটাস ডিসপ্লে
            st.markdown(f'''
                <div style="margin: 12px 0;">
                    <span class="stat-box">👁️ {v_count + 1} Views</span>
                    <span class="stat-box">❤️ {v.get("likes", 0)} Likes</span>
                    <span class="stat-box">👤 {v.get("followers", 0)} Followers</span>
                </div>
            ''', unsafe_allow_html=True)
            
            # লাইক ও ফলো বাটন
            c1, c2 = st.columns(2)
            with c1:
                if st.button(f"❤️ Like", key=f"l_{v_id}"):
                    supabase.table("videos").update({"likes": v.get("likes", 0) + 1}).eq("id", v_id).execute()
                    st.rerun()
            with c2:
                if st.button(f"➕ Follow", key=f"f_{v_id}"):
                    supabase.table("followers_count").update({"count": v.get("followers", 0) + 1}).eq("id", v_id).execute()
                    st.rerun()

            # রিওয়ার্ড লিঙ্ক
            st.markdown(f'<a href="https://www.profitablecpmratenetwork.com/tgt6azn6?key=e753cbd6d9bae06d67051ed846419521" target="_blank" class="btn-reward">💎 Claim Diamond Reward</a>', unsafe_allow_html=True)
            
            # ব্যানার বিজ্ঞাপন (প্রতিটি ভিডিওর নিচেই থাকবে)
            st.components.v1.html("""
                <div style="text-align:center; margin-top:10px;">
                    <script type="text/javascript">
                    atOptions = { 'key' : '342950879f2064f7255ad047622381c8', 'format' : 'iframe', 'height' : 50, 'width' : 320, 'params' : {} };
                    </script>
                    <script src="https://www.highperformanceformat.com/342950879f2064f7255ad047622381c8/invoke.js"></script>
                </div>
            """, height=70)
            
            st.markdown('</div>', unsafe_allow_html=True)

            # --- নতুন শর্ত: প্রতি ২ ভিডিও পর বড় অ্যাড ---
            if (index + 1) % 2 == 0:
                st.markdown(f'''
                    <div class="big-ad-box">
                        <p style="color:#00ff00; font-weight:bold;">🔥 SPECIAL PROMOTION 🔥</p>
                        <a href="https://www.profitablecpmratenetwork.com/a68pzvy9g?key=ff79dfacf59be49e36f413f0f2e76766" target="_blank" 
                           style="background:#fff; color:#000; padding:15px 30px; border-radius:10px; text-decoration:none; font-weight:bold; display:inline-block; margin-top:10px;">
                           CLICK TO EXPLORE NEW REWARDS
                        </a>
                    </div>
                ''', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Syncing Feed... Please wait.")

# ৫. ভিডিও আপলোড সেকশন
elif tab == "📤 Upload Video":
    if st.session_state.user:
        st.subheader("Share Your Moments")
        v_file = st.file_uploader("Select MP4 Video File", type=['mp4'])
        if st.button("🚀 Publish Now") and v_file:
            with st.spinner("Processing Video..."):
                try:
                    v_uuid = f"v_{uuid.uuid4()}.mp4"
                    supabase.storage.from_("videos").upload(path=v_uuid, file=v_file.getvalue())
                    v_url = supabase.storage.from_("videos").get_public_url(v_uuid)
                    
                    supabase.table("videos").insert({
                        "video_url": v_url, 
                        "uploader_name": st.session_state.user,
                        "uploader_pic": st.session_state.pic, 
                        "likes": 0, 
                        "followers": 0, 
                        "views": 0
                    }).execute()
                    
                    st.success("Video Published Successfully!")
                    st.balloons()
                except Exception as e:
                    st.error(f"Error: {e}")
    else:
        st.warning("Please login first to upload videos.")
