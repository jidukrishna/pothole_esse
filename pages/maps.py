import base64
from io import BytesIO
import numpy
import streamlit as st
import data_storage
import pandas as pd
import pydeck as pdk
from PIL import Image

# -------------------- Page Config --------------------
st.set_page_config(
    page_title="🗺️ EcoRoad - Map View",
    page_icon="🛣️",
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
        }
        .stButton button:hover {
            background-color: #1b5e20;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------- Load Data --------------------
data = data_storage.get_data("email, ph_no, address, lat, long, postcode, city, state, country, breadth, length, height, status, img_blob")

# Coordinates for map
cord = [(i[3], i[4]) for i in data]

# Convert blob to base64 image
def blob_to_base64(blob):
    image = Image.open(BytesIO(blob))
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Convert to DataFrame
df_coords = pd.DataFrame(cord, columns=["lat", "lon"])
df_data = pd.DataFrame(data, columns=[
    "email",
    "ph_no",
    "address",
    "lat",
    "long",
    "postcode",
    "city",
    "state",
    "country",
    "breadth",
    "length",
    "height",
    "status",
    "image",
])
df_data.index = numpy.arange(1, len(df_data)+1)

# Convert image column
df_data["image"] = df_data["image"].apply(lambda x: f'data:image/png;base64,{blob_to_base64(x)}')

# -------------------- Icon Layer Setup --------------------
ICON_URL = "https://upload.wikimedia.org/wikipedia/commons/e/ed/Map_pin_icon.svg"
icon_data = {
    "url": ICON_URL,
    "width": 128,
    "height": 128,
    "anchorY": 128
}
df_coords["icon"] = [icon_data] * len(df_coords)

# -------------------- PyDeck Layer --------------------
layer = pdk.Layer(
    "IconLayer",
    df_coords,
    get_position=["lon", "lat"],
    get_icon="icon",
    get_size=20,
    pickable=True
)

# -------------------- Map View --------------------
view_state = pdk.ViewState(
    latitude=df_coords["lat"].mean(),
    longitude=df_coords["lon"].mean(),
    zoom=6
)

deck_map = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    map_style="mapbox://styles/mapbox/streets-v11",
    tooltip={"text": "🧭 Latitude: {lat}\n🧭 Longitude: {lon}"}
)

# -------------------- Display --------------------
st.title("🗺️ EcoRoad Map Dashboard")
st.markdown("Explore reported road damages on the map. Click pins for location info.")

# Display Map
st.pydeck_chart(deck_map)

# -------------------- Info Section --------------------
st.subheader("📍 Selected Location Details")
if "clicked_info" not in st.session_state:
    st.session_state.clicked_info = "Click on a map pin to view report details here."

st.info(st.session_state.clicked_info)

# -------------------- Data Table --------------------
with st.expander("📊 Expand to View Full Reports Table"):
    st.dataframe(
        df_data,
        column_config={
            "image": st.column_config.ImageColumn(
                "🖼️ Pothole Image", help="Preview of the road damage", width="medium"
            )
        },
        use_container_width=True
    )

# -------------------- Footer --------------------
st.markdown("---")
st.markdown("📌 *Data retrieved from EcoRoad Storage*")
st.markdown("🌱 *Together, we pave the way for a sustainable future.*")
