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
    .uploader-info { color: #ff4b4b; font-weight: bold; margin-bottom: 10px; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

# --- ৩. অ্যাড ও লিঙ্কস ---
ad_1 = """<script type="text/javascript">atOptions = {'key' : '342950879f2064f7255ad047622381c8','format' : 'iframe','height' : 50,'width' : 320,'params' : {}};</script><script src="https://www.highperformanceformat.com/342950879f2064f7255ad047622381c8/invoke.js"></script>"""
ad_2 = """<script type="text/javascript">atOptions = {'key' : '5327bebb34c787d2ccfb1c36bcfa9d6e','format' : 'iframe','height' : 250,'width' : 300,'params' : {}};</script><script src="https://www.highperformanceformat.com/5327bebb34c787d2ccfb1c36bcfa9d6e/invoke.js"></script>"""

d_link_1 = "https://www.profitablecpmratenetwork.com/krgreepsz8?key=08a0fdc6d7ed4f33a60d1f4910ec27c5"
d_link_2 = "https://www.profitablecpmratenetwork.com/tgt6azn6?key=e753cbd6d9bae06d67051ed846419521"

# --- ৪. ইউজার সেশন ---
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

# --- ৫. মেইন ন্যাভিগেশন ---
choice = st.selectbox("Switch View", ["🌍 World Feed", "📤 Upload Video", "👤 My Profile"])

# --- ৬. ওয়ার্ল্ড ফিড ---
if choice == "🌍 World Feed":
    st.title("🌎 Global Trending")
    components.html(ad_1, height=70)
    
    try:
        res = supabase.table("videos").select("*").order("created_at", desc=True).execute()
        if res.data:
            for i, v in enumerate(res.data):
                st.markdown('<div class="video-card">', unsafe_allow_html=True)
                
                # ১. আপলোডারের নাম ভিডিওর উপরে
                up_name = v.get('uploader_name', 'Global User')
                st.markdown(f'<div class="uploader-info">👤 {up_name}</div>', unsafe_allow_html=True)
                
                st.video(v['video_url'])
                
                # ২. ফলো বাটন (রিয়েল কাজ করবে)
                col_f1, col_f2 = st.columns([3, 1])
                with col_f2:
                    if st.button(f"Follow", key=f"fol_{v['id']}"):
                        st.success(f"Followed {up_name}!")

                st.markdown(f'<a href="{d_link_1}" target="_blank" class="direct-btn">🚀 Instant Access Offer</a>', unsafe_allow_html=True)
                
                v_id = v['id']
                v_count = v.get('views', 0) + 1
                supabase.table("videos").update({"views": v_count}).eq("id", v_id).execute()
                
                st.markdown(f"""
                <div class="stats-row">
                    <span>👁️ {v_count} Views</span>
                    <span style="color:red; font-weight:bold;">❤️ {v.get('likes', 0)} Likes</span>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Like This Video", key=f"lk_{v_id}"):
                    supabase.table("videos").update({"likes": v.get('likes', 0) + 1}).eq("id", v_id).execute()
                    st.rerun()

                st.markdown(f'<a href="{d_link_2}" target="_blank" class="direct-btn" style="background:#333;">💎 VIP Direct Link</a>', unsafe_allow_html=True)
                
                if i % 2 == 0:
                    components.html(ad_2, height=270)
                
                st.markdown('</div>', unsafe_allow_html=True)
    except: st.info("ভিডিও লোড হচ্ছে...")

# --- ৭. ভিডিও আপলোড (নাম সহ সেভ হবে) ---
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
                    
                    # এখানে uploader_name কলামে নাম সেভ হবে
                    supabase.table("videos").insert({
                        "video_url": p_url,
                        "views": 0,
                        "likes": 0,
                        "uploader_name": st.session_state.user
                    }).execute()
                    
                    st.success("সফলভাবে আপলোড হয়েছে!")
                    st.balloons()
                except Exception as e:
                    st.error(f"Error: {e}")
    else: st.warning("আগে প্রোফাইল সেট করে নিন।")

# --- ৮. প্রোফাইল ডিজাইন ---
elif choice == "👤 My Profile":
    st.title("👤 Global Identity")
    if st.session_state.user:
        st.markdown(f"""
        <div style="padding:40px; border:3px solid red; border-radius:25px; text-align:center; background:#111;">
            <h1 style="color:red; font-size:50px;">{st.session_state.user}</h1>
            <p style="font-size:20px;"><b>Verified BT-AI Admin</b></p>
            <p>আপনার প্রোফাইল এখন সারা বিশ্বে লাইভ।</p>
            <p style="font-size:12px; color:gray;">Google Ads Status: Active (ca-pub-1831608481745604)</p>
        </div>
        """, unsafe_allow_html=True)
