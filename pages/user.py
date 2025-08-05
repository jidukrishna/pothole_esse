import streamlit as st
import data_storage
import location_raj
from streamlit_js_eval import get_geolocation
import re

# -------------------- Page Config --------------------
st.set_page_config(
    page_title="🌱 EcoRoad - Report Road Damage",
    page_icon="🌍",
    layout="wide"
)

# -------------------- Custom CSS --------------------
st.markdown("""
    <style>
        .main {
            background-color: #f0fff0;
        }
        .eco-card {
            border-radius: 12px;
            padding: 1.5rem;
            background-color: #e6f5e9;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
        }
        .stButton button {
            background-color: #2e7d32;
            color: white;
            border: None;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            transition: 0.3s;
        }
        .stButton button:hover {
            background-color: #1b5e20;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------- Title --------------------
st.title("🌿 EcoRoad - Road Filling Report")
st.markdown("Help us build better, safer roads with your report. Powered by the community, built for sustainability.")

# -------------------- Try Getting Geolocation --------------------
try:
    location = get_geolocation()["coords"]
except:
    location = None

# -------------------- Camera Input --------------------
with st.expander("📸 Capture Damage Area (Required)", expanded=True):
    enable = st.checkbox("Enable camera")
    picture = st.camera_input("Take a picture of the damaged road", disabled=not enable)

# -------------------- Location Section --------------------
with st.expander("📍 Get Location Info", expanded=True):
    location_button = st.button("Get Location")
    if location_button and location:
        lat = location['latitude']
        long = location['longitude']
        address = location_raj.reverse_location(lat, long)["display_name"]
        st.success(f"Latitude: {lat} \nLongitude: {long}")
        st.info(f"📌 Address: {address}")
    elif location_button:
        st.error("Unable to get location. Try enabling permissions or reload the page.")

# -------------------- Contact Info --------------------
with st.expander("📧 Contact Details", expanded=True):
    email = st.text_input("Email Address")
    ph_no = st.text_input("Phone Number")

# -------------------- Optional Dimensions --------------------
with st.expander("📏 Optional - Damage Dimensions"):
    st.subheader("Estimate the size of the damaged area")
    metrics = st.radio("Choose unit:", ["ft", "cm", "m"], horizontal=True)
    breadth = st.number_input("Breadth", step=0.2)
    length = st.number_input("Length", step=0.2)
    height = st.number_input("Depth", step=0.2)

# -------------------- Validators --------------------
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_valid_indian_number(phone):
    pattern = r'^(?:\+91|91|0)?[6-9]\d{9}$'
    return re.match(pattern, phone) is not None

# -------------------- Submit Section --------------------
submit = st.button("✅ Submit Report")

if submit:
    errors = []

    if not email or not is_valid_email(email):
        errors.append("❌ Invalid or missing email.")
    if not ph_no or not is_valid_indian_number(ph_no):
        errors.append("❌ Invalid or missing phone number.")
    if not picture:
        errors.append("❌ Please take a picture of the road damage.")
    if not location:
        errors.append("❌ Unable to retrieve location.")

    if errors:
        for error in errors:
            st.error(error)
    else:
        # Convert units
        conversion_factor = {"ft": 0.3048, "cm": 0.01, "m": 1}
        factor = conversion_factor[metrics]
        breadth = round(breadth * factor, 3)
        height = round(height * factor, 3)
        length = round(length * factor, 3)

        lat = location['latitude']
        long = location['longitude']
        address = location_raj.reverse_location(lat, long)
        pic_name = f"images/{lat}-{long}.jpg"

        # Save image
        a = picture.getbuffer()
        with open(pic_name, "wb") as f:
            f.write(a)

        # Insert into database
        data_storage.insert_data(email, ph_no, address, pic_name, a, breadth, height, length)

        st.success(f"""
        ✅ Report Submitted Successfully!

        📍 Location: {address["display_name"]}

        📷 Picture saved as `{pic_name}`

        📐 Dimensions (in meters):
        - Breadth: {breadth} m
        - Length: {length} m
        - Depth: {height} m
        """)

# -------------------- Footer --------------------
st.markdown("---")
st.markdown("© 2025 EcoRoad Project | Made with ❤️ for a cleaner, greener tomorrow")
