# 🌿 EcoRoad 3D Pothole Simulation

An interactive Streamlit app that simulates potholes on road surfaces in 3D and estimates the cost of eco-friendly road filling. Designed to support sustainable infrastructure maintenance with cost visualization and intuitive sliders.


---

## 🚀 Features

- 🕳️ Random pothole generation (with depth, width, and noise)
- 📈 Realistic 3D surface visualization using matplotlib
- 📐 Calculates:
  - Maximum depth
  - Cuboid approximation volume
  - Smoothed pothole volume
- 💰 Pricing estimations:
  - Selling Price
  - Manufacturing Cost
  - Profit & Margin
- 🌱 Designed with a clean, eco-friendly UI in Streamlit

---

## 📦 Installation

Make sure you have **Python 3.7+** installed.

```bash
git clone https://github.com/jidukrishna/pothole_esse.git
cd pothole_esse
```
Use either global or vitualenv for installing packages
```
pip install -r requirements.txt
```

Running the script (in the environment)
```
streamlit run main.py --server.port 8003
```
