import streamlit as st
from supabase import create_client
import uuid
import random
import os
import subprocess
from datetime import datetime

# --- [জংশন বক্স] ---
# মেইন প্রজেক্ট - এখানে শুধু ডাটাবেজ থাকবে (লাইক, ভিউ, ছবি)
MAIN_URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
MAIN_KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(MAIN_URL, MAIN_KEY)

# ১০টি চাবি - এখানে শুধু ভিডিও ফাইলগুলো (MP4) জমা হবে
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

MAX_VIDEOS = 100 # ১০০ ভিডিওর পর অটো ডিলিট শুরু হবে
# --- [জংশন বক্স শেষ] ---

st.set_page_config(page_title="BT AI book", layout="wide")

def delete_oldest_video():
    try:
        res = supabase.table("videos").select("*").order("created_at", asc=True).limit(1).execute()
        if res.data:
            old_v = res.data[0]
            v_url = old_v['video_url']
            for store in STORAGE_KEYS:
                if store['url'] in v_url:
                    s_bot = create_client(store['url'], store['key'])
                    f_name = v_url.split('/')[-1]
                    s_bot.storage.from_("videos").remove([f_name])
                    break
            supabase.table("videos").delete().eq("id", old_v['id']).execute()
    except: pass

st.markdown("""<style>.stApp { background-color: #000; color: #fff; }.video-card { background: #0d0d0d; border: 1px solid #333; border-radius: 15px; padding: 15px; margin-bottom: 50px; max-width: 500px; margin-left: auto; margin-right: auto; }.stat-box { font-size: 14px; color: #00ff00; font-weight: bold; margin-right: 15px; }.btn-reward { display: block; width: 100%; padding: 12px; margin: 10px 0; background: linear-gradient(135deg, #ed1c24, #aa0000); color: white !important; text-align: center; border-radius: 8px; font-weight: bold; text-decoration: none; }</style>""", unsafe_allow_html=True)

if 'user' not in st.session_state: st.session_state.user = None

tab = st.sidebar.radio("BT Menu", ["🌍 World Feed", "📤 Upload Video", "🔐 Profile"])

# প্রোফাইল ম্যানেজমেন্ট (ছবি মেইন প্রজেক্টে জমা হবে)
if tab == "🔐 Profile":
    if not st.session_state.user:
        u_name = st.sidebar.text_input("Name")
        if st.sidebar.button("Login/Join"):
            user_data = supabase.table("users").select("*").eq("username", u_name).execute()
            if user_data.data:
                st.session_state.user = u_name
                st.session_state.pic = user_data.data[0]['profile_pic']
                st.rerun()
            else:
                u_pic = st.sidebar.file_uploader("Upload Profile Photo", type=['jpg','png'])
                if u_pic:
                    fname = f"p_{uuid.uuid4()}.jpg"
                    supabase.storage.from_("videos").upload(path=fname, file=u_pic.getvalue())
                    p_url = supabase.storage.from_("videos").get_public_url(fname)
                    supabase.table("users").insert({"username": u_name, "profile_pic": p_url}).execute()
                    st.session_state.user = u_name; st.session_state.pic = p_url; st.rerun()
    else:
        st.sidebar.image(st.session_state.pic, width=100)
        st.sidebar.write(f"Welcome, {st.session_state.user}")
        if st.sidebar.button("Logout"): st.session_state.user = None; st.rerun()

# ভিডিও ফিড (সব চাবি থেকে ডাটা দেখাবে)
elif tab == "🌍 World Feed":
    st.title("🛡️ BT AI book")
    try:
        res = supabase.table("videos").select("*").execute()
        v_list = res.data if res.data else []
        random.shuffle(v_list)
        for v in v_list:
            v_id = v['id']
            st.markdown('<div class="video-card">', unsafe_allow_html=True)
            st.markdown(f"**👤 {v['uploader_name']}**")
            st.video(v['video_url'])
            new_v = v['views'] + random.randint(2, 5)
            supabase.table("videos").update({"views": new_v}).eq("id", v_id).execute()
            st.markdown(f'<span class="stat-box">👁️ {new_v}</span> <span class="stat-box">❤️ {v["likes"]}</span> <span class="stat-box">👥 {v["followers"]}</span>', unsafe_allow_html=True)
            st.markdown(f'<a href="https://www.profitablecpmratenetwork.com/tgt6azn6" target="_blank" class="btn-reward">💎 Claim Diamond</a>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    except: st.info("Loading...")

# আপলোড (ভিডিও যাবে বাকি ১০টি চাবিতে, ডাটা আসবে মেইন প্রজেক্টে)
elif tab == "📤 Upload Video":
    if not st.session_state.user: st.warning("লগইন করুন!")
    else:
        file = st.file_uploader("Select MP4 (Auto Convert to 2MB)", type=['mp4'])
        if st.button("🚀 Publish") and file:
            with st.spinner("🤖 কমপ্রেশন ও ডিস্ট্রিবিউট হচ্ছে..."):
                try:
                    # ১০০ ভিডিওর বেশি হলে অটো ডিলিট
                    count_res = supabase.table("videos").select("*", count='exact').execute()
                    if count_res.count >= MAX_VIDEOS: delete_oldest_video()
                    
                    t_in, t_out = "temp_in.mp4", "temp_out.mp4"
                    with open(t_in, "wb") as f: f.write(file.getvalue())
                    
                    # ভিডিও ২ এমবি তে রূপান্তর
                    subprocess.run(f"ffmpeg -i {t_in} -vcodec libx264 -crf 28 -fs 2M -y {t_out}", shell=True)
                    
                    v_uuid = f"v_{uuid.uuid4()}.mp4"
                    # লটারির মাধ্যমে ১০টি চাবির একটিতে ভিডিও পাঠানো
                    target = random.choice(STORAGE_KEYS)
                    s_bot = create_client(target['url'], target['key'])
                    
                    with open(t_out, "rb") as f: 
                        s_bot.storage.from_("videos").upload(path=v_uuid, file=f.read())
                    
                    v_url = s_bot.storage.from_("videos").get_public_url(v_uuid)
                    
                    # ডাটাবেজ এন্ট্রি মেইন প্রজেক্টে
                    supabase.table("videos").insert({
                        "video_url": v_url, "uploader_name": st.session_state.user,
                        "uploader_pic": st.session_state.pic, "likes": random.randint(10,50),
                        "views": random.randint(100,500), "followers": random.randint(5,20)
                    }).execute()
                    
                    st.success("পাবলিশ হয়েছে! ভিডিওটি বাকি ১০টি চাবির একটিতে নিরাপদে আছে।")
                    os.remove(t_in); os.remove(t_out)
                except Exception as e: st.error(f"Error: {e}")
