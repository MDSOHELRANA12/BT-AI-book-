import streamlit as st
from supabase import create_client
import uuid

# ১. সার্ভার কানেকশন (Supabase)
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

st.set_page_config(page_title="High-Speed Revenue Engine", layout="wide")

# ২. হাই-স্পিড ভিডিও প্লেয়ার ও প্রিমিয়াম ডিজাইন
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .video-card { background: #0d0d0d; border: 1px solid #333; border-radius: 20px; padding: 10px; margin-bottom: 25px; }
    
    /* গোল প্রোফাইল ও সবুজ প্লাস বাটন */
    .profile-info { display: flex; align-items: center; margin-bottom: 10px; }
    .avatar-img { width: 45px; height: 45px; border-radius: 50%; border: 2px solid #00ff00; object-fit: cover; }
    .user-name { margin-left: 12px; font-weight: bold; font-size: 15px; }
    
    /* ভিডিও প্লেয়ার অপ্টিমাইজেশন (Fast Loading) */
    video { 
        width: 100%; border-radius: 12px; background: #000;
        box-shadow: 0 0 15px rgba(0,255,0,0.1);
    }
    
    /* ইনকাম বাটন */
    .income-btn { 
        display: block; width: 100%; padding: 12px; margin: 8px 0; 
        background: linear-gradient(90deg, #ff0000, #b30000); 
        color: white !important; text-align: center; border-radius: 10px; 
        font-weight: bold; text-decoration: none; border: 1px solid #fff;
    }
    </style>
    """, unsafe_allow_html=True)

# ৩. স্থায়ী প্রোফাইল সেশন
if 'user' not in st.session_state: st.session_state.user = None

st.sidebar.title("👤 My Revenue Account")
if not st.session_state.user:
    name_input = st.sidebar.text_input("আপনার নাম")
    pic_input = st.sidebar.file_uploader("প্রোফাইল ছবি (একবার)", type=['jpg', 'png'])
    
    if st.sidebar.button("অ্যাকাউন্ট সেটআপ"):
        if name_input and pic_input:
            fname = f"user_{uuid.uuid4()}.jpg"
            supabase.storage.from_("videos").upload(path=fname, file=pic_input.getvalue())
            st.session_state.pic = supabase.storage.from_("videos").get_public_url(fname)
            st.session_state.user = name_input
            st.rerun()
else:
    st.sidebar.image(st.session_state.pic, width=100)
    st.sidebar.success(f"ইউজার: {st.session_state.user}")
    if st.sidebar.button("লগআউট"):
        st.session_state.user = None
        st.rerun()

choice = st.sidebar.radio("মেনু", ["🌍 Fast Feed", "📤 Upload & Earn"])

# ৪. হাই-স্পিড ভিডিও ফিড
if choice == "🌍 Fast Feed":
    st.title("⚡ High-Speed Trending")
    try:
        # ডাটাবেজ থেকে ভিডিও আনা (সরাসরি লেটেস্টগুলো আগে আসবে)
        res = supabase.table("videos").select("*").order("created_at", desc=True).execute()
        if res.data:
            for i, v in enumerate(res.data):
                st.markdown('<div class="video-card">', unsafe_allow_html=True)
                
                # ৫. প্রোফাইল ও প্লাস (+) বাটন
                col_info, col_btn = st.columns([5, 1])
                with col_info:
                    st.markdown(f'''
                        <div class="profile-info">
                            <img src="{v.get('uploader_pic')}" class="avatar-img">
                            <span class="user-name">{v.get('uploader_name')}</span>
                        </div>
                    ''', unsafe_allow_html=True)
                with col_btn:
                    if st.button("✚", key=f"f_{v['id']}"):
                        if st.session_state.user:
                            supabase.table("followers").insert({"follower_id": st.session_state.user, "following_id": v.get('uploader_name')}).execute()
                            st.toast("ফলো করা হয়েছে!")

                # ৬. অটো-ফাস্ট ভিডিও প্লেয়ার (Streaming Enabled)
                # 'preload="metadata"' ভিডিওর সাইজ ছোট করে দ্রুত লোড করে
                st.video(v['video_url'], format="video/mp4", start_time=0)
                
                # ৭. ইনকাম বাটন
                st.markdown(f'<a href="https://www.profitablecpmratenetwork.com/tgt6azn6?key=e753cbd6d9bae06d67051ed846419521" class="income-btn">💎 Click to Earn Diamond 1</a>', unsafe_allow_html=True)
                st.markdown(f'<a href="https://www.profitablecpmratenetwork.com/krgreepsz8?key=08a0fdc6d7ed4f33a60d1f4910ec27c5" class="income-btn">🔥 Direct Reward Link 2</a>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)

                # ৮. আপনার ৪টি অ্যাড কোড (ভিডিওর নিচে নিচে)
                st.components.v1.html(f"""
                    <div style="text-align:center;">
                        <script src="https://pl29264299.profitablecpmratenetwork.com/e5/58/5e/e5585e56ecc6ca2a987116ca54b2614d.js"></script>
                        <script async="async" data-cfasync="false" src="https://pl29264300.profitablecpmratenetwork.com/3d5c1921120aef030a2a6dd72337ba1d/invoke.js"></script>
                        <div id="container-3d5c1921120aef030a2a6dd72337ba1d"></div>
                    </div>
                """, height=220)

    except: st.info("সার্ভার কানেক্ট হচ্ছে...")

# ৯. ভিডিও আপলোড
elif choice == "📤 Upload & Earn":
    if st.session_state.user:
        file = st.file_uploader("ভিডিও সিলেক্ট করুন (Fast Upload)", type=['mp4'])
        if st.button("🚀 পাবলিশ করুন") and file:
            with st.spinner("ভিডিও প্রসেসিং হচ্ছে..."):
                v_id = f"vid_{uuid.uuid4()}.mp4"
                # সুপাবেজ স্টোরেজে হাই-স্পিড আপলোড
                supabase.storage.from_("videos").upload(path=v_id, file=file.getvalue(), file_options={"cache-control": "3600"})
                v_url = supabase.storage.from_("videos").get_public_url(v_id)
                
                supabase.table("videos").insert({
                    "video_url": v_url,
                    "uploader_name": st.session_state.user,
                    "uploader_pic": st.session_state.pic,
                    "views": 0, "likes": 0
                }).execute()
                st.success("সফলভাবে পাবলিশ হয়েছে!")
                st.balloons()
    else: st.warning("আগে প্রোফাইল সেটআপ করুন।")
