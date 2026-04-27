import streamlit as st
from supabase import create_client
import uuid

# --- ১. কানেকশন ---
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

# --- ২. কনফিগারেশন ও পুরোপুরি হাইড করার CSS ---
st.set_page_config(page_title="BT-AI World Engine", layout="wide")

st.markdown("""
    <style>
    /* উপরের সব আইকন এবং মেনু পুরোপুরি মুছে ফেলার জন্য */
    header, [data-testid="stHeader"] {
        visibility: hidden !important;
        height: 0px !important;
    }
    
    /* সাইডবারের বাড়তি জিনিস থাকলে সেগুলোও বন্ধ হবে */
    [data-testid="stSidebarNav"] {display: none !important;}
    
    /* ফুটার বা নিচের লেখা লুকানোর জন্য */
    footer {visibility: hidden !important;}
    
    /* অ্যাপের মূল ডিজাইন */
    .stApp { background-color: #000; color: #fff; }
    
    .video-card { 
        background: #0d0d0d; border: 2px solid #1a1a1a; 
        border-radius: 20px; padding: 20px; margin-bottom: 30px;
    }
    
    .stats-row { display: flex; justify-content: space-around; padding: 10px; background: #111; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- বাকি ফাংশনাল কোড ---
if 'user' not in st.session_state: st.session_state.user = None

st.sidebar.title("👤 Profile Control")
if not st.session_state.user:
    u_name = st.sidebar.text_input("Enter Your Name")
    if st.sidebar.button("Join World"):
        st.session_state.user = u_name
        st.rerun()
else:
    st.sidebar.success(f"Verified: {st.session_state.user}")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

choice = st.selectbox("Switch View", ["🌍 World Feed", "📤 Upload Video", "👤 My Profile"])

if choice == "🌍 World Feed":
    st.title("🌎 Global Trending")
    try:
        res = supabase.table("videos").select("*").order("created_at", desc=True).execute()
        if res.data:
            for v in res.data:
                st.markdown('<div class="video-card">', unsafe_allow_html=True)
                st.video(v['video_url'])
                st.markdown(f'<div class="stats-row"><span>👁️ {v.get("views", 0)} Views</span><span style="color:red; font-weight:bold;">❤️ {v.get("likes", 0)} Likes</span></div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
    except: st.info("ভিডিও লোড হচ্ছে...")

elif choice == "📤 Upload Video":
    st.title("📤 Publish to World")
    if st.session_state.user:
        uploaded_file = st.file_uploader("Select MP4 Video", type=['mp4'])
        if st.button("🚀 Publish Now") and uploaded_file:
            with st.spinner("Broadcasting..."):
                try:
                    f_bytes = uploaded_file.getvalue()
                    f_name = f"{uuid.uuid4()}.mp4"
                    supabase.storage.from_("videos").upload(path=f_name, file=f_bytes, file_options={"content-type": "video/mp4"})
                    p_url = supabase.storage.from_("videos").get_public_url(f_name)
                    supabase.table("videos").insert({"video_url": p_url, "views": 0, "likes": 0}).execute()
                    st.success("সফলভাবে আপলোড হয়েছে!")
                except Exception as e: st.error(f"Error: {e}")
    else: st.warning("আগে প্রোফাইল সেট করে নিন।")

elif choice == "👤 My Profile":
    st.title("👤 Global Identity")
    if st.session_state.user:
        st.markdown(f'<div style="padding:40px; border:3px solid red; border-radius:25px; text-align:center; background:#111;"><h1 style="color:red;">{st.session_state.user}</h1></div>', unsafe_allow_html=True)
