import streamlit as st
from supabase import create_client
import uuid
import streamlit.components.v1 as components

# ১. গুগল এডসেন্স ভেরিফিকেশন ও অটো অ্যাডস সিস্টেম
st.markdown("""
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1831608481745604" crossorigin="anonymous"></script>
    <div style="display:none;">google.com, pub-1831608481745604, DIRECT, f08c47fec0942fa0</div>
    """, unsafe_allow_html=True)

# ২. কানেকশন
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

st.set_page_config(page_title="BT-AI Revenue Engine", layout="wide")

# ৩. প্রফেশনাল স্টাইল (ব্যানার অ্যাড ও ডাইরেক্ট বাটনের ডিজাইন সহ)
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .video-card { background: #0d0d0d; border: 1px solid #333; border-radius: 20px; padding: 15px; margin-bottom: 25px; }
    .profile-pic { width: 45px; height: 45px; border-radius: 50%; object-fit: cover; border: 2px solid #ff0000; margin-right: 12px; }
    .user-info { display: flex; align-items: center; margin-bottom: 12px; }
    
    /* ডাইরেক্ট লিঙ্ক বাটনের স্টাইল */
    .direct-btn { 
        display: block; width: 100%; padding: 12px; margin: 10px 0; 
        background: linear-gradient(90deg, #ff0000, #990000); 
        color: white !important; text-align: center; border-radius: 12px; 
        font-weight: bold; text-decoration: none; border: 1px solid #fff;
    }
    
    /* ব্যানার অ্যাডের স্টাইল */
    .ad-box { background: #1a1a1a; padding: 10px; border-radius: 10px; text-align: center; margin: 15px 0; border: 1px dashed #555; }
    </style>
    """, unsafe_allow_html=True)

# ৪. ইউজার সেশন ও ছবি আপলোড সিস্টেম
if 'user' not in st.session_state: st.session_state.user = None

st.sidebar.title("👤 My Profile")
if not st.session_state.user:
    u_name = st.sidebar.text_input("Username")
    # এখানে এখন সরাসরি ছবি আপলোড করা যাবে
    u_pic_file = st.sidebar.file_uploader("Upload Profile Picture", type=['jpg', 'png', 'jpeg'])
    
    if st.sidebar.button("Login"):
        if u_name and u_pic_file:
            with st.spinner("Setting Profile..."):
                # ছবি সার্ভারে সেভ করা
                pic_name = f"profile_{uuid.uuid4()}.jpg"
                supabase.storage.from_("videos").upload(path=pic_name, file=u_pic_file.getvalue())
                pic_url = supabase.storage.from_("videos").get_public_url(pic_name)
                
                st.session_state.user = u_name
                st.session_state.pic = pic_url
                st.rerun()
        else: st.sidebar.error("Name and Photo required!")
else:
    st.sidebar.image(st.session_state.pic, width=100)
    st.sidebar.success(f"Hello, {st.session_state.user}")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

choice = st.sidebar.radio("Go to", ["🌍 World Feed", "📤 Upload Video"])

# ৫. ওয়ার্ল্ড ফিড (অ্যাড ও ডাইরেক্ট লিঙ্ক সহ)
if choice == "🌍 World Feed":
    st.title("🌎 Global Trending")
    try:
        res = supabase.table("videos").select("*").order("created_at", desc=True).execute()
        if res.data:
            for i, v in enumerate(res.data):
                st.markdown('<div class="video-card">', unsafe_allow_html=True)
                
                # ১. ইউজার ইনফো (গোল ছবি)
                u_n = v.get('uploader_name', 'User')
                u_p = v.get('uploader_pic', "https://cdn-icons-png.flaticon.com/512/3135/3135715.png")
                st.markdown(f'<div class="user-info"><img src="{u_p}" class="profile-pic"><b>{u_n}</b></div>', unsafe_allow_html=True)

                # ২. ভিডিও
                st.video(v['video_url'])
                
                # ৩. ডাইরেক্ট লিঙ্ক বাটন (আপনার আগের বাটনগুলো)
                st.markdown(f'<a href="https://www.profitablecpmrate.com/acbdqnnqig5mtmn5z7mubu" class="direct-btn">💎 Unlock Premium Content</a>', unsafe_allow_html=True)
                
                # ৪. স্ট্যাটাস ও লাইক
                v_id = v['id']
                v_count = v.get('views', 0) + 1
                supabase.table("videos").update({"views": v_count}).eq("id", v_id).execute()
                
                c1, c2 = st.columns([1, 1])
                with c1: st.write(f"👁️ {v_count} Views")
                with c2: 
                    if st.button(f"❤️ {v.get('likes', 0)} Like", key=f"lk_{v_id}"):
                        supabase.table("videos").update({"likes": v.get('likes', 0) + 1}).eq("id", v_id).execute()
                        st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)

                # ৫. ভিডিওর ফাঁকে ফাঁকে ব্যানার অ্যাড (প্রতি ২ ভিডিও পর পর)
                if i % 2 == 0:
                    st.markdown("""<div class="ad-box">
                        <p style="color:#888; font-size:10px;">ADVERTISEMENT</p>
                        <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1831608481745604" crossorigin="anonymous"></script>
                        <ins class="adsbygoogle" style="display:block" data-ad-format="fluid" data-ad-layout-key="-fb+5w+4e-db+86" data-ad-client="ca-pub-1831608481745604" data-ad-slot="YOUR_SLOT_ID"></ins>
                        <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
                    </div>""", unsafe_allow_html=True)

    except Exception as e: st.info("Loading Feed...")

# ৬. ভিডিও আপলোড
elif choice == "📤 Upload Video":
    if st.session_state.user:
        v_file = st.file_uploader("Select MP4", type=['mp4'])
        if st.button("🚀 Publish Now") and v_file:
            with st.spinner("Uploading to Server..."):
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
    else: st.warning("Login with name and photo first!")
