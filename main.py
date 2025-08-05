import streamlit as st
from PIL import Image

# Set page configuration
st.set_page_config(
    page_title="EcoRoad - Road Filling Project",
    page_icon="🌱",
    layout="wide"
)

# Optional: Add background image using custom CSS
st.markdown("""
    <style>
        .main {
            background-color: #f5fff5;
            background-image: linear-gradient(rgba(255,255,255,0.9), rgba(255,255,255,0.95)), url('https://images.unsplash.com/photo-1576526061095-e43b49ee1d5a?auto=format&fit=crop&w=1950&q=80');
            background-size: cover;
            background-attachment: fixed;
        }
        h1, h2, h3 {
            color: #2e7d32;
        }
        .info-card {
            border-radius: 12px;
            padding: 1.5rem;
            background-color: #e8f5e9;
            box-shadow: 2px 2px 12px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4129/4129341.png", width=100)
    st.title("EcoRoad 🌱")
    st.markdown("**Sustainable Road Filling System**")
    st.markdown("Built with ❤️ for cleaner infrastructure")

# Title and Intro
st.title("🌿 EcoRoad - Road Filling Dashboard")
st.markdown("### A community-driven initiative for sustainable road maintenance")

st.markdown("EcoRoad aims to monitor and manage **road damages** and **filling operations** with an eco-friendly approach, minimizing carbon footprints while maximizing road safety and infrastructure lifespan.")

# Info Cards


# Optional: Call to Action
st.markdown("## 📌 Get Started")
st.markdown("👉 Use the navigation panel on the left to upload data, simulate, and view reports.")

# Footer
st.markdown("---")
st.markdown("© 2025 EcoRoad Project | Built with GROUP 3 ESSE")

