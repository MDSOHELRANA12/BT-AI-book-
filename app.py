import streamlit as st
from supabase import create_client
import uuid
import streamlit.components.v1 as components

# ১. সুপাবেস কানেকশন (সোহেল ভাই, আপনার অরিজিনাল ডাটাবেস ঠিক রাখা হয়েছে)
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

st.set_page_config(page_title="BT AI book", layout="wide")

# ২. ডার্ক ইন্টারফেস ও স্টাইলিশ ডিজাইন
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .video-card { 
        background: #0d0d0d; border: 1px solid #333; border-radius: 15px; 
        padding: 15px; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    .user-avatar { 
        width: 50px; height: 50px; border-radius: 50%; 
        border: 2px solid #00ff00; object-fit: cover; margin-right: 12px; 
    }
    .username-text { font-weight: bold; font-size: 18px; color: #fff; }
    .stat-box { font-size: 14px; color: #00ff00; font-weight: bold; margin-right: 15px; }
    
    /* স্মার্টলিংক বড় ব্যানারের ডিজাইন */
    .btn-smartlink { 
        display: block; width: 100%; padding: 25px; margin: 15px 0; 
        background: linear-gradient(135deg, #ff0055, #990033); 
        color: white !important; text-align: center; border-radius: 15px; 
        font-size: 22px; font-weight: bold; text-decoration: none;
        border: 3px solid #fff; box-shadow: 0 0 20px #ff0055;
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ BT AI book")

# ৩. সেশন ম্যানেজমেন্ট (লগইন সিস্টেম ঠিক আছে)
if 'user' not in st.session_state:
    st.session_state.user = None
    st.session_state.pic = None

tab = st.sidebar.radio("Navigation", ["🌍 World Feed", "📤 Upload Video"])

# ৪. মেইন ফিড (ভিডিও ও অটোমেটিক অ্যাডস)
if tab == "🌍 World Feed":
    try:
        # ডাটাবেস থেকে সব ভিডিও আনা হচ্ছে
        res = supabase.table("videos").select("*").order("created_at", desc=True).execute()
        data = res.data if res.data else []

        for index, v in enumerate(data):
            st.markdown('<div class="video-card">', unsafe_allow_html=True)
            
            # ইউজার প্রোফাইল গোল ছবি ও নাম
            st.markdown(f'''
                <div style="display:flex; align-items:center; margin-bottom:15px;">
                    <img src="{v.get('uploader_pic', '')}" class="user-avatar">
                    <span class="username-text">{v.get('uploader_name', 'BT User')}</span>
                </div>
            ''', unsafe_allow_html=True)

            # ভিডিও প্লেয়ার
            st.video(v['video_url'])
            
            # --- প্রতিটি ভিডিওর নিচে সোশ্যাল বার (Social Bar - নড়াচড়া করবে) ---
            components.html("""
                <script src="https://pl29289908.profitablecpmratenetwork.com/75/f2/b3/75f2b3ea1ac23fb6fb2830593292cea8.js"></script>
            """, height=50)

            # স্ট্যাটাস ও বাটন লজিক (ভিউ কাউন্ট ঠিক আছে)
            v_id = v['id']
            v_count = v.get("views", 0)
            try:
                supabase.table("videos").update({"views": v_count + 1}).eq("id", v_id).execute()
            except: pass

            st.markdown(f'''
                <div style="margin: 12px 0;">
                    <span class="stat-box">👁️ {v_count + 1} Views</span>
                    <span class="stat-box">❤️ {v.get("likes", 0)} Likes</span>
                </div>
            ''', unsafe_allow_html=True)
            
            # লাইক ও ফলো বাটন
            c1, c2 = st.columns(2)
            with c1:
                if st.button(f"❤️ Like", key=f"l_{v_id}"):
                    supabase.table("videos").update({"likes": v.get("likes", 0) + 1}).eq("id", v_id).execute()
                    st.rerun()
            with c2:
                if st.button(f"➕ Follow", key=f"f_{v_id}"):
                    supabase.table("videos").update({"followers": v.get("followers", 0) + 1}).eq("id", v_id).execute()
                    st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)

            # --- ৫. ৪টি ভিডিও পর পর বড় স্মার্টলিংক ব্যানার (অটোমেটিক আসবে) ---
            if (index + 1) % 4 == 0:
                st.markdown(f'''
                    <div style="padding: 15px; background: #111; border-radius: 20px; border: 2px solid #ff0055; margin-bottom: 30px; text-align: center;">
                        <h2 style="color:#ff0055; margin-bottom:10px;">🎁 Special Reward Unlocked! 🎁</h2>
                        <p style="color:#fff;">Click the big button below to claim your daily diamonds!</p>
                        <a href="https://www.profitablecpmratenetwork.com/a68pzvy9g?key=ff79dfacf59be49e36f413f0f2e76766" target="_blank" class="btn-smartlink">
                            💎 CLAIM YOUR REWARD NOW 💎
                        </a>
                    </div>
                ''', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Syncing Feed... Please wait.")

# ৫. ভিডিও আপলোড সেকশন (আপনার অরিজিনাল কোড অপরিবর্তিত)
elif tab == "📤 Upload Video":
    if st.session_state.user:
        st.subheader("Share Your Moments")
        v_file = st.file_uploader("Select MP4 Video File", type=['mp4'])
        if st.button("🚀 Publish Now") and v_file:
            with st.spinner("Processing Video..."):
                try:
                    v_uuid = f"v_{uuid.uuid4()}.mp4"
                    supabase.storage.from_("videos").upload(path=v_uuid, file=v_file.getvalue())
                    v_url = supabase.storage.from_("videos").get_public_url(v_uuid)
                    supabase.table("videos").insert({
                        "video_url": v_url, 
                        "uploader_name": st.session_state.user,
                        "uploader_pic": st.session_state.pic, 
                        "likes": 0, "followers": 0, "views": 0
                    }).execute()
                    st.success("Video Published Successfully!")
                    st.balloons()
                except Exception as e:
                    st.error(f"Error: {e}")
    else:
        st.warning("Please login first to upload videos.")
