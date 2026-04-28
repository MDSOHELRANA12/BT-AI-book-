import streamlit as st
from supabase import create_client
import uuid

# 1. Database Connection
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

st.set_page_config(page_title="BT AI book (Global Edition)", layout="wide")

# 2. অরিজিনাল স্টাইল (কালো গ্যাপ ছাড়া)
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .video-container { 
        background: #000; border-radius: 0px; 
        padding: 0px; margin-bottom: 20px; 
    }
    .user-info { display: flex; align-items: center; padding: 10px; }
    .user-avatar { width: 40px; height: 40px; border-radius: 50%; border: 2px solid #00ff00; margin-right: 10px; }
    .stat-text { color: #00ff00; font-weight: bold; font-size: 14px; margin-left: 10px; }
    .btn-earn { 
        display: block; width: 100%; padding: 15px; background: red; 
        color: white; text-align: center; border-radius: 10px; font-weight: bold; text-decoration: none;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. অরিজিনাল ভিউ এবং ফিড অ্যালগরিদম
if 'user' not in st.session_state:
    st.session_state.user = None

tab = st.sidebar.radio("Menu", ["🌍 World Feed", "📤 Upload", "💰 Monetization"])

if tab == "🌍 World Feed":
    try:
        # ডাটাবেজ থেকে ভিডিও আনা
        response = supabase.table("videos").select("*").order("created_at", desc=True).execute()
        videos = response.data
        
        for v in videos:
            # অরিজিনাল ভিউ আপডেট লজিক
            new_views = v.get('views', 0) + 1
            supabase.table("videos").update({"views": new_views}).eq("id", v['id']).execute()

            st.markdown('<div class="video-container">', unsafe_allow_html=True)
            
            # ইউজার প্রোফাইল (Atip / MDSOHELRANA)
            st.markdown(f'''
                <div class="user-info">
                    <img src="{v.get('uploader_pic', 'https://via.placeholder.com/50')}" class="user-avatar">
                    <span style="font-weight:bold;">{v.get('uploader_name', 'User')}</span>
                </div>
            ''', unsafe_allow_html=True)

            # ভিডিওর উপরের অ্যাড
            st.components.v1.html(f"""
                <script type="text/javascript">
                atOptions = {{ 'key' : '5327bebb34c787d2ccfb1c36bcfa9d6e', 'format' : 'iframe', 'height' : 250, 'width' : 300, 'params' : {{}} }};
                </script>
                <script src="https://www.highperformanceformat.com/5327bebb34c787d2ccfb1c36bcfa9d6e/invoke.js"></script>
            """, height=260)

            # ভিডিও প্লেয়ার
            st.video(v['video_url'])

            # অরিজিনাল ভিউ এবং লাইক সংখ্যা দেখানো
            st.markdown(f'<div><span class="stat-text">👁️ {new_views} Views</span><span class="stat-text">❤️ {v.get("likes", 0)} Likes</span><span class="stat-text">👤 {v.get("followers", 0)} Followers</span></div>', unsafe_allow_html=True)

            # ইন্টারঅ্যাকশন বাটন
            c1, c2 = st.columns(2)
            with c1:
                if st.button(f"❤️ Like", key=f"lk_{v['id']}"):
                    supabase.table("videos").update({"likes": v.get("likes", 0) + 1}).eq("id", v['id']).execute()
                    st.rerun()
            with c2:
                if st.button(f"➕ Follow", key=f"fl_{v['id']}"):
                    supabase.table("videos").update({"followers": v.get("followers", 0) + 1}).eq("id", v['id']).execute()
                    st.rerun()

            # ডায়মন্ড রিওয়ার্ড অ্যাড বাটন
            st.markdown(f'<a href="https://www.profitablecpmratenetwork.com/tgt6azn6?key=e753cbd6d9bae06d67051ed846419521" target="_blank" class="btn-earn">💎 Get Diamond Reward</a>', unsafe_allow_html=True)

            # ভিডিওর নিচের ব্যানার অ্যাড
            st.components.v1.html("""
                <script async="async" data-cfasync="false" src="https://pl29264300.profitablecpmratenetwork.com/3d5c1921120aef030a2a6dd72337ba1d/invoke.js"></script>
                <div id="container-3d5c1921120aef030a2a6dd72337ba1d"></div>
            """, height=250)
            
            st.markdown('<hr style="border:1px solid #333;">', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    except:
        st.info("অ্যালগরিদম লোড হচ্ছে...")

elif tab == "📤 Upload":
    # আপনার আগের আপলোড কোড এখানে থাকবে...
    st.write("ভিডিও আপলোড করুন")

elif tab == "💰 Monetization":
    st.header("Global Monetization Program")
    st.info("আপনার ১০০০ ফলোয়ার হলে পেমেন্ট রিকোয়েস্ট করতে পারবেন।")
