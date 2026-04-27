import streamlit as st
from supabase import create_client
import uuid
import streamlit.components.v1 as components

# --- ১. গুগল অ্যাডসেন্স ও মেটা ভেরিফিকেশন ---
# এটি হেডারে থাকবে যেন গুগল বট সহজেই আপনার সাইট ভেরিফাই করে
adsense_code = """
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1831608481745604"
     crossorigin="anonymous"></script>
    <meta name="google-adsense-account" content="ca-pub-1831608481745604">
"""
components.html(adsense_code, height=0)

# --- ২. সার্ভার কানেকশন ---
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

# --- ৩. গ্লোবাল ডিজাইন সেটিংস ---
st.set_page_config(page_title="BT-AI Global Engine", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* মেইন ব্যাকগ্রাউন্ড */
    .stApp { background-color: #000; color: #fff; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    
    /* টপ সেটিং বার (আপনার গ্লোবাল আইকন কন্ট্রোল) */
    .global-header {
        background: linear-gradient(90deg, #1a1a1a, #000);
        padding: 15px; border-bottom: 2px solid #ff0000;
        text-align: center; border-radius: 0 0 20px 20px;
        margin-bottom: 20px;
    }
    
    /* ভিডিও কার্ড ডিজাইন */
    .video-card { 
        background: #0d0d0d; border: 1px solid #222; 
        border-radius: 20px; padding: 15px; margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(255, 0, 0, 0.1);
    }
    
    /* ইউজার ব্যাজ ও ফলো বাটন */
    .user-box {
        display: flex; align-items: center; justify-content: space-between;
        background: #1a1a1a; padding: 10px 20px; border-radius: 50px;
        border: 1px solid #333; margin-bottom: 10px;
    }
    .follow-btn {
        background: #ff0000; color: white !important; border: none;
        padding: 5px 15px; border-radius: 20px; font-weight: bold;
    }
    
    /* ডিরেক্ট লিঙ্ক বাটন */
    .action-btn {
        display: block; width: 100%; padding: 14px; margin: 10px 0;
        background: linear-gradient(45deg, #ff0000, #b30000);
        color: white !important; text-align: center; border-radius: 12px;
        font-weight: bold; text-decoration: none; border: 1px solid #fff;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ৪. সেশন ম্যানেজমেন্ট ---
if 'user' not in st.session_state: st.session_state.user = None

# --- ৫. টপ গ্লোবাল আইকন সেটিংস (এখানেই লগইন ও প্রোফাইল) ---
with st.container():
    st.markdown('<div class="global-header"><h1>🌍 BT-AI WORLD ENGINE</h1></div>', unsafe_allow_html=True)
    
    col_a, col_b, col_c = st.columns([1,2,1])
    with col_b:
        if not st.session_state.user:
            with st.expander("⚙️ Click here to Setup Global Identity (লগইন করুন)"):
                u_name = st.text_input("Enter Name", placeholder="আপনার নাম")
                u_pass = st.text_input("Enter Password", type="password", placeholder="পাসওয়ার্ড")
                if st.button("✅ Activate Now"):
                    if u_name and u_pass:
                        st.session_state.user = u_name
                        st.success(f"Welcome {u_name}! Identity Active.")
                        st.rerun()
        else:
            st.markdown(f"<p style='text-align:center; color:red;'>🟢 Active: <b>{st.session_state.user}</b></p>", unsafe_allow_html=True)
            if st.button("Logout"):
                st.session_state.user = None
                st.rerun()

# --- ৬. মেইন ন্যাভিগেশন ---
tab1, tab2 = st.tabs(["🌍 GLOBAL FEED", "📤 BROADCAST VIDEO"])

# --- ৭. গ্লোবাল ফিড (World Feed) ---
with tab1:
    # অ্যাড কোড
    ad_top = """<div style="text-align:center;"><script type="text/javascript">atOptions = {'key' : '342950879f2064f7255ad047622381c8','format' : 'iframe','height' : 50,'width' : 320,'params' : {}};</script><script src="https://www.highperformanceformat.com/342950879f2064f7255ad047622381c8/invoke.js"></script></div>"""
    components.html(ad_top, height=70)

    try:
        res = supabase.table("videos").select("*").order("created_at", desc=True).execute()
        if res.data:
            for i, v in enumerate(res.data):
                st.markdown('<div class="video-card">', unsafe_allow_html=True)
                
                # ইউজার ইনফো
                v_author = v.get('author', 'Global User')
                st.markdown(f'''
                    <div class="user-box">
                        <span>👤 <b>{v_author}</b></span>
                        <button class="follow-btn">Follow +</button>
                    </div>
                ''', unsafe_allow_html=True)
                
                st.video(v['video_url'])
                
                # অফার বাটন
                st.markdown(f'<a href="https://www.profitablecpmratenetwork.com/krgreepsz8?key=08a0fdc6d7ed4f33a60d1f4910ec27c5" target="_blank" class="action-btn">🚀 INSTANT ACCESS OFFER</a>', unsafe_allow_html=True)
                
                # লাইক ও ভিউ
                c1, c2 = st.columns(2)
                v_id = v['id']
                with c1: st.write(f"👁️ {v.get('views', 0)} Views")
                with c2:
                    if st.button(f"❤️ {v.get('likes', 0)} Likes", key=f"lk_{v_id}_{i}"):
                        supabase.table("videos").update({"likes": v.get('likes', 0) + 1}).eq("id", v_id).execute()
                        st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)
                # প্রতি ২ ভিডিও পর বড় অ্যাড
                if i % 2 == 0:
                    ad_mid = """<div style="text-align:center;"><script type="text/javascript">atOptions = {'key' : '5327bebb34c787d2ccfb1c36bcfa9d6e','format' : 'iframe','height' : 250,'width' : 300,'params' : {}};</script><script src="https://www.highperformanceformat.com/5327bebb34c787d2ccfb1c36bcfa9d6e/invoke.js"></script></div>"""
                    components.html(ad_mid, height=270)
    except: st.warning("Loading World Feed...")

# --- ৮. ব্রডকাস্ট/আপলোড (Broadcast Now) ---
with tab2:
    if st.session_state.user:
        st.subheader("📤 Broadcast Your Content to the World")
        up_file = st.file_uploader("Choose MP4 Video", type=['mp4'])
        if st.button("🚀 GO LIVE / BROADCAST") and up_file:
            with st.spinner("Processing Global Broadcast..."):
                try:
                    f_name = f"{uuid.uuid4()}.mp4"
                    f_bytes = up_file.getvalue()
                    supabase.storage.from_("videos").upload(path=f_name, file=f_bytes, file_options={"content-type": "video/mp4"})
                    p_url = supabase.storage.from_("videos").get_public_url(f_name)
                    
                    supabase.table("videos").insert({
                        "video_url": p_url, "views": 0, "likes": 0, "author": st.session_state.user
                    }).execute()
                    st.success("Broadcast Success! Your video is now Live.")
                except Exception as e: st.error(f"Error: {e}")
    else:
        st.error("⚠️ Please Setup Your Identity First (উপরের সেটিংস থেকে নাম দিন)")
