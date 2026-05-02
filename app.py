import streamlit as st
from supabase import create_client
import uuid
import random
import os
import subprocess
from datetime import datetime
from moviepy.editor import VideoFileClip 

# --- [জংশন বক্স শুরু] ---
MAIN_URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
MAIN_KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(MAIN_URL, MAIN_KEY)

# ১০টি স্টোরেজ চাবি (ভিডিও ফাইল এখানে জমা হবে)
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

MAX_VIDEOS = 100 # ১০০ ভিডিওর বেশি হলে অটো ডিলিট হবে
DAILY_LIMIT = 3  # একজন ইউজার দিনে ৩টি ভিডিওর বেশি দিতে পারবে না
# --- [জংশন বক্স শেষ] ---

st.set_page_config(page_title="BT AI book", layout="wide")

# --- ১. অটো ডিলিট ফাংশন (পুরানো ভিডিও ডিলিট করবে) ---
def delete_oldest_video():
    try:
        res = supabase.table("videos").select("*").order("created_at", asc=True).limit(1).execute()
        if res.data:
            old_v = res.data[0]
            v_url = old_v['video_url']
            for store in STORAGE_KEYS:
                if store['url'] in v_url:
                    s_bot = create_client(store['url'], store['key'])
                    f_path = v_url.split('/')[-1]
                    s_bot.storage.from_("videos").remove([f_path])
                    break
            supabase.table("videos").delete().eq("id", old_v['id']).execute()
    except: pass

def format_value(val):
    if val >= 1000000: return f"{val/1000000:.1f}M"
    elif val >= 1000: return f"{val/1000:.1f}K"
    return str(val)

# স্টাইল
st.markdown("""<style>.stApp { background-color: #000; color: #fff; }.video-card { background: #0d0d0d; border: 1px solid #333; border-radius: 15px; padding: 15px; margin-bottom: 50px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); max-width: 500px; margin-left: auto; margin-right: auto; }.stat-box { font-size: 14px; color: #00ff00; font-weight: bold; margin-right: 15px; }.btn-reward { display: block; width: 100%; padding: 12px; margin: 10px 0; background: linear-gradient(135deg, #ed1c24, #aa0000); color: white !important; text-align: center; border-radius: 8px; font-weight: bold; text-decoration: none; }</style>""", unsafe_allow_html=True)

st.title("🛡️ BT AI book")

if 'user' not in st.session_state: st.session_state.user = None

# নেভিগেশন
tab = st.sidebar.radio("BT Menu", ["🌍 World Feed", "📤 Upload Video", "🔐 Profile"])

# --- প্রোফাইল/লগইন ---
if tab == "🔐 Profile":
    if not st.session_state.user:
        u_name = st.sidebar.text_input("Enter Name")
        if st.sidebar.button("Join Now"):
            user_data = supabase.table("users").select("*").eq("username", u_name).execute()
            if user_data.data:
                st.session_state.user = u_name
                st.session_state.pic = user_data.data[0]['profile_pic']
                st.rerun()
            else:
                u_pic = st.sidebar.file_uploader("Upload Photo", type=['jpg','png'])
                if u_pic:
                    fname = f"p_{uuid.uuid4()}.jpg"
                    supabase.storage.from_("videos").upload(path=fname, file=u_pic.getvalue())
                    p_url = supabase.storage.from_("videos").get_public_url(fname)
                    supabase.table("users").insert({"username": u_name, "profile_pic": p_url}).execute()
                    st.session_state.user = u_name
                    st.session_state.pic = p_url
                    st.rerun()
    else:
        st.sidebar.image(st.session_state.pic, width=100)
        st.sidebar.success(f"Hello, {st.session_state.user}")
        if st.sidebar.button("Logout"): st.session_state.user = None; st.rerun()

# --- ওয়ার্ল্ড ফিড (অটো ভিউ ভাইরাল অ্যালগরিদম) ---
elif tab == "🌍 World Feed":
    try:
        res = supabase.table("videos").select("*").execute()
        data = res.data if res.data else []
        random.shuffle(data)
        for v in data:
            v_id = v['id']
            st.markdown('<div class="video-card">', unsafe_allow_html=True)
            st.markdown(f"**👤 {v['uploader_name']}**")
            st.video(v['video_url'])
            
            # --- অটো ভিউ বুস্ট ---
            new_v = v['views'] + random.randint(2, 8)
            supabase.table("videos").update({"views": new_v}).eq("id", v_id).execute()
            
            st.markdown(f'<span class="stat-box">👁️ {format_value(new_v)} Views</span> <span class="stat-box">❤️ {format_value(v["likes"])} Likes</span> <span class="stat-box">👥 {format_value(v["followers"])} Followers</span>', unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button(f"❤️ Like", key=f"L_{v_id}"):
                    supabase.table("videos").update({"likes": v['likes']+1}).eq("id", v_id).execute(); st.rerun()
            with c2:
                if st.button(f"➕ Follow", key=f"F_{v_id}"):
                    supabase.table("videos").update({"followers": v['followers']+1}).eq("id", v_id).execute(); st.success("Followed!"); st.rerun()
            
            st.markdown(f'<a href="https://www.profitablecpmratenetwork.com/tgt6azn6?key=e753cbd6d9bae06d67051ed846419521" target="_blank" class="btn-reward">💎 Claim Diamond Reward</a>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    except: st.info("Loading Feed...")

# --- আপলোড (অটো কনভার্ট ও ২ এমবি লিমিট) ---
elif tab == "📤 Upload Video":
    if not st.session_state.user: st.warning("লগইন না করলে ভিডিও আপলোড করা যাবে না!")
    else:
        v_file = st.file_uploader("Select Video (MP4)", type=['mp4'])
        if st.button("🚀 Publish Now") and v_file:
            # ডেইলি লিমিট চেক
            today = datetime.now().strftime("%Y-%m-%d")
            check = supabase.table("videos").select("*").eq("uploader_name", st.session_state.user).gte("created_at", today).execute()
            
            if len(check.data) >= DAILY_LIMIT:
                st.error(f"❌ আজকে আর হবে না! প্রতিদিন শুধু {DAILY_LIMIT}টি ভিডিও দেওয়া যায়।")
            else:
                with st.spinner("🤖 ২ এমবি-তে কনভার্ট হচ্ছে..."):
                    try:
                        # অটো ডিলিট চেক (১০০ পূর্ণ হলে)
                        count_res = supabase.table("videos").select("*", count='exact').execute()
                        if count_res.count >= MAX_VIDEOS: delete_oldest_video()
                        
                        t_in, t_out = "in.mp4", "out.mp4"
                        with open(t_in, "wb") as f: f.write(v_file.getvalue())
                        
                        # --- ২ এমবি অটো কনভার্ট কমান্ড ---
                        subprocess.run(f"ffmpeg -i {t_in} -vcodec libx264 -crf 28 -fs 2M -y {t_out}", shell=True)
                        
                        v_uuid = f"v_{uuid.uuid4()}.mp4"
                        target = random.choice(STORAGE_KEYS)
                        s_bot = create_client(target['url'], target['key'])
                        with open(t_out, "rb") as f: s_bot.storage.from_("videos").upload(path=v_uuid, file=f.read())
                        v_url = s_bot.storage.from_("videos").get_public_url(v_uuid)
                        
                        # ডাটাবেজে সেভ (বোনাস ভিউ সহ)
                        supabase.table("videos").insert({
                            "video_url": v_url, "uploader_name": st.session_state.user,
                            "uploader_pic": st.session_state.pic, "likes": random.randint(10,30),
                            "views": random.randint(100,300), "followers": random.randint(5,15)
                        }).execute()
                        
                        st.success("✅ ভিডিও ২ এমবি সাইজে কনভার্ট হয়ে পাবলিশ হয়েছে!")
                        os.remove(t_in); os.remove(t_out)
                    except Exception as e: st.error(f"Error: {e}")
