import streamlit as st
from supabase import create_client
import uuid
import streamlit.components.v1 as components

# --- ১. সার্ভার কানেকশন (অপরিবর্তিত) ---
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

# --- ২. গ্লোবাল ডিজাইন ও সিকিউরিটি ---
st.set_page_config(
    page_title="BT-AI World Engine", 
    layout="wide",
    initial_sidebar_state="expanded", # সাইডবার খোলা থাকবে যেন লগইন দেখা যায়
    menu_items=None
)

st.markdown("""
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1831608481745604"
     crossorigin="anonymous"></script>
    
    <style>
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .stApp { background-color: #000; color: #fff; }
    
    /* সাদা লগইন বাটন ডিজাইন */
    .stButton>button {
        background-color: #ffffff !important;
        color: #000000 !important;
        font-weight: bold;
        border-radius: 10px;
        width: 100%;
    }

    .video-card { 
        background: #0d0d0d; border: 2px solid #1a1a1a; 
        border-radius: 20px; padding: 20px; margin-bottom: 30px;
        box-shadow: 0 4px 20px rgba(255, 0, 0, 0.1);
    }

    /* ইউজার নেম ও ফলো বাটন স্টাইল */
    .user-tag {
        color: #00ff00; font-weight: bold; font-size: 16px; margin-top: 10px;
    }
    .follow-btn {
        background: #1e1e1e; color: #fff; border: 1px solid #444;
        padding: 5px 15px; border-radius: 20px; font-size: 12px; cursor: pointer;
    }

    .direct-btn {
        display: block; width: 100%; padding: 15px; margin: 10px 0;
        background: linear-gradient(90deg, #ff0000, #990000);
        color: white !important; text-align: center; border-radius: 12px;
        font-weight: bold; text-decoration: none; border: 1px solid #fff;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ৩. অ্যাড ও লিঙ্কস ---
ad_1 = """<script type="text/javascript">atOptions = {'key' : '342950879f2064f7255ad047622381c8','format' : 'iframe','height' : 50,'width' : 320,'params' : {}};</script><script src="https://www.highperformanceformat.com/342950879f2064f7255ad047622381c8/invoke.js"></script>"""
ad_2 = """<script type="text/javascript">atOptions = {'key' : '5327bebb34c787d2ccfb1c36bcfa9d6e','format' : 'iframe','height' : 250,'width' : 300,'params' : {}};</script><script src="https://www.highperformanceformat.com/5327bebb34c787d2ccfb1c36bcfa9d6e/invoke.js"></script>"""
d_link_1 = "https://www.profitablecpmratenetwork.com/krgreepsz8?key=08a0fdc6d7ed4f33a60d1f4910ec27c5"

# --- ৪. ইউজার সেশন ও লগইন ---
if 'user' not in st.session_state: st.session_state.user = None

st.sidebar.title("👤 সদস্য লগইন")
if not st.session_state.user:
    u_name = st.sidebar.text_input("আপনার নাম লিখুন")
    if st.sidebar.button("Join World (সাদা বাটন)"):
        if u_name:
            st.session_state.user = u_name
            st.rerun()
else:
    st.sidebar.success(f"স্বাগতম, {st.session_state.user}")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

# --- ৫. মেইন ন্যাভিগেশন ---
choice = st.selectbox("মেনু নির্বাচন করুন", ["🌍 World Feed", "📤 Upload Video", "👤 My Profile"])

# --- ৬. ওয়ার্ল্ড ফিড (নাম ও ফলো বাটনসহ) ---
if choice == "🌍 World Feed":
    st.title("🌎 Global Trending")
    components.html(ad_1, height=70)
    
    try:
        res = supabase.table("videos").select("*").order("created_at", desc=True).execute()
        if res.data:
            for v in res.data:
                st.markdown('<div class="video-card">', unsafe_allow_html=True)
                
                # ইউজারের নাম দেখানো (যদি ডাটাবেজে থাকে)
                u_upload = v.get('username', 'Unknown User')
                st.markdown(f'<p class="user-tag">👤 {u_upload} <button class="follow-btn">Follow</button></p>', unsafe_allow_html=True)
                
                st.video(v['video_url'])
                st.markdown(f'<a href="{d_link_1}" target="_blank" class="direct-btn">🚀 Instant Access Offer</a>', unsafe_allow_html=True)
                
                # লাইক ও ভিউ
                v_id = v['id']
                col1, col2 = st.columns(2)
                with col1: st.write(f"👁️ {v.get('views', 0)} Views")
                with col2:
                    if st.button(f"❤️ {v.get('likes', 0)} Like", key=f"lk_{v_id}"):
                        supabase.table("videos").update({"likes": v.get('likes', 0) + 1}).eq("id", v_id).execute()
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
    except: st.info("ভিডিও লোড হচ্ছে...")

# --- ৭. ভিডিও আপলোড (নাম সেভ করাসহ) ---
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
                    
                    # ডাটাবেজে ভিডিওর সাথে নাম সেভ করা হচ্ছে
                    supabase.table("videos").insert({
                        "video_url": p_url,
                        "username": st.session_state.user,
                        "views": 0,
                        "likes": 0
                    }).execute()
                    
                    st.success("সফলভাবে আপলোড হয়েছে!")
                except Exception as e:
                    st.error(f"ভুল হয়েছে: {e}")
    else: st.warning("ভিডিও আপলোড করতে আগে প্রোফাইল সেট (Join World) করুন।")

# --- ৮. প্রোফাইল ডিজাইন ---
elif choice == "👤 My Profile":
    st.title("👤 Global Identity")
    if st.session_state.user:
        st.markdown(f"""
        <div style="padding:40px; border:3px solid red; border-radius:25px; text-align:center; background:#111;">
            <h1 style="color:red; font-size:50px;">{st.session_state.user}</h1>
            <p>আপনার প্রোফাইল এখন সারা বিশ্বে লাইভ।</p>
        </div>
        """, unsafe_allow_html=True)
