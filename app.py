import streamlit as st
from supabase import create_client
import uuid
import random

# ১. সুপাবেস কানেকশন
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

st.set_page_config(page_title="BT AI book | Hacked & Secured", layout="wide")

# ২. ডাইনামিক ভ্যালু ফরম্যাট
def format_value(value):
    if value >= 1000000: return f"{value/1000000:.1f}M"
    elif value >= 1000: return f"{value/1000:.1f}K"
    return str(value)

# ৩. প্রো ডিজাইন (সোহেল ভাই অরিজিনাল)
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .video-card { background: #0d0d0d; border: 1px solid #333; border-radius: 15px; padding: 15px; margin-bottom: 25px; }
    .stat-box { font-size: 14px; color: #00ff00; font-weight: bold; margin-right: 15px; }
    .btn-reward { display: block; width: 100%; padding: 12px; margin: 10px 0; background: linear-gradient(135deg, #ed1c24, #aa0000); color: white !important; text-align: center; border-radius: 8px; font-weight: bold; text-decoration: none; }
    </style>
    """, unsafe_allow_html=True)

# ৪. লগইন সিস্টেম
if 'user' not in st.session_state:
    st.session_state.user = None

# ৫. মেইন ফিড (ব্যান্ডউইথ সেভিং মোড)
tab = st.sidebar.radio("Navigation", ["🌍 World Feed", "📤 Upload (External)"])

if tab == "🌍 World Feed":
    res = supabase.table("videos").select("*").execute()
    data = res.data if res.data else []
    random.shuffle(data)

    for index, v in enumerate(data):
        st.markdown('<div class="video-card">', unsafe_allow_html=True)
        st.video(v['video_url'])
        
        # আপনার ইনকাম বাটন ও অ্যাড
        st.markdown(f'<a href="https://www.profitablecpmratenetwork.com/tgt6azn6?key=e753cbd6d9bae06d67051ed846419521" target="_blank" class="btn-reward">💎 Claim Diamond Reward</a>', unsafe_allow_html=True)
        
        # ২ ভিডিও পর বড় অ্যাড
        if (index + 1) % 2 == 0:
            st.markdown('<div style="border:2px dashed #ed1c24; padding:15px; text-align:center;"><p>🔥 BIG REWARD AVAILABLE 🔥</p></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ৬. হ্যাকিং স্ট্র্যাটেজি: ভিডিও এখন অন্য কোথাও হোস্ট হবে
elif tab == "📤 Upload (External)":
    st.header("🚀 Zero Cost Upload")
    st.info("সোহেল ভাই, এখানে ভিডিওর 'Direct Link' দিন। এতে সুপাবেসের ১ পয়সাও ব্যান্ডউইথ খরচ হবে না।")
    
    v_url = st.text_input("Enter Video Direct Link (Google Drive/Dropbox/YouTube)")
    u_name = st.text_input("Your Name")
    
    if st.button("Publish for Free"):
        if v_url and u_name:
            supabase.table("videos").insert({"video_url": v_url, "uploader_name": u_name, "likes": 0, "views": 0}).execute()
            st.success("✅ ওদের সিস্টেমকে ফাঁকি দেওয়া হয়েছে! ভিডিও লাইভ।")
