import streamlit as st
from supabase import create_client
import uuid
import streamlit.components.v1 as components

# --- 1. Secure Database Connection ---
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

# --- 2. Global Page Setup ---
st.set_page_config(page_title="Bt-Ai World Intelligence", layout="wide")

# --- 3. Professional Ad Integration (Banners 1-4) ---
ad_code_1 = """<script type="text/javascript"> atOptions = { 'key' : '342950879f2064f7255ad047622381c8', 'format' : 'iframe', 'height' : 50, 'width' : 320, 'params' : {} }; </script> <script type="text/javascript" src="https://www.highperformanceformat.com/342950879f2064f7255ad047622381c8/invoke.js"></script>"""
ad_code_2 = """<script type="text/javascript"> atOptions = { 'key' : '5327bebb34c787d2ccfb1c36bcfa9d6e', 'format' : 'iframe', 'height' : 250, 'width' : 300, 'params' : {} }; </script> <script type="text/javascript" src="https://www.highperformanceformat.com/5327bebb34c787d2ccfb1c36bcfa9d6e/invoke.js"></script>"""
ad_code_3 = """<script async="async" data-cfasync="false" src="https://pl29264300.profitablecpmratenetwork.com/3d5c1921120aef030a2a6dd72337ba1d/invoke.js"></script><div id="container-3d5c1921120aef030a2a6dd72337ba1d"></div>"""
ad_code_4 = """<script src="https://pl29264299.profitablecpmratenetwork.com/e5/58/5e/e5585e56ecc6ca2a987116ca54b2614d.js"></script>"""

# --- 4. Premium Interface Design (All White Text) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff !important; }
    h1, h2, h3, p, span, div, label { color: #ffffff !important; }
    .card { 
        background: #111111; padding: 25px; border-radius: 15px; 
        border: 1px solid #333; margin-bottom: 25px;
    }
    .revenue-btn {
        display: block; padding: 15px; background: linear-gradient(45deg, #ff0000, #cc0000);
        color: white !important; text-align: center; text-decoration: none;
        font-size: 20px; font-weight: bold; border-radius: 10px; border: 2px solid #fff;
    }
    .ad-wrapper { text-align: center; margin: 20px 0; background: #000; border-radius: 10px; border: 1px dashed #555; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. Navigation Sidebar ---
st.sidebar.title("✪ Bt-Ai Global Pro")
menu = ["🏠 Global Feed", "📤 Publish Video", "💰 Wallet & Bank", "👤 Profile & Security", "⚙️ Owner Control"]
choice = st.sidebar.selectbox("Select Action", menu)

# --- 6. Global Video Feed (Likes, Views, Payout) ---
if choice == "🏠 Global Feed":
    st.title("🌎 Global Trending Content")
    try:
        v_data = supabase.table("videos").select("*").order("created_at", desc=True).execute()
        if v_data.data:
            for index, v in enumerate(v_data.data):
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.video(v['video_url'])
                
                # Direct Earning Link
                d_link = "https://www.profitablecpmratenetwork.com/tgt6azn6?key=e753cbd6d9bae06d67051ed846419521"
                st.markdown(f'<a href="{d_link}" target="_blank" class="revenue-btn">📽️ Watch & Earn Real Cash</a>', unsafe_allow_html=True)
                
                # Stats Row
                col1, col2, col3 = st.columns([1, 1, 2])
                if col1.button(f"❤️ Like ({v.get('likes', 0)})", key=f"lk_{v['id']}"):
                    supabase.table("videos").update({"likes": v.get('likes', 0) + 1, "views": v.get('views', 0) + 1}).eq("id", v['id']).execute()
                    st.rerun()
                col2.write(f"👁️ Views: {v.get('views', 0)}")
                col3.write(f"💵 Earned: ${v.get('views', 0) * 0.01:.2f}")
                st.markdown('</div>', unsafe_allow_html=True)

                # Cyclic Ad Placement
                st.markdown('<div class="ad-wrapper">', unsafe_allow_html=True)
                if index % 4 == 0: components.html(ad_code_1, height=70)
                elif index % 4 == 1: components.html(ad_code_2, height=270)
                elif index % 4 == 2: components.html(ad_code_3, height=200)
                else: components.html(ad_code_4, height=150)
                st.markdown('</div>', unsafe_allow_html=True)
    except:
        st.error("Connection lost. Please refresh.")

# --- 7. High-Speed Video Upload ---
elif choice == "📤 Publish Video":
    st.title("📤 Publish Your Content")
    file = st.file_uploader("Upload MP4 File", type=['mp4'])
    if st.button("Publish Now") and file:
        with st.spinner("Uploading to Global Server..."):
            filename = f"{uuid.uuid4()}.mp4"
            try:
                supabase.storage.from_("videos").upload(filename, file.read())
                url = supabase.storage.from_("videos").get_public_url(filename)
                supabase.table("videos").insert({"video_url": url, "likes": 0, "views": 0}).execute()
                st.success("Success! Video is now live globally.")
                st.balloons()
            except Exception as e:
                st.error(f"Upload error: {e}")

# --- 8. Wallet & Automatic Payout ---
elif choice == "💰 Wallet & Bank":
    st.title("💰 Your Global Payout")
    data = supabase.table("videos").select("views").execute()
    total_v = sum([x['views'] for x in data.data]) if data.data else 0
    st.markdown(f"""
    <div class="card" style="text-align: center;">
        <h2>Current Total Balance</h2>
        <h1 style="font-size: 60px; color: #00ff00 !important;">${total_v * 0.01:.2f}</h1>
        <p>Minimum withdrawal: $50.00</p>
    </div>
    """, unsafe_allow_html=True)

# --- 9. Profile & Admin Access ---
elif choice == "👤 Profile & Security":
    st.title("👤 Security Profile")
    st.markdown('<div class="card"><h3>Admin: MD SOHEL RANA</h3><p>Status: Fully Protected</p></div>', unsafe_allow_html=True)

elif choice == "⚙️ Owner Control":
    st.title("⚙️ Owner Dashboard")
    if st.text_input("Access Key", type="password") == "S$s123456789112233":
        st.success("Welcome, Sohel Rana! All systems are optimized.")
import
