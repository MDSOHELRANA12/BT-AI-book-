import streamlit as st
from supabase import create_client
import uuid
import streamlit.components.v1 as components

# ১. সুপাবেস কানেকশন (আগের মতোই থাকবে)
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

st.set_page_config(page_title="BT AI book", layout="wide")

# ২. ডার্ক ইন্টারফেস ও স্টাইল (আগের কাঠামো ঠিক রেখে)
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .video-card { 
        background: #0d0d0d; border: 1px solid #333; border-radius: 15px; 
        padding: 15px; margin-bottom: 25px;
    }
    .user-avatar { width: 50px; height: 50px; border-radius: 50%; border: 2px solid #00ff00; }
    .stat-box { font-size: 14px; color: #00ff00; font-weight: bold; margin-right: 15px; }
    
    /* বড় রিওয়ার্ড ব্যানার ডিজাইন - আপনার ৩টি ভিডিও পর পর আসবে */
    .reward-box {
        padding: 20px; border: 2px solid #ff0055; border-radius: 20px; 
        text-align: center; margin: 20px 0; background: #000;
    }
    .reward-btn {
        background: linear-gradient(90deg, #ff0055, #ff0080);
        padding: 18px; display: block; border-radius: 15px; color: white !important;
        font-weight: bold; text-decoration: none; font-size: 20px;
        box-shadow: 0 0 15px #ff0055; margin-top: 10px;
    }
    
    /* প্রতিটি ভিডিওর নিচে লাল বাটন */
    .claim-btn {
        display: block; width: 100%; padding: 12px; margin: 10px 0;
        background: red; color: white !important; text-align: center;
        border-radius: 10px; font-weight: bold; text-decoration: none;
    }
    </style>
    """, unsafe_allow_html=True)

# ৩. সোশ্যাল বার (Social Bar) - এটি স্ক্রিনে অটোমেটিক ভেসে থাকবে
components.html("""
    <script src="https://pl29289908.profitablecpmratenetwork.com/75/f2/b3/75f2b3ea1ac23fb6fb2830593292cea8.js"></script>
""", height=0)

if 'user' not in st.session_state:
    st.session_state.user = None

tab = st.sidebar.radio("Navigation", ["🌍 World Feed", "📤 Upload Video"])

if tab == "🌍 World Feed":
    try:
        res = supabase.table("videos").select("*").order("created_at", desc=True).execute()
        data = res.data if res.data else []

        for index, v in enumerate(data):
            st.markdown('<div class="video-card">', unsafe_allow_html=True)
            
            # ইউজার প্রোফাইল (আগের সিস্টেম)
            st.markdown(f'''
                <div style="display:flex; align-items:center; margin-bottom:10px;">
                    <img src="{v.get('uploader_pic', '')}" class="user-avatar">
                    <span style="margin-left:10px; font-weight:bold;">{v.get('uploader_name', 'User')}</span>
                </div>
            ''', unsafe_allow_html=True)

            # ভিডিও প্লেয়ার
            st.video(v['video_url'])
            
            # প্রতিটি ভিডিওর নিচে আপনার লাল বাটন
            st.markdown(f'<a href="https://www.profitablecpmratenetwork.com/a68pzvy9g?key=ff79dfacf59be49e36f413f0f2e76766" target="_blank" class="claim-btn">💎 Claim Diamond Reward</a>', unsafe_allow_html=True)

            # লাইক ও ফলো সেকশন (আগের কাঠামো)
            st.markdown(f'<div><span class="stat-box">👁️ {v.get("views", 0)} Views</span> <span class="stat-box">❤️ {v.get("likes", 0)} Likes</span></div>', unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button(f"❤️ Like", key=f"l_{v['id']}"):
                    supabase.table("videos").update({"likes": v.get("likes", 0) + 1}).eq("id", v['id']).execute()
                    st.rerun()
            with c2:
                if st.button(f"➕ Follow", key=f"f_{v['id']}"):
                    supabase.table("videos").update({"followers": v.get("followers", 0) + 1}).eq("id", v['id']).execute()
                    st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)

            # ৪. প্রতি ৩টি ভিডিও পর পর বড় ব্যানার (আপনার নির্দেশ অনুযায়ী ৩টি করা হয়েছে)
            if (index + 1) % 3 == 0:
                st.markdown(f'''
                    <div class="reward-box">
                        <h2 style="color:#ff0055;">🎁 Special Reward Unlocked! 🎁</h2>
                        <p>Click below to claim your daily diamonds!</p>
                        <a href="https://www.profitablecpmratenetwork.com/a68pzvy9g?key=ff79dfacf59be49e36f413f0f2e76766" target="_blank" class="reward-btn">
                            🚀 CLAIM YOUR REWARD NOW 🚀
                        </a>
                    </div>
                ''', unsafe_allow_html=True)

    except Exception as e:
        st.error("Feed is updating...")

elif tab == "📤 Upload Video":
    # আপলোড সিস্টেম আগের মতোই থাকবে
    pass
