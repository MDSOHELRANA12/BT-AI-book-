import streamlit as st
from supabase import create_client
import uuid
import streamlit.components.v1 as components

# ==========================================
# ১. হাই-স্পিড সার্ভার ও কনফিগারেশন
# ==========================================
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

# পেজ সেটআপ
st.set_page_config(page_title="BT-AI World Engine", layout="wide")

# ==========================================
# ২. গ্লোবাল ডিজাইন ও গুগল এডসেন্স (CSS/JS)
# ==========================================
st.markdown("""
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1831608481745604"
     crossorigin="anonymous"></script>
    
    <style>
    /* মেইন অ্যাপ স্টাইল */
    .stApp { 
        background-color: #000; 
        color: #fff; 
    }
    
    /* ভিডিও কার্ড ডিজাইন */
    .video-card { 
        background: #0d0d0d; 
        border: 2px solid #1a1a1a; 
        border-radius: 20px; 
        padding: 20px; 
        margin-bottom: 30px;
        box-shadow: 0 4px 20px rgba(255, 0, 0, 0.1);
    }
    
    /* ডাইরেক্ট বাটন স্টাইল */
    .direct-btn {
        display: block; 
        width: 100%; 
        padding: 15px; 
        margin: 10px 0;
        background: linear-gradient(90deg, #ff0000, #990000);
        color: white !important; 
        text-align: center; 
        border-radius: 12px;
        font-weight: bold; 
        text-decoration: none; 
        border: 1px solid #fff;
    }
    
    /* স্ট্যাটাস রো ডিজাইন */
    .stats-row { 
        display: flex; 
        justify-content: space-around; 
        padding: 10px; 
        background: #111; 
        border-radius: 10px; 
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# ৩. অ্যাডস ও ডাইরেক্ট লিঙ্কস সেটিংস
# ==========================================
ad_1 = """<script type="text/javascript">atOptions = {'key' : '342950879f2064f7255ad047622381c8','format' : 'iframe','height' : 50,'width' : 320,'params' : {}};</script><script src="https://www.highperformanceformat.com/342950879f2064f7255ad047622381c8/invoke.js"></script>"""
ad_2 = """<script type="text/javascript">atOptions = {'key' : '5327bebb34c787d2ccfb1c36bcfa9d6e','format' : 'iframe','height' : 250,'width' : 300,'params' : {}};</script><script src="https://www.highperformanceformat.com/5327bebb34c787d2ccfb1c36bcfa9d6e/invoke.js"></script>"""

d_link_1 = "https://www.profitablecpmratenetwork.com/krgreepsz8?key=08a0fdc6d7ed4f33a60d1f4910ec27c5"
d_link_2 = "https://www.profitablecpmratenetwork.com/tgt6azn6?key=e753cbd6d9bae06d67051ed846419521"

# ==========================================
# ৪. ইউজার সেশন ম্যানেজমেন্ট (Sidebar)
# ==========================================
if 'user' not in st.session_state: 
    st.session_state.user = None

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

# ==========================================
# ৫. মেইন ন্যাভিগেশন
# ==========================================
choice = st.selectbox("Switch View", ["🌍 World Feed", "📤 Upload Video", "👤 My Profile"])

# ==========================================
# ৬. ওয়ার্ল্ড ফিড (ভিডিও ডিসপ্লে ও অ্যাডস)
# ==========================================
if choice == "🌍 World Feed":
    st.title("🌎 Global Trending")
    components.html(ad_1, height=70) # টপ ব্যানার অ্যাড
    
    try:
        res = supabase.table("videos").select("*").order("created_at", desc=True).execute()
        if res.data:
            for i, v in enumerate(res.data):
                st.markdown('<div class="video-card">', unsafe_allow_html=True)
                
                # ভিডিও প্লেয়ার
                st.video(v['video_url'])
                
                # ডাইরেক্ট লিঙ্ক বাটন ১
                st.markdown(f'<a href="{d_link_1}" target="_blank" class="direct-btn">🚀 Instant Access Offer</a>', unsafe_allow_html=True)
                
                # ভিউ আপডেট লজিক
                v_id = v['id']
                v_count = v.get('views', 0) + 1
                supabase.table("videos").update({"views": v_count}).eq("id", v_id).execute()
                
                # স্ট্যাটাস ডিসপ্লে
                st.markdown(f"""
                <div class="stats-row">
                    <span>👁️ {v_count} Views</span>
                    <span style="color:red; font-weight:bold;">❤️ {v.get('likes', 0)} Likes</span>
                </div>
                """, unsafe_allow_html=True)
                
                # লাইক বাটন
                if st.button(f"Like This Video", key=f"lk_{v_id}"):
                    supabase.table("videos").update({"likes": v.get('likes', 0) + 1}).eq("id", v_id).execute()
                    st.rerun()

                # ডাইরেক্ট লিঙ্ক বাটন ২
                st.markdown(f'<a href="{d_link_2}" target="_blank" class="direct-btn" style="background:#333;">💎 VIP Direct Link</a>', unsafe_allow_html=True)
                
                # প্রতি ২ ভিডিও পর পর অ্যাড দেখানো
                if i % 2 == 0:
                    components.html(ad_2, height=270)
                
                st.markdown('</div>', unsafe_allow_html=True)
    except: 
        st.info("ভিডিও লোড হচ্ছে...")

# ==========================================
# ৭. ভিডিও আপলোড সেকশন
# ==========================================
elif choice == "📤 Upload Video":
    st.title("📤 Publish to World")
    if st.session_state.user:
        uploaded_file = st.file_uploader("Select MP4 Video", type=['mp4'])
        if st.button("🚀 Publish Now") and uploaded_file:
            with st.spinner("Broadcasting..."):
                try:
                    f_bytes = uploaded_file.getvalue()
                    f_name = f"{uuid.uuid4()}.mp4"
                    
                    # স্টোরেজে আপলোড
                    supabase.storage.from_("videos").upload(path=f_name, file=f_bytes, file_options={"content-type": "video/mp4"})
                    p_url = supabase.storage.from_("videos").get_public_url(f_name)
                    
                    # ডাটাবেজে এন্ট্রি
                    supabase.table("videos").insert({
                        "video_url": p_url,
                        "views": 0,
                        "likes": 0
                    }).execute()
                    
                    st.success("সফলভাবে আপলোড হয়েছে!")
                    st.balloons()
                except Exception as e:
                    st.error(f"আপলোড আটকে গেছে: {e}")
    else: 
        st.warning("আগে প্রোফাইল সেট করে নিন।")

# ==========================================
# ৮. প্রোফাইল ডিজাইন ও অ্যাড স্ট্যাটাস
# ==========================================
elif choice == "👤 My Profile":
    st.title("👤 Global Identity")
    if st.session_state.user:
        st.markdown(f"""
        <div style="padding:40px; border:3px solid red; border-radius:25px; text-align:center; background:#111;">
            <h1 style="color:red; font-size:50px;">{st.session_state.user}</h1>
            <p style="font-size:20px;"><b>Verified BT-AI Admin</b></p>
            <p>আপনার প্রোফাইল এখন সারা বিশ্বে লাইভ।</p>
            <hr style="border-color:#333;">
            <p style="font-size:12px; color:gray;">Google Ads Status: Active</p>
            <p style="font-size:12px; color:gray;">Publisher ID: ca-pub-1831608481745604</p>
        </div>
        """, unsafe_allow_html=True)
