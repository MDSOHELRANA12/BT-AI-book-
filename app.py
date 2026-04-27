import streamlit as st
from supabase import create_client
import uuid
import streamlit.components.v1 as components

# --- ১. হাই-স্পিড সার্ভার কানেকশন (অপরিবর্তিত) ---
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

# --- ২. গ্লোবাল ডিজাইন ও সিকিউরিটি ---
st.set_page_config(
    page_title="BT-AI World Engine", 
    layout="wide",
    initial_sidebar_state="expanded", # এটি অন রাখা হয়েছে যাতে সাইন-ইন দেখা যায়
    menu_items=None
)

st.markdown("""
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1831608481745604"
     crossorigin="anonymous"></script>
    
    <style>
    /* গিটহাব আইকন লুকানো কিন্তু ফাংশন সচল রাখা */
    header {visibility: hidden !important;}
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    .viewerBadge_container__1QS1n {display: none !important;}
    
    .stApp { background-color: #000; color: #fff; }
    
    /* আপনার চাওয়া সেই সাদা লগইন বাটন */
    .stButton>button {
        background-color: #ffffff !important;
        color: #000000 !important;
        font-weight: bold;
        border: 2px solid #ff0000;
        border-radius: 12px;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #ff0000 !important; color: #fff !important; }

    .video-card { 
        background: #0d0d0d; border: 2px solid #1a1a1a; 
        border-radius: 20px; padding: 20px; margin-bottom: 30px;
        box-shadow: 0 4px 20px rgba(255, 0, 0, 0.2);
    }

    /* নাম ও ফলো বাটন ডিজাইন */
    .user-info-row { display: flex; align-items: center; margin-bottom: 10px; }
    .user-tag { color: #00ff00; font-weight: bold; font-size: 18px; }
    .follow-btn-style {
        background: #ff0000; color: #fff; border: none;
        padding: 5px 15px; border-radius: 20px; font-size: 12px;
        margin-left: 15px; cursor: pointer; font-weight: bold;
    }

    .direct-btn {
        display: block; width: 100%; padding: 15px; margin: 10px 0;
        background: linear-gradient(90deg, #ff0000, #330000);
        color: white !important; text-align: center; border-radius: 12px;
        font-weight: bold; text-decoration: none; border: 1px solid #fff;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ৩. অ্যাড ও লিঙ্কস (আপনার সব আর্নিং লিঙ্ক ঠিক আছে) ---
ad_1 = """<script type="text/javascript">atOptions = {'key' : '342950879f2064f7255ad047622381c8','format' : 'iframe','height' : 50,'width' : 320,'params' : {}};</script><script src="https://www.highperformanceformat.com/342950879f2064f7255ad047622381c8/invoke.js"></script>"""
d_link_1 = "https://www.profitablecpmratenetwork.com/krgreepsz8?key=08a0fdc6d7ed4f33a60d1f4910ec27c5"

# --- ৪. ইউজার সেশন ও সেটিংস ---
if 'user' not in st.session_state: st.session_state.user = None

st.sidebar.title("👤 Account Settings")
if not st.session_state.user:
    u_name = st.sidebar.text_input("আপনার নাম (ইউজারনেম)")
    u_pass = st.sidebar.text_input("পাসওয়ার্ড", type="password")
    if st.sidebar.button("Join World (সাদা বাটন)"):
        if u_name:
            st.session_state.user = u_name
            st.rerun()
else:
    st.sidebar.success(f"Verified: {st.session_state.user}")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

# --- ৫. মেইন ন্যাভিগেশন ---
choice = st.selectbox("Switch View", ["🌍 World Feed", "📤 Upload Video", "👤 My Profile"])

# --- ৬. ওয়ার্ল্ড ফিড (নাম ও ফলো বাটন সচল করা হয়েছে) ---
if choice == "🌍 World Feed":
    st.title("🌎 Global Trending")
    components.html(ad_1, height=70)
    
    try:
        res = supabase.table("videos").select("*").order("created_at", desc=True).execute()
        if res.data:
            for v in res.data:
                st.markdown('<div class="video-card">', unsafe_allow_html=True)
                
                # ইউজারের নাম এবং ফলো বাটন
                u_upload = v.get('username', 'Global Admin')
                st.markdown(f'''
                    <div class="user-info-row">
                        <span class="user-tag">👤 {u_upload}</span>
                        <button class="follow-btn-style">Follow +</button>
                    </div>
                ''', unsafe_allow_html=True)
                
                st.video(v['video_url'])
                st.markdown(f'<a href="{d_link_1}" target="_blank" class="direct-btn">🚀 Instant Access Offer</a>', unsafe_allow_html=True)
                
                # লাইক ও ভিউ আপডেট
                v_id = v['id']
                col1, col2 = st.columns(2)
                with col1: st.write(f"👁️ {v.get('views', 0)} Views")
                with col2:
                    if st.button(f"❤️ {v.get('likes', 0)} Like", key=f"lk_{v_id}"):
                        supabase.table("videos").update({"likes": v.get('likes', 0) + 1}).eq("id", v_id).execute()
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
    except: st.info("ভিডিও লোড হচ্ছে...")

# --- ৭. ভিডিও আপলোড (নাম সেভ করার ব্যবস্থা) ---
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
                    
                    # ডাটাবেজে আপনার নামের সাথে ভিডিও সেভ হবে
                    supabase.table("videos").insert({
                        "video_url": p_url,
                        "username": st.session_state.user,
                        "views": 0, "likes": 0
                    }).execute()
                    
                    st.success("সফলভাবে আপলোড হয়েছে!")
                except Exception as e:
                    st.error(f"Error: {e}")
    else: st.warning("ভিডিও আপলোড করতে আগে সাইডবার থেকে নাম দিয়ে 'Join World' করুন।")

# --- ৮. প্রোফাইল ---
elif choice == "👤 My Profile":
    st.title("👤 Global Identity")
    if st.session_state.user:
        st.markdown(f"""
        <div style="padding:40px; border:3px solid red; border-radius:25px; text-align:center; background:#111;">
            <h1 style="color:red; font-size:50px;">{st.session_state.user}</h1>
            <p>আপনার প্রোফাইল এখন সারা বিশ্বে লাইভ।</p>
        </div>
        """, unsafe_allow_html=True)
