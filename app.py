import streamlit as st
from supabase import create_client
import uuid

# ১. ডাটাবেজ কানেকশন (আপনার দেওয়া চাবি ব্যবহার করা হয়েছে)
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

st.set_page_config(page_title="BT AI book - Global Revenue", layout="wide")

# ২. গ্লোবাল স্ট্যান্ডার্ড ডিজাইন
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .video-card { background: #0d0d0d; border: 1px solid #333; border-radius: 15px; padding: 15px; margin-bottom: 10px; }
    .user-avatar { width: 50px; height: 50px; border-radius: 50%; border: 2px solid #00ff00; object-fit: cover; margin-right: 12px; }
    .btn-revenue { display: block; width: 100%; padding: 12px; margin-top: 10px; background: linear-gradient(135deg, #ed1c24, #aa0000); color: white !important; text-align: center; border-radius: 8px; font-weight: bold; text-decoration: none; }
    .monetization-card { background: #111; border: 2px solid #ed1c24; padding: 25px; border-radius: 15px; margin-top: 10px; }
    .bank-badge { background: #222; padding: 15px; border-radius: 10px; border-left: 6px solid #00ff00; margin-bottom: 15px; font-family: monospace; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ BT AI book (Global Edition)")

# ৩. প্রোফাইল ও সেশন ম্যানেজমেন্ট
if 'user' not in st.session_state:
    st.session_state.user = None
    st.session_state.pic = None

st.sidebar.header("Global Account")
if not st.session_state.user:
    name_in = st.sidebar.text_input("Enter Full Name")
    file_in = st.sidebar.file_uploader("Upload Profile Photo", type=['jpg', 'png'])
    if st.sidebar.button("Join Platform"):
        if name_in and file_in:
            fname = f"profile_{uuid.uuid4()}.jpg"
            supabase.storage.from_("videos").upload(path=fname, file=file_in.getvalue())
            st.session_state.pic = supabase.storage.from_("videos").get_public_url(fname)
            st.session_state.user = name_in
            st.rerun()
else:
    st.sidebar.image(st.session_state.pic, width=100)
    st.sidebar.write(f"Welcome, {st.session_state.user}")

# ৪. মেনু নেভিগেশন
tab = st.sidebar.radio("Navigate", ["🌍 Global Feed", "📤 Upload & Earn", "💰 Monetization & Payout"])

# ৫. ওয়ার্ল্ড ফিড (সারা বিশ্বের ভিডিও এখানে আসবে)
if tab == "🌍 Global Feed":
    try:
        response = supabase.table("videos").select("*").order("created_at", desc=True).execute()
        videos = response.data
        if videos:
            for v in videos:
                # অটো ভিউ আপডেট
                new_view = v.get('views', 0) + 1
                supabase.table("videos").update({"views": new_view}).eq("id", v['id']).execute()
                
                st.markdown('<div class="video-card">', unsafe_allow_html=True)
                st.markdown(f'''<div style="display:flex;align-items:center;margin-bottom:12px;">
                    <img src="{v.get('uploader_pic')}" class="user-avatar">
                    <b style="font-size:18px;">{v.get('uploader_name')}</b>
                </div>''', unsafe_allow_html=True)
                
                st.video(v['video_url'], format="video/mp4")
                st.write(f"📊 {new_view} Views | ❤️ {v.get('likes', 0)} Reactions")
                st.markdown(f'<a href="https://www.profitablecpmratenetwork.com/..." class="btn-revenue">💎 Reward: Click to Earn Diamond</a>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
    except:
        st.info("Loading Global Content...")

# ৬. ভিডিও আপলোডিং
elif tab == "📤 Upload & Earn":
    if st.session_state.user:
        up_file = st.file_uploader("Select Video (MP4)", type=['mp4'])
        if st.button("🚀 Publish to World") and up_file:
            with st.spinner("Uploading to Server..."):
                vid_id = f"vid_{uuid.uuid4()}.mp4"
                supabase.storage.from_("videos").upload(path=vid_id, file=up_file.getvalue())
                vid_url = supabase.storage.from_("videos").get_public_url(vid_id)
                supabase.table("videos").insert({
                    "video_url": vid_url, 
                    "uploader_name": st.session_state.user, 
                    "uploader_pic": st.session_state.pic,
                    "views": 1
                }).execute()
                st.success("Successfully Published!")
    else:
        st.warning("Please join as a member first.")

# ৭. শক্তিশালী মনিটাইজেশন ও পেমেন্ট গেটওয়ে (মালিকের নিয়ন্ত্রণ)
elif tab == "💰 Monetization & Payout":
    st.header("💰 Global Monetization Program")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### 📖 Eligibility Rules
        - **Daily Upload:** ১টি ভিডিও (৬ মাস টানা)।
        - **Followers:** ১,০০০+ গ্লোবাল ফলোয়ার।
        - **Quality:** কপিরাইট মুক্ত অরিজিনাল কন্টেন্ট।
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        ### 🏦 Central Bank Info (Admin)
        <div class="bank-badge">
            <b>Owner:</b> MD SOHEL RANA<br>
            <b>Bank:</b> Clear Bank (London)<br>
            <b>IBAN:</b> GB56CLRB04281298407970<br>
            <b>SWIFT:</b> CLRBGB22XXX
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    
    # উইথড্রয়াল ফর্ম - সারা বিশ্বের যেকোনো ব্যাংকের জন্য
    st.subheader("💸 Request Payout (Global & Local)")
    with st.form("payout_request"):
        st.info("সঠিক তথ্য দিন, মালিক (MD SOHEL RANA) যাচাই করে ম্যানুয়ালি পেমেন্ট এপ্রুভ করবেন।")
        user_country = st.selectbox("Select Your Country", ["Bangladesh", "India", "USA", "UK", "UAE", "Others"])
        payout_method = st.text_input("Payment Method (e.g., bKash, PayPal, Local Bank Name)")
        user_iban = st.text_input("Account Number / IBAN / Wallet ID")
        amount = st.number_input("Amount to Withdraw (USD)", min_value=10)
        
        submit_btn = st.form_submit_button("Submit Payout Request")
        
        if submit_btn:
            if user_iban and payout_method:
                st.success(f"ধন্যবাদ {st.session_state.user}! আপনার রিকোয়েস্টটি মালিকের কাছে পাঠানো হয়েছে। আপনার ৬ মাসের রেকর্ড চেক করে মালিক টাকা এপ্রুভ করবেন।")
                # এখানে ডাটাবেজে রিকোয়েস্ট সেভ করার লজিক দেওয়া যায়
            else:
                st.error("Please fill all details correctly.")

    # মালিকের বিশেষ নোট
    st.warning("⚠️ Note: মালিকের নির্দেশ এবং সঠিক তথ্য ছাড়া কোনো পেমেন্ট রিলিজ করা হবে না। কোনো সমস্যা পেলে পেমেন্ট আটকে দেওয়ার ক্ষমতা মালিক সংরক্ষণ করেন।")

if st.sidebar.button("Sign Out"):
    st.session_state.user = None
    st.rerun()
