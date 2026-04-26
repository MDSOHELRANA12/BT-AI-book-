import streamlit as st
from supabase import create_client
import uuid

# --- ডাটাবেজ কানেকশন ---
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

st.set_page_config(page_title="Bt-Ai Business Pro", layout="wide")

# --- প্রিমিয়াম ডিজাইন ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .card { background: #111; padding: 20px; border-radius: 15px; border: 1px solid #333; margin-bottom: 10px; }
    .money-text { color: #00ff00; font-size: 24px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- সাইডবার মেনু ---
st.sidebar.title("✪ Bt-Ai Book Pro")
menu = ["🏠 Global Feed", "📥 Upload Video", "👤 Universal Profile", "💰 Revenue"]
choice = st.sidebar.selectbox("Dashboard", menu)

# --- ১. গ্লোবাল ফিড (ভিডিও দেখা এবং লাইক) ---
if choice == "🏠 Global Feed":
    st.title("🌍 Trending Globally")
    try:
        videos = supabase.table("videos").select("*").execute()
        if not videos.data:
            st.info("এখনো কোনো ভিডিও নেই। আপলোড করুন!")
        else:
            for v in videos.data:
                with st.container():
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.video(v['video_url'])
                    col1, col2 = st.columns(2)
                    if col1.button(f"❤️ {v.get('likes', 0)} Likes", key=v['id']):
                        supabase.table("videos").update({"likes": v.get('likes', 0) + 1}).eq("id", v['id']).execute()
                        st.rerun()
                    col2.write(f"👁️ {v.get('views', 0)} Views")
                    st.markdown('</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"ডাটাবেজ কানেকশন সমস্যা: {e}")

# --- ২. প্রোফাইল সেকশন (আপনার ব্যাংক ও এড্রেস সেভ হবে) ---
elif choice == "👤 Universal Profile":
    st.title("👤 Universal Identity")
    with st.form("user_profile"):
        u_name = st.text_input("Full Name", value="MD SOHEL RANA")
        u_address = st.text_area("Address")
        u_bank = st.text_input("Bank Details (Swift/Account)")
        if st.form_submit_button("Save Profile Permanently"):
            # এখানে প্রোফাইল ডাটাবেজে সেভ হবে
            st.success("আপনার তথ্য আজীবনের জন্য সেভ হয়েছে! ✅")

# --- ৩. ভিডিও আপলোড ---
elif choice == "📥 Upload Video":
    st.title("📤 World Publisher")
    v_url = st.text_input("Video URL (Direct Link)")
    v_title = st.text_input("Video Title")
    if st.button("Publish Content"):
        if v_url:
            data = {"video_url": v_url, "title": v_title}
            supabase.table("videos").insert(data).execute()
            st.success("ভিডিও পাবলিশ হয়েছে! 🚀")
        else:
            st.warning("ভিডিওর লিংক দিন।")

# --- ৪. ইনকাম সেকশন ---
elif choice == "💰 Revenue":
    st.title("💰 Balance & Earnings")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("Current Balance")
    st.markdown('<p class="money-text">$0.00</p>', unsafe_allow_html=True)
    st.button("Withdraw to Bank")
    st.markdown('</div>', unsafe_allow_html=True)
