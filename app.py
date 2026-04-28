import streamlit as st
from supabase import create_client
import uuid

# ১. ডাটাবেজ কানেকশন
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

st.set_page_config(page_title="BT AI book", layout="wide")

# ২. ডাইরেক্ট ডিসপ্লে ডিজাইন (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .video-card { 
        background: #0d0d0d; border: 1px solid #333; border-radius: 15px; 
        padding: 10px; margin-bottom: 20px;
    }
    /* বিজ্ঞাপন সরাসরি দেখানোর জন্য স্টাইল */
    .ad-overlay {
        width: 100%;
        text-align: center;
        margin-bottom: 10px;
    }
    .btn-revenue { 
        display: block; width: 100%; padding: 12px; margin: 5px 0; 
        background: linear-gradient(135deg, #ed1c24, #aa0000); 
        color: white !important; text-align: center; border-radius: 8px; 
        font-weight: bold; text-decoration: none;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ BT AI book")

# প্রোফাইল ম্যানেজমেন্ট
if 'user' not in st.session_state:
    st.session_state.user = None
    st.session_state.pic = None

if not st.session_state.user:
    st.sidebar.header("Login")
    name_in = st.sidebar.text_input("Name")
    if st.sidebar.button("Enter"):
        st.session_state.user = name_in or "User"
        st.rerun()
else:
    tab = st.sidebar.radio("Menu", ["🌍 World Feed", "📤 Upload"])

    if tab == "🌍 World Feed":
        videos = supabase.table("videos").select("*").order("created_at", desc=True).execute().data
        
        if videos:
            for v in videos:
                st.markdown('<div class="video-card">', unsafe_allow_html=True)
                
                # --- সরাসরি অ্যাড পজিশন (ভিডিওর সাথে সাথে) ---
                st.markdown('<div class="ad-overlay">', unsafe_allow_html=True)
                # আপনার অ্যাড নেটওয়ার্কের কোড এখানে সরাসরি ইনজেক্ট করা হচ্ছে
                st.components.v1.html(f"""
                    <div style="display:flex; justify-content:center; align-items:center;">
                        <script async="async" data-cfasync="false" src="//pl29264300.profitablecpmratenetwork.com/3d5c1921120aef030a2a6dd72337ba1d/invoke.js"></script>
                        <div id="container-3d5c1921120aef030a2a6dd72337ba1d"></div>
                    </div>
                """, height=260)
                st.markdown('</div>', unsafe_allow_html=True)

                # ভিডিও এবং অন্যান্য বাটন
                st.video(v['video_url'])
                
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.write(f"👁️ {v.get('views', 0)} | ❤️ {v.get('likes', 0)}")
                with col2:
                    if st.button(f"✚ Follow", key=f"fol_{v['id']}"):
                        supabase.table("videos").update({"followers": v.get('followers', 0) + 1}).eq("id", v['id']).execute()
                        st.rerun()

                st.markdown(f'<a href="https://www.profitablecpmratenetwork.com/tgt6azn6?key=e753cbd6d9bae06d67051ed846419521" class="btn-revenue">💎 Get Reward 1</a>', unsafe_allow_html=True)
                st.markdown(f'<a href="https://www.profitablecpmratenetwork.com/tgt6azn6?key=e753cbd6d9bae06d67051ed846419521" class="btn-revenue" style="background:blue;">💰 Get Reward 2</a>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)

    elif tab == "📤 Upload":
        up_file = st.file_uploader("Upload Video", type=['mp4'])
        if st.button("Publish") and up_file:
            vid_id = str(uuid.uuid4())
            supabase.storage.from_("videos").upload(vid_id, up_file.getvalue())
            url = supabase.storage.from_("videos").get_public_url(vid_id)
            supabase.table("videos").insert({"video_url": url, "uploader_name": st.session_state.user}).execute()
            st.success("Done!")
