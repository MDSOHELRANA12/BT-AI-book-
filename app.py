import streamlit as st
from supabase import create_client
import uuid
import streamlit.components.v1 as components

# --- ১. হাই-স্পিড সার্ভার কানেকশন ---
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

# --- ২. গ্লোবাল ডিজাইন ও গুগল এডসেন্স সেটআপ ---
st.set_page_config(page_title="BT-AI World Engine", layout="wide")

st.markdown("""
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1831608481745604"
     crossorigin="anonymous"></script>
    
    <style>
    /* ১. কিতাব (GitHub) এবং পেন্সিল (Edit) আইকন দেখাবে কিন্তু ক্লিক করা যাবে না */
    header .st-emotion-cache-12fmjuu, /* GitHub container */
    header .st-emotion-cache-15z7m3b, /* Edit container */
    button[title="View source"], 
    button[title="Edit this app"],
    a[href*="github.com"] {
        pointer-events: none !important; /* ক্লিক নিষ্ক্রিয় */
        cursor: default !important;
        opacity: 0.5 !important; /* হালকা ঝাপসা দেখাবে */
    }
    
    /* ২. স্টার (Star) আইকন পুরোপুরি সচল থাকবে */
    header .st-emotion-cache-10940p5 { 
        display: inline-flex !important; 
        pointer-events: auto !important;
        opacity: 1 !important;
    }

    footer {visibility: hidden !important;} 
    
    .stApp { background-color: #000; color: #fff; }
    .video-card { 
        background: #0d0d0d; border: 2px solid #1a1a1a; 
        border-radius: 20px; padding: 20px; margin-bottom: 30px;
        box-shadow: 0 4px 20px rgba(255, 0, 0, 0.1);
    }
    .direct-btn {
        display: block; width: 100%; padding: 15px; margin: 10px 0;
        background: linear-gradient(90deg, #ff0000, #990000);
        color: white !important; text-align: center; border-radius: 12px;
        font-weight: bold; text-decoration: none; border: 1px solid #fff;
    }
    .stats-row { display: flex; justify-content: space-around; padding: 10px; background: #111; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- বাকি কোড (যা আছে তাই থাকবে) ---
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
            for i, v in enumerate(res.data):
                st.markdown('<div class="video-card">', unsafe_allow_html=True)
                st.video(v['video_url'])
                v_id = v['id']
                v_count = v.get('views', 0) + 1
                supabase.table("videos").update({"views": v_count}).eq("id", v_id).execute()
                st.markdown(f'<div class="stats-row"><span>👁️ {v_count} Views</span><span style="color:red; font-weight:bold;">❤️ {v.get('likes', 0)} Likes</span></div>', unsafe_allow_html=True)
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
