import streamlit as st
from supabase import create_client
import uuid
import streamlit.components.v1 as components

# --- ১. গুগল অ্যাডসেন্স ও ভেরিফিকেশন (সবার উপরে) ---
# এটি আপনার ads.txt ভেরিফিকেশন এবং অটো-অ্যাড কোড নিশ্চিত করবে
adsense_script = """
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1831608481745604"
     crossorigin="anonymous"></script>
    
    """

# --- ২. সার্ভার কানেকশন (অপরিবর্তিত) ---
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

# --- ৩. গ্লোবাল সেটিংস ও হেডার লোড ---
st.set_page_config(page_title="BT-AI World Engine", layout="wide")

# হেডার স্ক্রিপ্ট ইনজেকশন
components.html(adsense_script, height=0)

st.markdown("""
    <style>
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    .stApp { background-color: #000; color: #fff; }
    .video-card { 
        background: #0d0d0d; border: 2px solid #1a1a1a; 
        border-radius: 20px; padding: 15px; margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(255, 0, 0, 0.05);
    }
    .user-info {
        display: flex; align-items: center; justify-content: space-between;
        margin-bottom: 10px; padding: 8px 15px; background: #111; border-radius: 50px;
        border: 1px solid #222;
    }
    .follow-btn {
        background: #ff0000; color: #fff !important; border: none;
        padding: 5px 15px; border-radius: 20px; font-weight: bold;
        cursor: pointer; font-size: 12px; transition: 0.3s;
    }
    .follow-btn:hover { background: #cc0000; transform: scale(1.05); }
    
    .direct-btn {
        display: block; width: 100%; padding: 12px; margin: 8px 0;
        background: linear-gradient(90deg, #ff0000, #990000);
        color: white !important; text-align: center; border-radius: 10px;
        text-decoration: none; border: 1px solid #fff; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ৪. অ্যাড ও লিঙ্কস ---
ad_1 = """<script type="text/javascript">atOptions = {'key' : '342950879f2064f7255ad047622381c8','format' : 'iframe','height' : 50,'width' : 320,'params' : {}};</script><script src="https://www.highperformanceformat.com/342950879f2064f7255ad047622381c8/invoke.js"></script>"""
ad_2 = """<script type="text/javascript">atOptions = {'key' : '5327bebb34c787d2ccfb1c36bcfa9d6e','format' : 'iframe','height' : 250,'width' : 300,'params' : {}};</script><script src="https://www.highperformanceformat.com/5327bebb34c787d2ccfb1c36bcfa9d6e/invoke.js"></script>"""
d_link_1 = "https://www.profitablecpmratenetwork.com/krgreepsz8?key=08a0fdc6d7ed4f33a60d1f4910ec27c5"
d_link_2 = "https://www.profitablecpmratenetwork.com/tgt6azn6?key=e753cbd6d9bae06d67051ed846419521"

# --- ৫. ইউজার সেশন ম্যানেজমেন্ট ---
if 'user' not in st.session_state:
    st.session_state.user = None

# --- ৬. মেইন ন্যাভিগেশন ---
choice = st.selectbox("Switch View", ["🌍 World Feed", "📤 Upload Video", "👤 My Profile"])

# --- ৭. ওয়ার্ল্ড ফিড ---
if choice == "🌍 World Feed":
    st.title("🌎 Global Trending")
    components.html(ad_1, height=70)
    
    try:
        res = supabase.table("videos").select("*").order("created_at", desc=True).execute()
        if res.data:
            for i, v in enumerate(res.data):
                st.markdown('<div class="video-card">', unsafe_allow_html=True)
                
                # ইউজার ইনফো এবং ফলো বাটন
                author_name = v.get('author', 'Global User')
                st.markdown(f'''
                    <div class="user-info">
                        <span>👤 <b>{author_name}</b></span>
                        <button class="follow-btn" onclick="alert('Following {author_name}')">Follow +</button>
                    </div>
                ''', unsafe_allow_html=True)
                
                st.video(v['video_url'])
                st.markdown(f'<a href="{d_link_1}" target="_blank" class="direct-btn">🚀 Instant Access Offer</a>', unsafe_allow_html=True)
                
                v_id = v['id']
                v_count = v.get('views', 0) + 1
                supabase.table("videos").update({"views": v_count}).eq("id", v_id).execute()
                
                col1, col2 = st.columns(2)
                with col1: st.write(f"👁️ {v_count} Views")
                with col2: 
                    if st.button(f"❤️ {v.get('likes', 0)} Likes", key=f"lk_{v_id}"):
                        supabase.table("videos").update({"likes": v.get('likes', 0) + 1}).eq("id", v_id).execute()
                        st.rerun()

                st.markdown(f'<a href="{d_link_2}" target="_blank" class="direct-btn" style="background:#333;">💎 VIP Direct Link</a>', unsafe_allow_html=True)
                if i % 2 == 0: components.html(ad_2, height=270)
                st.markdown('</div>', unsafe_allow_html=True)
    except: st.info("Loading videos...")

# --- ৮. ভিডিও আপলোড ---
elif choice == "📤 Upload Video":
    st.title("📤 Publish to World")
    if st.session_state.user:
        uploaded_file = st.file_uploader("Select Video (MP4)", type=['mp4'])
        if st.button("🚀 Broadcast Now") and uploaded_file:
            with st.spinner("Broadcasting to World..."):
                try:
                    f_bytes = uploaded_file.getvalue()
                    f_name = f"{uuid.uuid4()}.mp4"
                    supabase.storage.from_("videos").upload(path=f_name, file=f_bytes, file_options={"content-type": "video/mp4"})
                    p_url = supabase.storage.from_("videos").get_public_url(f_name)
                    
                    supabase.table("videos").insert({
                        "video_url": p_url, 
                        "views": 0, 
                        "likes": 0,
                        "author": st.session_state.user
                    }).execute()
                    st.success("সফলভাবে বিশ্বজুড়ে পাবলিশ হয়েছে!")
                except Exception as e: st.error(f"Error: {e}")
    else:
        st.warning("⚠️ ভিডিও আপলোড করতে আগে 'My Profile' থেকে প্রোফাইল একটিভ করুন।")

# --- ৯. প্রোফাইল ও গ্লোবাল লগইন সিস্টেম ---
elif choice == "👤 My Profile":
    st.title("👤 Global Identity")
    
    if not st.session_state.user:
        st.markdown("""<div style="background:#111; padding:20px; border-radius:15px; border:1px solid #ff0000;">
            <h3 style="color:red;">বিশ্বজুড়ে ভিডিও শেয়ার করতে লগইন করুন</h3>
            <p>আপনার নাম এবং ৪ অক্ষরের পাসওয়ার্ড দিয়ে প্রোফাইল একটিভ করুন।</p>
        </div>""", unsafe_allow_html=True)
        
        input_name = st.text_input("আপনার নাম")
        input_pass = st.text_input("গোপন পাসওয়ার্ড", type="password")
        
        if st.button("✅ প্রোফাইল একটিভ করুন"):
            if input_name and len(input_pass) >= 4:
                st.session_state.user = input_name
                st.success(f"অভিনন্দন {input_name}! আপনার গ্লোবাল প্রোফাইল এখন একটিভ।")
                st.rerun()
            else:
                st.error("দয়া করে নাম এবং কমপক্ষে ৪ অক্ষরের পাসওয়ার্ড দিন।")
    else:
        st.markdown(f"""
        <div style="padding:40px; border:3px solid red; border-radius:25px; text-align:center; background:#111;">
            <h1 style="color:red; font-size:50px;">{st.session_state.user}</h1>
            <p style="font-size:20px;"><b>Verified BT-AI World User</b></p>
            <p>আপনার প্রোফাইল একটিভ। এখন আপনি ভিডিও আপলোড করতে পারবেন।</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Logout"):
            st.session_state.user = None
            st.rerun()
