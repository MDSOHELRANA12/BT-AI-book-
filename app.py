import streamlit as st
from supabase import create_client
import uuid
import streamlit.components.v1 as components

# --- ১. কানেকশন ---
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

# --- ২. সিকিউরিটি এবং ডিজাইন লক ---
st.set_page_config(page_title="BT-AI World Engine", layout="wide")

st.markdown("""
    <style>
    /* ১. কিতাব, পেন্সিল এবং নিচের লোগো পুরোপুরি রিমুভ */
    [title="View source"], 
    [title="Edit this app"], 
    .viewerBadge_container__1QS1n,
    footer {
        display: none !important;
        visibility: hidden !important;
    }

    /* ২. উপরের ৩টি মেনুতে (সেটিংস, স্টার, অ্যারো) লাল লাইট ইফেক্ট */
    header [data-testid="stHeader"] svg {
        color: #ff0000 !important;
        filter: drop-shadow(0 0 5px #ff0000) !important;
    }

    /* ৩. মূল অ্যাপের ডিজাইন */
    .stApp { background-color: #000; color: #fff; }
    .video-card { 
        background: #0d0d0d; border: 2px solid #1a1a1a; 
        border-radius: 20px; padding: 20px; margin-bottom: 30px;
    }
    .direct-btn {
        display: block; width: 100%; padding: 15px; margin: 10px 0;
        background: linear-gradient(90deg, #ff0000, #990000);
        color: white !important; text-align: center; border-radius: 12px;
        font-weight: bold; text-decoration: none; border: 1px solid #fff;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ৪. আপনার জিরো পয়েন্ট প্রোফাইল সিস্টেম (নাম না দিলে কাজ করবে না) ---
if 'user' not in st.session_state: 
    st.session_state.user = None

st.sidebar.title("👤 Profile Control")
if not st.session_state.user:
    u_name = st.sidebar.text_input("Enter Your Name to Activate")
    if st.sidebar.button("Join World"):
        if u_name:
            st.session_state.user = u_name
            st.rerun()
else:
    st.sidebar.success(f"Verified Admin: {st.session_state.user}")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

# --- ৫. মেইন ফিড এবং আপলোড (প্রোফাইল ছাড়া লক থাকবে) ---
choice = st.selectbox("Switch View", ["🌍 World Feed", "📤 Upload Video", "👤 My Profile"])

if choice == "🌍 World Feed":
    st.title("🌎 Global Trending")
    try:
        res = supabase.table("videos").select("*").order("created_at", desc=True).execute()
        if res.data:
            for v in res.data:
                st.markdown('<div class="video-card">', unsafe_allow_html=True)
                st.video(v['video_url'])
                st.markdown('</div>', unsafe_allow_html=True)
    except: st.info("ভিডিও লোড হচ্ছে...")

elif choice == "📤 Upload Video":
    st.title("📤 Publish to World")
    # প্রোফাইল ভেরিফাইড থাকলেই শুধু আপলোড অপশন আসবে
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
                except Exception as e:
                    st.error(f"এরর: {e}")
    else: 
        st.error("⚠️ আগে সাইডবারে আপনার নাম দিয়ে প্রোফাইল এক্টিভেট করুন, নাহলে আপলোড হবে না।")

elif choice == "👤 My Profile":
    if st.session_state.user:
        st.markdown(f'<div style="padding:40px; border:3px solid red; border-radius:25px; text-align:center; background:#111;"><h1 style="color:red;">{st.session_state.user}</h1><p>Verified BT-AI Admin</p></div>', unsafe_allow_html=True)
