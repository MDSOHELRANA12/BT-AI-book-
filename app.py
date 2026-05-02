import streamlit as st
from supabase import create_client
import uuid
import random
import os
import subprocess
from datetime import datetime

# --- [জংশন বক্স] ---
MAIN_URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
MAIN_KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(MAIN_URL, MAIN_KEY)

STORAGE_KEYS = [
    {"url": "https://wzwhcuifcdkhjkvhndcp.supabase.co", "key": "sb_secret_bt9SDKvRqm9J91cZD-MAkw_caf0Gnkh"},
    {"url": "https://fypvwatkffekksbceofu.supabase.co", "key": "sb_secret_JeRIhaN33UZe9nTKgfMzwQ_Kc5rHL8o"},
    {"url": "https://osdjwtywivieuetnhxyo.supabase.co", "key": "sb_secret_ffiZGQ8XSUdAWXa26Ut2ww_-dVCfJy4"},
    {"url": "https://fiqjddgdpirdpbaccynt.supabase.co", "key": "sb_secret_kKfsUaR3Eyxp-W-ZLQYftg_9THDBB3C"},
    {"url": "https://ebkpbdjfeabqfwbkgvrg.supabase.co", "key": "sb_secret_HuxmaOONEyvFBqDB2yH_IQ_OcC6Pm4b"},
    {"url": "https://xjquucfkndfzawjscmdb.supabase.co", "key": "sb_secret_dRBwgkxRhwLwwYLSU92VBw_NUKkyX32"},
    {"url": "https://ziliihcgqsxnttrtupgm.supabase.co", "key": "sb_secret_GyhZd_60lAW6np0uBNjuBA_amZpgwUl"},
    {"url": "https://optlxxgrdmrvvkzwkmui.supabase.co", "key": "sb_secret_aKImpLhPtUkF3ggXgDKGRw_BJC7Qd_M"},
    {"url": "https://owlhzlgegmezedskzwgl.supabase.co", "key": "sb_secret_wOMZKz1TtugQNXFYgV4d4g_K82EnAl1"},
    {"url": "https://bczxwfclimiaaljjfegq.supabase.co", "key": "sb_secret_7rFR003t7a_N_VIEbf7aAw_WfPL7xRs"},
]

st.set_page_config(page_title="BT AI book", layout="centered")

# --- CSS ডিজাইন ---
st.markdown("""
<style>
    .stApp { background-color: #000; color: #fff; }
    .video-card { background: #111; border-radius: 15px; padding: 10px; margin-bottom: 20px; border: 1px solid #333; text-align: center; }
    .ad-slot { background: #1a1a1a; padding: 10px; border-radius: 10px; margin: 15px 0; border: 1px dashed #444; }
    .stat-row { display: flex; justify-content: space-around; padding: 10px; background: #222; border-radius: 10px; margin-top: 5px; }
</style>
""", unsafe_allow_html=True)

if 'user' not in st.session_state: st.session_state.user = None

# --- অটো ক্লিনিং ফাংশন ---
def auto_cleanup():
    res = supabase.table("videos").select("id", "video_url").order("created_at", desc=False).execute()
    if len(res.data) >= 100:
        old = res.data[0]
        v_url = old['video_url']
        v_name = v_url.split('/')[-1]
        for s in STORAGE_KEYS:
            if s['url'] in v_url:
                try: create_client(s['url'], s['key']).storage.from_("videos").remove([v_name])
                except: pass
        supabase.table("videos").delete().eq("id", old['id']).execute()

tab = st.sidebar.radio("BT Menu", ["🌍 World Feed", "📤 Upload Video", "🔐 Profile"])

# --- ১. ওয়ার্ল্ড ফিড ---
if tab == "🌍 World Feed":
    st.title("🛡️ BT AI book")
    
    # অ্যাড কোড (এখানে আপনার Google Ad বা অন্য Ad কোড বসাবেন)
    st.markdown('<div class="ad-slot"><b>[ Sponsored Ad ]</b><br>এখানে অ্যাড শো হবে</div>', unsafe_allow_html=True)
    
    res = supabase.table("videos").select("*").order("created_at", desc=True).execute()
    
    for v in res.data:
        with st.container():
            st.markdown(f'<div class="video-card"><b>👤 {v["uploader_name"]}</b></div>', unsafe_allow_html=True)
            st.video(v['video_url'])
            
            # স্ট্যাটাস এবং বাটন
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button(f"❤️ {v.get('likes', 0)}", key=f"lk_{v['id']}"):
                    supabase.table("videos").update({"likes": v.get('likes', 0) + 1}).eq("id", v['id']).execute()
                    st.rerun()
            with col2:
                st.markdown(f"👁️ {v.get('views', 0)}")
            with col3:
                # ফলোয়ার আপডেট সিস্টেম
                if st.button(f"➕ Follow ({v.get('followers', 0)})", key=f"fl_{v['id']}"):
                    supabase.table("videos").update({"followers": v.get('followers', 0) + 1}).eq("id", v['id']).execute()
                    st.toast(f"Followed {v['uploader_name']}")
                    st.rerun()
            st.markdown("---")

# --- ২. ভিডিও আপলোড (২ এমবি ও ১৫ সেকেন্ড লিমিট) ---
elif tab == "📤 Upload Video":
    if not st.session_state.user:
        st.warning("Please login first!")
    else:
        file = st.file_uploader("ভিডিও সিলেক্ট করুন (অটো ২ এমবি ও ১৫ সেকেন্ড হবে)", type=['mp4'])
        if st.button("🚀 Publish") and file:
            # দৈনিক লিমিট চেক (৩টি ভিডিও)
            today = datetime.now().strftime("%Y-%m-%d")
            check = supabase.table("videos").select("*").eq("uploader_name", st.session_state.user).gte("created_at", today).execute()
            
            if len(check.data) >= 3:
                st.error("আজকের ৩টি ভিডিওর লিমিট শেষ!")
            else:
                with st.spinner("ভিডিও প্রসেসিং হচ্ছে..."):
                    auto_cleanup() # আপলোডের আগে পুরনো ভিডিও ডিলিট
                    t_in, t_out = "temp_in.mp4", "temp_out.mp4"
                    with open(t_in, "wb") as f: f.write(file.getvalue())
                    
                    # শক্তিশালী কমান্ড: ১৫ সেকেন্ডে কাটা + ২ এমবি সাইজ কন্ট্রোল
                    subprocess.run(f"ffmpeg -i {t_in} -t 15 -vf scale=-2:480 -vcodec libx264 -crf 32 -b:v 800k -fs 2M -y {t_out}", shell=True)
                    
                    target = random.choice(STORAGE_KEYS)
                    s_bot = create_client(target['url'], target['key'])
                    v_uuid = f"vid_{uuid.uuid4()}.mp4"
                    
                    with open(t_out, "rb") as f:
                        s_bot.storage.from_("videos").upload(v_uuid, f.read())
                    
                    v_url = s_bot.storage.from_("videos").get_public_url(v_uuid)
                    
                    supabase.table("videos").insert({
                        "video_url": v_url,
                        "uploader_name": st.session_state.user,
                        "uploader_pic": st.session_state.pic,
                        "likes": 0,
                        "views": random.randint(5, 50),
                        "followers": 0
                    }).execute()
                    
                    st.success("ভিডিও পাবলিশ হয়েছে!")
                    os.remove(t_in); os.remove(t_out)
                    st.rerun()
