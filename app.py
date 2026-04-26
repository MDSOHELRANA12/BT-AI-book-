import streamlit as st
from supabase import create_client
import uuid
import streamlit.components.v1 as components

# --- 1. Database Connection (Secure Configuration) ---
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

# --- 2. Page Configuration ---
st.set_page_config(page_title="Bt-Ai World Intelligence", layout="wide")

# --- 3. Advertisement Ad Codes (Banners 1-4) ---
ad_code_1 = """<script type="text/javascript"> atOptions = { 'key' : '342950879f2064f7255ad047622381c8', 'format' : 'iframe', 'height' : 50, 'width' : 320, 'params' : {} }; </script> <script type="text/javascript" src="https://www.highperformanceformat.com/342950879f2064f7255ad047622381c8/invoke.js"></script>"""
ad_code_2 = """<script type="text/javascript"> atOptions = { 'key' : '5327bebb34c787d2ccfb1c36bcfa9d6e', 'format' : 'iframe', 'height' : 250, 'width' : 300, 'params' : {} }; </script> <script type="text/javascript" src="https://www.highperformanceformat.com/5327bebb34c787d2ccfb1c36bcfa9d6e/invoke.js"></script>"""
ad_code_3 = """<script async="async" data-cfasync="false" src="https://pl29264300.profitablecpmratenetwork.com/3d5c1921120aef030a2a6dd72337ba1d/invoke.js"></script><div id="container-3d5c1921120aef030a2a6dd72337ba1d"></div>"""
ad_code_4 = """<script src="https://pl29264299.profitablecpmratenetwork.com/e5/58/5e/e5585e56ecc6ca2a987116ca54b2614d.js"></script>"""

# --- 4. Premium UI/UX Design (White Text on Black) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    .stApp, p, div, span, h1, h2, h3, label { color: #ffffff !important; }
    .card { 
        background: #111111; 
        padding: 20px; 
        border-radius: 15px; 
        border: 1px solid #333; 
        margin-bottom: 25px; 
        box-shadow: 0px 5px 15px rgba(255,255,255,0.05);
    }
    .direct-link-btn {
        display: block; padding: 12px; 
        background: linear-gradient(45deg, #ff0000, #ff4500);
        color: #ffffff !important; text-align: center; 
        text-decoration: none; font-size: 18px; font-weight: bold; 
        border-radius: 10px; border: 2px solid #fff; margin-top: 10px;
    }
    .ad-box { text-align: center; margin: 20px 0; padding: 10px; background: #000; border-radius: 10px; border: 1px dashed #444; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. Sidebar Navigation ---
st.sidebar.title("✪ Bt-Ai Global Pro")
menu = ["🏠 Global Feed", "📤 Publish Video", "💰 Wallet & Bank", "👤 Profile & Security", "⚙️ Owner Control"]
choice = st.sidebar.selectbox("Dashboard Menu", menu)

# --- 6. Global Feed Section (Likes, Views, Ads) ---
if choice == "🏠 Global Feed":
    st.title("🌎 Global Trending Feed")
    try:
        v_data = supabase.table("videos").select("*").order("created_at", desc=True).execute()
        if v_data.data:
            for index, v in enumerate(v_data.data):
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.video(v['video_url'])
                
                # Direct Link Revenue Button
                d_link = "https://www.profitablecpmratenetwork.com/tgt6azn6?key=e753cbd6d9bae06d67051ed846419521"
                st.markdown(f'<a href="{d_link}" target="_blank" class="direct-link-btn">📽️ Watch Full Content & Earn</a>', unsafe_allow_html=True)
                
                # Interaction Row
                c1, c2, c3 = st.columns([1, 1, 2])
                if c1.button(f"❤️ Like ({v.get('likes', 0)})", key=f"lk_{v['id']}"):
                    supabase.table("videos").update({"likes": v.get('likes', 0) + 1, "views": v.get('views', 0) + 1}).eq("id", v['id']).execute()
                    st.rerun()
                c2.write(f"👁️ Views: {v.get('views', 0)}")
                c3.write(f"📊 Revenue: ${v.get('views', 0) * 0.01:.2f}")
                st.markdown('</div>', unsafe_allow_html=True)

                # Automated Ad Placement
                st.markdown('<div class="ad-box">', unsafe_allow_html=True)
                if index % 4 == 0: components.html(ad_code_1, height=70)
                elif index % 4 == 1: components.html(ad_code_2, height=270)
                elif index % 4 == 2: components.html(ad_code_3, height=200)
                else: components.html(ad_code_4, height=150)
                st.markdown('</div>', unsafe_allow_html=True)
    except:
        st.error("Error connecting to database feed.")

# --- 7. Upload Content Section ---
elif choice == "📤 Publish Video":
    st.title("📤 Publish Your Content")
    v_file = st.file_uploader("Select MP4 Video File", type=['mp4'])
    
    if st.button("Publish Now") and v_file:
        with st.spinner("Processing..."):
            f_name = f"{uuid.uuid4()}.mp4"
            try:
                # Storage Upload
                supabase.storage.from_("videos").upload(f_name, v_file.read())
                v_url = supabase.storage.from_("videos").get_public_url(f_name)
                # Database Entry
                supabase.table("videos").insert({"video_url": v_url, "likes": 0, "views": 0}).execute()
                st.success("Success! Video is live.")
                st.balloons()
            except Exception as e:
                st.error(f"Upload Failed: {e}")

# --- 8. Wallet & Payouts ---
elif choice == "💰 Wallet & Bank":
    st.title("💰 Total Earnings")
    v_total = supabase.table("videos").select("views").execute()
    total_views = sum([x['views'] for x in v_total.data]) if v_total.data else 0
    st.markdown(f"""
    <div class="card" style="text-align: center;">
        <h2>Current Balance</h2>
        <h1 style="font-size: 60px; color: #00ff00 !important;">${total_views * 0.01:.2f}</h1>
        <p>Keep sharing content to increase earnings!</p>
    </div>
    """, unsafe_allow_html=True)

# --- 9. Profile & Owner Access ---
elif choice == "👤 Profile & Security":
    st.title("👤 User Identity")
    st.markdown('<div class="card"><h3>Name: MD SOHEL RANA</h3><p>Verified Administrator</p></div>', unsafe_allow_html=True)

elif choice == "⚙️ Owner Control":
    st.title("⚙️ System Management")
    pwd = st.text_input("Enter Access Key", type="password")
    if pwd == "S$s123456789112233":
        st.success("Access Granted. System optimized for global use.")
import
