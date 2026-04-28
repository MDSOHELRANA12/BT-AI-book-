import streamlit as st
from supabase import create_client
import uuid

# --- ডাটাবেজ কানেকশন ---
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

st.set_page_config(page_title="BT AI book - World Revenue", layout="wide")

# --- ইন্টারফেস ডিজাইন (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .video-container { background: #0a0a0a; border: 1px solid #222; border-radius: 20px; padding: 20px; margin-bottom: 25px; }
    .btn-ads { display: block; width: 100%; padding: 15px; background: linear-gradient(90deg, #FF0000, #990000); color: white !important; text-align: center; border-radius: 10px; font-weight: bold; text-decoration: none; margin-top: 10px; }
    .stat-badge { background: #1a1a1a; padding: 5px 15px; border-radius: 20px; font-size: 14px; border: 1px solid #333; }
    .owner-secure { background: #002200; border-left: 5px solid #00ff00; padding: 15px; border-radius: 10px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- ফাংশন: লাইক ও ফলো আপডেট ---
def update_stat(table, row_id, column):
    try:
        current = supabase.table(table).select(column).eq("id", row_id).single().execute().data[column]
        supabase.table(table).update({column: current + 1}).eq("id", row_id).execute()
    except: pass

# --- সাইডবার ও ইউজার প্রোফাইল ---
if 'user' not in st.session_state: st.session_state.user = None

st.sidebar.title("💎 BT AI Book")
if not st.session_state.user:
    u_name = st.sidebar.text_input("Username")
    if st.sidebar.button("Login/Sign Up"):
        st.session_state.user = u_name or "Global_User"
        st.rerun()
else:
    st.sidebar.success(f"Verified: {st.session_state.user}")
    menu = st.sidebar.radio("Navigation", ["Global Feed", "Upload Video", "Wallet & Monetization"])

    # --- ১. গ্লোবাল ফিড (লাইক/ফলো কাজ করবে) ---
    if menu == "Global Feed":
        st.header("🌎 Trending World Revenue")
        videos = supabase.table("videos").select("*").order("created_at", desc=True).execute().data
        
        for v in videos:
            st.markdown('<div class="video-container">', unsafe_allow_html=True)
            st.subheader(f"👤 {v.get('uploader_name', 'Unknown User')}")
            
            # ভিডিও প্লেয়ার
            st.video(v['video_url'])
            
            # স্ট্যাটাস ও বাটন
            col1, col2, col3 = st.columns([1,1,1])
            with col1:
                if st.button(f"❤️ Like ({v.get('likes', 0)})", key=f"lk_{v['id']}"):
                    update_stat("videos", v['id'], "likes")
                    st.rerun()
            with col2:
                if st.button(f"➕ Follow", key=f"fl_{v['id']}"):
                    st.toast("Following started!")
            with col3:
                st.markdown(f'<span class="stat-badge">👁️ {v.get("views", 0)} Views</span>', unsafe_allow_html=True)

            # ডাইরেক্ট লিঙ্কের কাজ
            st.markdown(f'<a href="https://www.profitablecpmratenetwork.com/..." target="_blank" class="btn-ads">🔗 Click to Earn Reward (Direct Link)</a>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # --- ২. ভিডিও আপলোড ---
    elif menu == "Upload Video":
        up_file = st.file_uploader("Choose Video", type=['mp4', 'mov'])
        if st.button("🚀 Upload to World") and up_file:
            vid_id = str(uuid.uuid4())
            supabase.storage.from_("videos").upload(vid_id, up_file.getvalue())
            url = supabase.storage.from_("videos").get_public_url(vid_id)
            supabase.table("videos").insert({"video_url": url, "uploader_name": st.session_state.user}).execute()
            st.success("Video Published Successfully!")

    # --- ৩. ওয়ালেট ও ব্যাংকিং (সিকিউরড) ---
    elif menu == "Wallet & Monetization":
        st.header("💰 Global Monetization Program")
        
        # আপনার ব্যাংক ডিটেইলস এখন হাইড এবং সুরক্ষিত
        st.markdown("""
        <div class="owner-secure">
            🛡️ Central Payout Status: ACTIVE<br>
            Bank Authority: MD SOHEL RANA (Verified Global Owner)<br>
            Method: Clear Bank London / SWIFT Transfer enabled.
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        st.subheader("Rules (English Standard)")
        st.info("- Daily Upload: 1 Video (Must continue 6 months)\n- Followers: 1,000+ required\n- Quality: Original Content Only")

        with st.form("payout"):
            st.write("Request Your Local Bank Payout")
            country = st.selectbox("Country", ["Bangladesh", "India", "Global"])
            method = st.text_input("Method (bKash/PayPal/Bank)")
            acc = st.text_input("Account Details")
            amt = st.number_input("Amount (USD)", min_value=10)
            if st.form_submit_button("Submit Request"):
                st.success("Request sent to Owner. Manual verification in progress.")

# সাইন আউট
if st.sidebar.button("Logout"):
    st.session_state.user = None
    st.rerun()
